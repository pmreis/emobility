import sqlite3
import xml.etree.ElementTree as et
import os.path as osp
from datetime import datetime as dt
from pathlib import Path
import pandas as pd
import gzip

projRootPath = Path(__file__).resolve().parent.parent

COUNTRIES = ['PT', 'ES']

def noneToStrNull(s):
    if s is None:
        return "Null"
    else:
        return s

def logError(data, chargerId, error):
    errorLog = {
        'ChargerId': chargerId,
        'Error': error,
        'LoggedDate': dt.today().strftime('%Y-%m-%d')
    }
    data['errors'].append(errorLog)

def element_text(elem):
    if elem is None or elem.text is None:
        return None
    text = elem.text.strip()
    return text if text else None

def extract_city(site, ns):
    city = element_text(site.find('.//ns2:city/ns:values/ns:value', ns))
    if city is not None:
        return city

    # ES-style DATEX: municipality embedded in addressLine text
    for address_line in site.findall('.//ns2:addressLine', ns):
        for value in address_line.findall('.//ns:value', ns):
            text = element_text(value)
            if text is None:
                continue
            prefix = 'Municipio:'
            if text.startswith(prefix):
                city = text[len(prefix):].strip()
                if city:
                    return city
    return None

# Connect to SQLite DB and return connection
def connect_db(db_name):
    dbpath = osp.normpath(f'{projRootPath}/data/{db_name}')
    conn = sqlite3.connect(dbpath)
    return conn

# Decompress gz file and obtain the Datex II content into memory
def decompress_datex(xml_file):
    filepath = osp.normpath(f'{projRootPath}/data/sources/{xml_file}.gz')
    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        file_content_str = f.read()
    return file_content_str

def output_csv_path(country, filename):
    return osp.normpath(f'{projRootPath}/data/outputs/{country}_{filename}.csv')

