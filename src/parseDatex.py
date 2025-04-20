import sqlite3
import xml.etree.ElementTree as ET
import os
from pathlib import Path

projRootPath = Path(
    os.getenv("DATA_SOURCE_PATH", Path(__file__).resolve().parent.parent)
)

# Connect to SQLite DB and return connection
def connect_db(db_name):
    dbpath = f"{projRootPath}/data/{db_name}"
    conn = sqlite3.connect(dbpath)
    return conn

# Parse Datex II file and return data structure with Chargers and Plugs
def parse_datex(xml_file):
    filepath = f"{projRootPath}/data/sources/{xml_file}"
    tree = ET.parse(filepath)
    root = tree.getroot()

    ns = {
        'ns' : 'http://datex2.eu/schema/3/common',
        'ns2': 'http://datex2.eu/schema/3/locationExtension',
        'ns3': 'http://datex2.eu/schema/3/locationReferencing',
        'ns4': 'http://datex2.eu/schema/3/facilities',
        'ns5': 'http://datex2.eu/schema/3/commonExtension',
        'ns6': 'http://datex2.eu/schema/3/energyInfrastructure',
        'ns7': 'http://datex2.eu/schema/3/d2Payload',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    data = {
        'chargers': [],
        'plugs': []
    }

    for site in root.findall('.//ns6:energyInfrastructureSite', ns):
        site_id = site.get('id')
        
        # Country
        country = site.find('.//ns2:countryCode', ns).text
        
        # Operator
        operator = site.find('.//ns4:operator', ns)
        operator_mob_abb = operator.get('id')
        operator_nap_abb = operator.find('.//ns4:nationalOrganisationNumber', ns).text
        operator_name = operator.find('.//ns4:name/ns:values/ns:value[@lang="pt-pt"]', ns).text.strip()

        charger = {
            'Country': country,
            'ChargerNapId': site_id,
            'OperatorMobAbb': operator_mob_abb,
            'OperatorNapAbb': operator_nap_abb,
            'OperatorName': operator_name
        }

        # The first plug id contains the Mobie abbreviation (3 letter)
        first_plug = site.find('.//ns6:refillPoint', ns)
        charger['OperatorMobAbb'] = first_plug.find('.//ns4:externalIdentifier', ns).text.split('*')[1][:3]

        data['chargers'].append(charger)

        # Parse Charger Plugs data
        for refill_point in site.findall('.//ns6:refillPoint', ns):
            plug_nap_id = refill_point.find('.//ns4:externalIdentifier', ns).text
            
            connector = refill_point.find('.//ns6:connector', ns)
            plug_design = connector.find('.//ns6:connectorType', ns).text
            voltage = int(float(connector.find('.//ns6:voltage', ns).text))
            current = int(float(connector.find('.//ns6:maximumCurrent', ns).text))
            max_power = int(float(connector.find('.//ns6:maxPowerAtSocket', ns).text))

            plug = {
                'ChargerNapId': site_id,
                'PlugNapId': plug_nap_id,
                'PlugDesign': plug_design,
                'Voltage': voltage,
                'Current': current,
                'MaxPower': max_power
            }

            data['plugs'].append(plug)

    data['chargers'].sort(key=lambda r: r['ChargerNapId'])
    data['plugs'].sort(key=lambda r: (r['ChargerNapId'], r['PlugNapId']))

    return data

def insert_chargers(conn, data):
    cursor = conn.cursor()

    for charger in data['chargers']:
        cursor.execute('''
            INSERT OR IGNORE INTO Chargers (Country, ChargerNapId, OperatorMobAbb, OperatorNapAbb, OperatorName)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            charger['Country'],
            charger['ChargerNapId'],
            charger['OperatorMobAbb'],
            charger['OperatorNapAbb'],
            charger['OperatorName']
        ))

    conn.commit()

def insert_plugs(conn, data):
    cursor = conn.cursor()

    # Inserir plugs
    for plug in data['plugs']:

        cursor.execute('SELECT Id FROM Chargers WHERE Country = ? AND ChargerNapId = ?', 
            ('PT', plug['ChargerNapId']))

        charger_id = cursor.fetchone()[0]

        if charger_id:
            cursor.execute('''
                INSERT INTO Plugs (ChargerId, PlugNapId, PlugDesign, Voltage, Current, MaxPower)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                charger_id,
                plug['PlugNapId'],
                plug['PlugDesign'],
                plug['Voltage'],
                plug['Current'],
                plug['MaxPower']
            ))

    conn.commit()


def main():
    db_name = 'data.db'
    xml_file = 'nap_EvChargingInfra.xml'

    conn = connect_db(db_name)
    data = parse_datex(xml_file)
    insert_chargers(conn, data)

if __name__ == "__main__":
    main()