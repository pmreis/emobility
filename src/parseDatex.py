import sqlite3
import xml.etree.ElementTree as et
import os.path as osp
from datetime import datetime as dt
from pathlib import Path
import pandas as pd

projRootPath = Path(__file__).resolve().parent.parent

# Connect to SQLite DB and return connection
def connect_db(db_name):
    dbpath = osp.normpath(f'{projRootPath}/data/{db_name}')
    conn = sqlite3.connect(dbpath)
    return conn

# Parse Datex II file and return data structure with Chargers and Plugs
def parse_datex(xml_file):
    filepath = osp.normpath(f'{projRootPath}/data/sources/{xml_file}')
    tree = et.parse(filepath)
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
        'operators': [],
        'chargers': [],
        'plugs': []
    }

    for site in root.findall('.//ns6:energyInfrastructureSite', ns):
        site_id = site.get('id')

        # Charger Location
        city = site.find('.//ns2:city/ns:values/ns:value[@lang="pt-pt"]', ns).text.strip()
        country = site.find('.//ns2:countryCode', ns).text.strip()
        insertedDate = dt.today().strftime('%Y-%m-%d')

        latitude = float(site.find('.//ns3:latitude', ns).text.strip())
        longitude = float(site.find('.//ns3:longitude', ns).text.strip())

        # Operator
        operator_elem = site.find('.//ns4:operator', ns)
        operator_abb = site.find('.//ns6:refillPoint/ns4:externalIdentifier', ns).text.split('*')[1][:3]
        operator_other_abb = operator_elem.find('.//ns4:nationalOrganisationNumber', ns).text.strip()
        operator_name = operator_elem.find('.//ns4:name/ns:values/ns:value[@lang="pt-pt"]', ns).text.strip()
        operator_tin = operator_elem.find('.//ns4:vatIdentificationNumber', ns).text.replace(' ', '').strip()
        operator_phone = operator_elem.find('.//ns4:telephoneNumber', ns).text.replace(' ', '').strip()

        charger = {
            'ChargerId': site_id,
            'Country': country,
            'OperatorAbb': operator_abb,
            'City': city,
            'InsertedDate': insertedDate,
            'Lat': latitude,
            'Lon': longitude
        }

        charger['Data'] = f'{charger['ChargerId']}{charger['Country']}{charger['OperatorAbb']}{charger['City']}{charger['Lat']}{charger['Lon']}'

        operator = {
            'OperatorAbb': operator_abb,
            'OperatorOtherAbb': operator_other_abb,
            'OperatorName': operator_name,
            'CountryIso': country,
            'Tin': operator_tin,
            'Phone': operator_phone
        }

        data['operators'].append(operator)
        data['chargers'].append(charger)

        # Parse Charger Plugs data
        for refill_point in site.findall('.//ns6:refillPoint', ns):
            plug_element = refill_point.find('.//ns4:externalIdentifier', ns)
            if plug_element is None:
                continue

            plug_id = refill_point.find('.//ns4:externalIdentifier', ns).text.strip()

            connector = refill_point.find('.//ns6:connector', ns)
            plug_design = connector.find('.//ns6:connectorType', ns).text
            voltage = int(float(connector.find('.//ns6:voltage', ns).text))
            current = int(float(connector.find('.//ns6:maximumCurrent', ns).text))
            max_power = int(float(connector.find('.//ns6:maxPowerAtSocket', ns).text))

            plug = {
                'PlugId': plug_id,
                'ChargerId': site_id,
                'PlugDesign': plug_design,
                'Voltage': voltage,
                'Current': current,
                'MaxPower': max_power
            }

            data['plugs'].append(plug)

    data['operators'].sort(key=lambda r: r['OperatorAbb'])
    data['chargers'].sort(key=lambda r: r['ChargerId'])
    data['plugs'].sort(key=lambda r: (r['ChargerId'], r['PlugId']))

    return data


# Insert operators
def insert_operators(conn, data):
    cursor = conn.cursor()

    for operator in data['operators']:
        cursor.execute('''
            INSERT OR IGNORE INTO Operators (OperatorAbb, OperatorOtherAbb, OperatorName, CountryIso, Tin, Phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            operator['OperatorAbb'],
            operator['OperatorOtherAbb'],
            operator['OperatorName'],
            operator['CountryIso'],
            operator['Tin'],
            operator['Phone']
        ))

    conn.commit()

# Insert temp chargers (only IDs)
def insert_tmp_chargers(conn, data):
    cursor = conn.cursor()

    cursor.execute('''
        create table TempChargers (
            ChargerId varchar(36) primary key
        );
    ''')

    for charger in data['chargers']:
        cursor.execute('''
            INSERT INTO TempChargers (ChargerId)
            VALUES (?)
        ''', (
            charger['ChargerId'],
        ))

    cursor.execute('''
            update Chargers
            set Status = 'Removed'
            where ChargerId not in (
                select ChargerId
                from TempChargers
            )
        ''')

    cursor.execute('''
        update Chargers
        set Status = 'Present'
        where ChargerId in (
            select ChargerId
            from TempChargers
        )
    ''')

    cursor.execute('drop table TempChargers')

    conn.commit()

# Insert or update chargers
def insert_or_update_chargers(conn, data):
    cursor = conn.cursor()

    for charger in data['chargers']:
        chargerId = charger['ChargerId']
        cursor.execute('SELECT CONCAT(ChargerId, Country, OperatorAbb, City, Lat, Lon) FROM Chargers WHERE ChargerId = ?', (chargerId,))
        row = cursor.fetchone()
        if(row is None):
            cursor.execute('''
                INSERT OR IGNORE INTO Chargers (ChargerId, Country, OperatorAbb, City, InsertedDate, Lat, Lon)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                charger['ChargerId'],
                charger['Country'],
                charger['OperatorAbb'],
                charger['City'],
                charger['InsertedDate'],
                charger['Lat'],
                charger['Lon']
            ))

            conn.commit()
            continue

        else:
            existingChargerData = row[0]
            if(existingChargerData != charger['Data']):
                cursor.execute('''
                    UPDATE Chargers
                    SET Country = ?, OperatorAbb = ?, City = ?, InsertedDate = ?, Lat = ?, Lon = ?
                    WHERE ChargerId = ?
                ''', (
                    charger['Country'],
                    charger['OperatorAbb'],
                    charger['City'],
                    charger['InsertedDate'],
                    charger['Lat'],
                    charger['Lon'],
                    charger['ChargerId']
                ))

                conn.commit()