# Parse Datex II in memory and return data structure with Chargers and Plugs
def parse_datex(datexInMemory, default_country):
    root = et.fromstring(datexInMemory)

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
        'plugs': [],
        'errors': []
    }

    insertedDate = dt.today().strftime('%Y-%m-%d')

    for site in root.findall('.//ns6:energyInfrastructureSite', ns):
        site_id = site.get('id')
        if site_id.count('-') >= 2:
            site_id = site_id.split('-', 1)[1] # Splits by dash, only once and gets the 2nd array value of the split. The first index of the array is 0.

        # Charger Location
        city = noneToStrNull(extract_city(site, ns))
        if city == "Null":
            logError(data, site_id, 'City is missing')

        country = element_text(site.find('.//ns2:countryCode', ns))
        if country is None:
            country = default_country

        latitude = float(site.find('.//ns3:latitude', ns).text.strip())
        longitude = float(site.find('.//ns3:longitude', ns).text.strip())

        # Operator
        operator_elem = site.find('.//ns4:operator', ns)
        operator_abb = None

        # Prefer fac:operator id (e.g. ES*CEP -> CEP)
        if operator_elem is not None:
            op_id = operator_elem.get('id')
            if op_id and '*' in op_id:
                operator_abb = op_id.split('*', 1)[1][:3]

        if operator_abb is None:
            operator_abb_elem = site.find('.//ns6:refillPoint/ns4:externalIdentifier', ns)
            if operator_abb_elem is not None and operator_abb_elem.text and '*' in operator_abb_elem.text:
                operator_abb = operator_abb_elem.text.split('*')[1][:3]
            else:
                # The refillPoint ID might have either an asterisk (*) as separator or a hyphen (-)
                refill = site.find('.//ns6:refillPoint', ns)
                refillId = refill.get('id').strip() if refill is not None and refill.get('id') else ''
                if '-' in refillId:
                    operator_abb = refillId.split('-')[1][:3]
                elif '*' in refillId:
                    operator_abb = refillId.split('*')[1][:3]

        if operator_abb is None:
            logError(data, site_id, 'Operator abbreviation is missing')
            operator_abb = 'Null'

        if operator_elem is not None:
            other_abb = element_text(operator_elem.find('.//ns4:nationalOrganisationNumber', ns))
            operator_name = element_text(operator_elem.find('.//ns4:name/ns:values/ns:value', ns))
            tin = element_text(operator_elem.find('.//ns4:vatIdentificationNumber', ns))
            phone = element_text(operator_elem.find('.//ns4:telephoneNumber', ns))

            operator = {
                'OperatorAbb': operator_abb,
                'OperatorOtherAbb': other_abb if other_abb is not None else '',
                'OperatorName': operator_name if operator_name is not None else '',
                'CountryIso': country,
                'Tin': tin.replace(' ', '') if tin is not None else '',
                'Phone': phone.replace(' ', '') if phone is not None else ''
            }

            data['operators'].append(operator)
        else:
            logError(data, site_id, 'OPC is missing')

        # Charger Block
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

        data['chargers'].append(charger)


        # Connectors / Plugs
        for refill_point in site.findall('.//ns6:refillPoint', ns):
            plug_element = refill_point.find('.//ns4:externalIdentifier', ns)
            if plug_element is not None:
                plug_id = plug_element.text.strip()
            else:
                # The refillPoint ID might have either an asterisk (*) as separator or a hyphen (-)
                refillId = refill_point.get('id').strip()
                if '-' in refillId:
                    plug_id = refillId.replace('-', '*')
                else:
                    plug_id = refillId

            connector = refill_point.find('.//ns6:connector', ns)
            if connector is None:
                logError(data, site_id, f'Connector is missing on RefillPoint {refill_point.get('id')}')
                continue

            plug_design = element_text(connector.find('.//ns6:connectorType', ns))
            if plug_design is None:
                logError(data, site_id, f'ConnectorType is missing on RefillPoint {refill_point.get("id")}')
                continue

            voltage_text = element_text(connector.find('.//ns6:voltage', ns))
            current_text = element_text(connector.find('.//ns6:maximumCurrent', ns))
            max_power_text = element_text(connector.find('.//ns6:maxPowerAtSocket', ns))

            # Defaults match db_schema.sql when ES (or others) omit electrical fields
            voltage = int(float(voltage_text)) if voltage_text is not None else 400
            current = int(float(current_text)) if current_text is not None else 16
            max_power = int(float(max_power_text)) if max_power_text is not None else 11000

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
    data['errors'].sort(key=lambda r: (r['ChargerId'], r['Error']))

    return data


# Insert operators
def insert_operators(conn, data):
    cursor = conn.cursor()

    for operator in data['operators']:
        cursor.execute('''
            insert or ignore into Operators (OperatorAbb, OperatorOtherAbb, OperatorName, CountryIso, Tin, Phone)
            values (?, ?, ?, ?, ?, ?);
        ''', (
            operator['OperatorAbb'],
            operator['OperatorOtherAbb'],
            operator['OperatorName'],
            operator['CountryIso'],
            operator['Tin'],
            operator['Phone']
        ))

    conn.commit()

def insert_errors(conn, data):
    cursor = conn.cursor()

    for error in data['errors']:
        cursor.execute('''
            insert or ignore into ParseErrors (ChargerId, Error, LoggedDate)
            values (?, ?, ?);
        ''', (
            error['ChargerId'],
            error['Error'],
            error['LoggedDate']
        ))

    conn.commit()

# Insert temp chargers (only IDs)
def tmp_chargers_deltas(conn, data, country):
    cursor = conn.cursor()

    cursor.execute('''
        create table TempChargers (
            ChargerId varchar(36) primary key
        );
    ''')

    for charger in data['chargers']:
        cursor.execute('''
            insert into TempChargers (ChargerId)
            values (?);
        ''', (charger['ChargerId'],))

    # Output Removed Delta
    query = pd.read_sql_query('''
        select c.ChargerId,
            c.OperatorAbb,
            o.OperatorName,
            c.City,
            c.Lat,
            c.Lon
        from Chargers c
        join Operators o on o.OperatorAbb = c.OperatorAbb
        where c.Country = :country
            and c.Active = 'Yay'
            and c.ChargerId not in (
                select ChargerId
                from TempChargers
            );
    ''', conn, params={'country': country})
    query.to_csv(output_csv_path(country, 'Chargers_Today_Removed'), sep=",", index=None, mode="w")

    cursor.execute('''
        update Chargers
        set Active = 'Nay'
        where Country = ?
            and ChargerId not in (
                select ChargerId
                from TempChargers
            );
    ''', (country,))

    # Output Readded Delta
    query = pd.read_sql_query('''
        select c.ChargerId,
            c.OperatorAbb,
            o.OperatorName,
            c.City,
            c.Lat,
            c.Lon
        from Chargers c
        join Operators o on o.OperatorAbb = c.OperatorAbb
        where c.Country = :country
            and c.Active = 'Nay'
            and c.ChargerId in (
                select ChargerId
                from TempChargers
            );
    ''', conn, params={'country': country})
    query.to_csv(output_csv_path(country, 'Chargers_Today_Readded'), sep=",", index=None, mode="w")

    cursor.execute('''
        update Chargers
        set Active = 'Yay'
        where Country = ?
            and ChargerId in (
                select ChargerId
                from TempChargers
            );
    ''', (country,))

    cursor.execute('''
        delete from Plugs
        where ChargerId in (select ChargerId from TempChargers);
    ''')

    cursor.execute('drop table TempChargers')

    conn.commit()