# Insert plugs
def insert_plugs(conn, data):
    cursor = conn.cursor()

    # Inserir plugs
    for plug in data['plugs']:
            cursor.execute('''
                INSERT OR IGNORE INTO Plugs (ChargerId, PlugId, PlugDesign, Voltage, Current, MaxPower)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                plug['ChargerId'],
                plug['PlugId'],
                plug['PlugDesign'],
                plug['Voltage'],
                plug['Current'],
                plug['MaxPower']
            ))

    conn.commit()

# Generate CSVs
def generate_output_csvs(conn):

    data = pd.read_sql_query('''
        with recursive
        countAllChargers as (
            select count(1) total
            from Chargers
        ),
        cte1 as (
            select
                OperatorAbb party_id,
            count(1) as 'count'
            from Chargers
            group by OperatorAbb
            order by count desc
        ),
        cte2 as (
            select
            row_number() over() idx,
            cte1.*,
            cast(cte1.count as real) / cast(countAllChargers.total as real) mrkt_shr
            from cte1, countAllChargers
        )
    select
        cte2.*,
        sum(mrkt_shr) over (order by idx) mrkt_shr_acc
    from cte2
    ''', conn)

    filepath = osp.normpath(f'{projRootPath}/data/outputs/PT_Market_Share_Analysis.csv')
    data.to_csv(filepath, sep=",", index=None, mode="w")

    # Output Operators as CSV
    data = pd.read_sql_query('''
        select * from Operators order by OperatorAbb
    ''', conn)
    filepath = osp.normpath(f'{projRootPath}/data/outputs/PT_Operators.csv')
    data.to_csv(filepath, sep=",", index=None, mode="w")

    # Output Chargers as CSV
    data = pd.read_sql_query('''
        select * from Chargers order by ChargerId
    ''', conn)
    filepath = osp.normpath(f'{projRootPath}/data/outputs/PT_Chargers.csv')
    data.to_csv(filepath, sep=",", index=None, mode="w")

    # Output Today's New Chargers as CSV
    data = pd.read_sql_query('''
        select ChargerId,
            OperatorAbb,
            City,
            Lat,
            Lon
        from Chargers c
        where c.InsertedDate = date('now')
    ''', conn)
    filepath = osp.normpath(f'{projRootPath}/data/outputs/PT_Chargers_New_Today.csv')
    data.to_csv(filepath, sep=",", index=None, mode="w")

    # Output Chargers per Municipality
    data = pd.read_sql_query('''
        select City, count(1) Qty
        from Chargers
        group by City
        order by Qty desc, City asc;
    ''', conn)
    filepath = osp.normpath(f'{projRootPath}/data/outputs/PT_Chargers_Per_Municipality.csv')
    data.to_csv(filepath, sep=",", index=None, mode="w")

    # Output Chargers per District
    data = pd.read_sql_query('''
        select d.Distrito, count(1) Qty
        from Chargers c
        join Concelhos cc on cc.Alias = c.City
        join Distritos d on d.Id = cc.Distrito
        group by d.Id
        order by Qty desc, d.Distrito asc;
    ''', conn)
    filepath = osp.normpath(f'{projRootPath}/data/outputs/PT_Chargers_Per_District.csv')
    data.to_csv(filepath, sep=",", index=None, mode="w")

    # Output Plugs
    data = pd.read_sql_query('''
        select p.ChargerId, p.PlugId, p.MaxPower
        from Plugs p
        where p.PlugDesign != 'chademo'
        order by p.ChargerId, p.PlugId;
    ''', conn)
    filepath = osp.normpath(f'{projRootPath}/data/outputs/PT_Plugs_NonChademo.csv')
    data.to_csv(filepath, sep=",", index=None, mode="w")

    #conn.execute("VACUUM")
    conn.close()


def main():
    db_name = 'data.db'
    xml_file = 'PT_NAP_Static.xml'

    conn = connect_db(db_name)
    data = parse_datex(xml_file)
    insert_operators(conn, data)
    insert_or_update_chargers(conn, data)
    insert_plugs(conn, data)
    insert_tmp_chargers(conn, data)
    generate_output_csvs(conn)

if __name__ == "__main__":
    main()