# Insert or update chargers
def insert_or_update_chargers(conn, data):
    cursor = conn.cursor()

    for charger in data['chargers']:
        chargerId = charger['ChargerId']
        cursor.execute('select concat(ChargerId, Country, OperatorAbb, City, Lat, Lon) from Chargers where ChargerId = ?;', (chargerId,))
        row = cursor.fetchone()
        if(row is None):
            cursor.execute('''
                insert or ignore into Chargers (ChargerId, Country, OperatorAbb, City, InsertedDate, Lat, Lon)
                values (?, ?, ?, ?, ?, ?, ?);
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
                    update Chargers
                    set Country = ?, OperatorAbb = ?, City = ?, Lat = ?, Lon = ?
                    where ChargerId = ?;
                ''', (
                    charger['Country'],
                    charger['OperatorAbb'],
                    charger['City'],
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
            insert or ignore into Plugs (ChargerId, PlugId, PlugDesign, Voltage, Current, MaxPower)
            values (?, ?, ?, ?, ?, ?);
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
def generate_output_csvs(conn, country):
    params = {'country': country}

    query = pd.read_sql_query('''
        with
        countAllChargers as (
            select count(1) total
            from Chargers
            where Country = :country
                and Active = 'Yay'
        ),
        cte1 as (
            select
                o.OperatorAbb 'Operator',
                o.OperatorName,
                count(c.OperatorAbb) as 'Qty'
            from Operators o
            left join Chargers c on c.OperatorAbb = o.OperatorAbb
                and o.CountryIso = :country
                and c.Active = 'Yay'
            group by o.OperatorAbb
            order by Qty desc
        ),
        cte2 as (
            select
            row_number() over() 'Rank',
            cte1.*,
            cast(cte1.Qty as real) / cast(countAllChargers.total as real) 'MarketShare'
            from cte1, countAllChargers
        )
        select
        cte2.*,
        sum(MarketShare) over (order by Rank) 'CumulativeMarketShare'
        from cte2;
    ''', conn, params=params)
    query.to_csv(output_csv_path(country, 'Market_Share_Analysis'), sep=",", index=None, mode="w")

    # PT-only: market share aggregating Galp OPCs
    if country == 'PT':
        query = pd.read_sql_query('''
            with
            countAllChargers as (
                select count(1) total
                from Chargers
                where Country = :country
                    and Active = 'Yay'
            ),
            galpGroupData as (
                select
                    'GRG' as 'OperatorAbb',
                    'Grupo Galp (GLP+GLG+MLT)' as 'OperatorName',
                    count(c.ChargerId) as 'Qty'
                from Chargers c
                join Operators o on o.OperatorAbb = c.OperatorAbb
                where c.OperatorAbb in ('GLP', 'GLG', 'MLT')
                    and o.CountryIso = :country
                    and c.Active = 'Yay'
            ),
            allDataExpectGalp as (
                select
                    o.OperatorAbb,
                    o.OperatorName,
                    count(c.OperatorAbb) as 'Qty'
                from Operators o
                left join Chargers c on c.OperatorAbb = o.OperatorAbb
                    and o.CountryIso = :country
                    and c.Active = 'Yay'
                where o.OperatorAbb not in ('GLP', 'GLG', 'MLT')
                group by o.OperatorAbb
            ),
            allData as (
                select OperatorAbb, OperatorName, Qty
                from galpGroupData
                union
                select OperatorAbb, OperatorName, Qty
                from allDataExpectGalp
                order by Qty desc
            ),
            cte2 as (
                select
                row_number() over() 'Rank',
                allData.*,
                cast(allData.Qty as real) / cast(countAllChargers.total as real) 'MarketShare'
                from allData, countAllChargers
            )
            select
            cte2.*,
            sum(MarketShare) over (order by Rank) 'CumulativeMarketShare'
            from cte2;
        ''', conn, params=params)
        query.to_csv(output_csv_path(country, 'Market_ShareAgg_Analysis'), sep=",", index=None, mode="w")

    # Output installed power per Operator as CSV
    query = pd.read_sql_query('''
        select o.OperatorAbb, o.OperatorName, sum(p.MaxPower)/1000 'Total Power (kW)'
        from Plugs p
        join Chargers c on c.ChargerId = p.ChargerId
        join Operators o on o.OperatorAbb = c.OperatorAbb
        where o.CountryIso = :country
            and c.Active = 'Yay'
        group by o.OperatorAbb, o.OperatorName
        order by sum(p.MaxPower) desc;
    ''', conn, params=params)
    query.to_csv(output_csv_path(country, 'Market_PowerShare_Analysis'), sep=",", index=None, mode="w")

    # PT-only: installed power aggregating Galp OPCs
    if country == 'PT':
        query = pd.read_sql_query('''
            with
            galpGroupData as (
                select 'GRG' OperatorAbb, 'Grupo Galp (GLP+GLG+MLT)' OperatorName, sum(p.MaxPower)/1000 total
                from Plugs p
                join Chargers c on c.ChargerId = p.ChargerId
                join Operators o on o.OperatorAbb = c.OperatorAbb
                where o.OperatorAbb in ('GLP', 'GLG', 'MLT')
                    and o.CountryIso = :country
                    and c.Active = 'Yay'
            ),
            allDataExpectGalp as (
                select o.OperatorAbb, o.OperatorName, sum(p.MaxPower)/1000 total
                from Plugs p
                join Chargers c on c.ChargerId = p.ChargerId
                join Operators o on o.OperatorAbb = c.OperatorAbb
                where o.OperatorAbb not in ('GLP', 'GLG', 'MLT')
                    and o.CountryIso = :country
                    and c.Active = 'Yay'
                group by o.OperatorAbb, o.OperatorName
            )
            select OperatorAbb, OperatorName, total 'Total Power (kW)'
            from galpGroupData
            union
            select OperatorAbb, OperatorName, total 'Total Power (kW)'
            from allDataExpectGalp
            order by total desc;
        ''', conn, params=params)
        query.to_csv(output_csv_path(country, 'Market_PowerShareAgg_Analysis'), sep=",", index=None, mode="w")

    # Output Operators as CSV
    query = pd.read_sql_query('''
        select *
        from Operators
        where CountryIso = :country
        order by OperatorAbb;
    ''', conn, params=params)
    query.to_csv(output_csv_path(country, 'Operators'), sep=",", index=None, mode="w")

    # Output Active Chargers as CSV
    query = pd.read_sql_query('''
        select ChargerId,
            OperatorAbb,
            City,
            InsertedDate,
            Lat,
            Lon
        from Chargers
        where Country = :country and Active = 'Yay'
        order by ChargerId;
    ''', conn, params=params)
    query.to_csv(output_csv_path(country, 'Chargers_Active'), sep=",", index=None, mode="w")

    # Output Inactive Chargers as CSV
    query = pd.read_sql_query('''
        select ChargerId,
            OperatorAbb,
            City,
            InsertedDate,
            Lat,
            Lon
        from Chargers
        where Country = :country and Active = 'Nay'
        order by ChargerId;
    ''', conn, params=params)
    query.to_csv(output_csv_path(country, 'Chargers_Inactive'), sep=",", index=None, mode="w")

    # Output Today's New Chargers as CSV
    query = pd.read_sql_query('''
        select c.ChargerId,
            c.OperatorAbb,
            o.OperatorName,
            c.City,
            c.Lat,
            c.Lon
        from Chargers c
        join Operators o on o.OperatorAbb = c.OperatorAbb
        where c.InsertedDate = date('now')
            and c.Country = :country
        order by ChargerId;
    ''', conn, params=params)
    query.to_csv(output_csv_path(country, 'Chargers_Today_New'), sep=",", index=None, mode="w")

    # Output Chargers per Municipality
    query = pd.read_sql_query('''
        select City, count(1) Qty
        from Chargers
        where Country = :country
            and Active = 'Yay'
        group by City
        order by Qty desc, City asc;
    ''', conn, params=params)
    query.to_csv(output_csv_path(country, 'Chargers_Per_Municipality'), sep=",", index=None, mode="w")

    # PT-only: chargers per district (Concelhos/Distritos)
    if country == 'PT':
        query = pd.read_sql_query('''
            select d.Distrito, count(1) Qty
            from Chargers c
            join Concelhos cc on cc.Alias = c.City
            join Distritos d on d.Id = cc.Distrito
            where c.Country = :country
                and Active = 'Yay'
            group by d.Id
            order by Qty desc, d.Distrito asc;
        ''', conn, params=params)
        query.to_csv(output_csv_path(country, 'Chargers_Per_District'), sep=",", index=None, mode="w")

    # Output Plugs Pt1
    query = pd.read_sql_query('''
        select p.ChargerId, p.PlugId, p.MaxPower
        from Plugs p
        join Chargers c on c.ChargerId = p.ChargerId
        where c.Country = :country
            and p.PlugDesign != 'chademo'
            and substr(p.ChargerId, 1, 1) <= 'L'
        order by p.ChargerId, p.PlugId
    ''', conn, params=params)
    query.to_csv(output_csv_path(country, 'Plugs_NonChademo_1'), sep=",", index=None, mode="w")

    # Output Plugs Pt2
    query = pd.read_sql_query('''
        select p.ChargerId, p.PlugId, p.MaxPower
        from Plugs p
        join Chargers c on c.ChargerId = p.ChargerId
        where c.Country = :country
            and p.PlugDesign != 'chademo'
            and substr(p.ChargerId, 1, 1) > 'L'
        order by p.ChargerId, p.PlugId
    ''', conn, params=params)
    query.to_csv(output_csv_path(country, 'Plugs_NonChademo_2'), sep=",", index=None, mode="w")

    # Output Errors for this country's chargers
    query = pd.read_sql_query('''
        select e.*
        from ParseErrors e
        join Chargers c on c.ChargerId = e.ChargerId
        where c.Country = :country
        order by e.ChargerId, e.Error
    ''', conn, params=params)
    query.to_csv(output_csv_path(country, 'Errors'), sep=",", index=None, mode="w")


def main():
    db_name = 'data.db'
    conn = connect_db(db_name)

    for country in COUNTRIES:
        xml_file = f'{country}_NAP_Static.xml'
        datex = decompress_datex(xml_file)
        data = parse_datex(datex, country)
        insert_operators(conn, data)
        insert_or_update_chargers(conn, data)
        tmp_chargers_deltas(conn, data, country)
        insert_plugs(conn, data)
        insert_errors(conn, data)
        generate_output_csvs(conn, country)

    conn.execute("VACUUM")
    conn.close()

if __name__ == "__main__":
    main()
