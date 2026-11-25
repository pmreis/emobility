import sqlite3
import os.path as osp
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


projRootPath = Path(__file__).resolve().parent.parent

# Connect to SQLite DB and return connection
def connect_db(db_name):
    dbpath = osp.normpath(f'{projRootPath}/data/{db_name}')
    conn = sqlite3.connect(dbpath)
    conn.execute('pragma foreign_keys = ON')
    return conn

def load_countries(conn):
    return [
        r[0]
        for r in conn.execute(
            'select CountryIso from Countries order by CountryIso'
        ).fetchall()
    ]

# Generate Charts
def generate_charts(conn, country):
    data = pd.read_sql_query('''
    with recursive
        dates(InsertedDate) as (
            values(date('now', '-29 days'))
            union all
            select date(InsertedDate, '+1 day')
            from dates
            where InsertedDate < date('now')
        ),
        lastDates as (
            select InsertedDate, '0' as Qnt
            from dates
        ),
        chargersCount as (
            select c.InsertedDate, Count(c.ChargerId) as Qnt
            from Chargers c
            where c.CountryIso = :country
                and c.InsertedDate >= date('now', '-29 days')
            group by c.InsertedDate
        ),
        dataUnion as (
            select *
            from lastDates
            union
            select *
            from chargersCount
        )
    select InsertedDate, sum(Qnt) Qnt
    from dataUnion
    group by InsertedDate
    order by InsertedDate;
    ''', conn, params={'country': country})

    # Create theme, figure and axes
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    fig.autofmt_xdate(rotation=90)

    bars = ax.bar(
        x=np.arange(len(data)),  # Use range based on number of rows
        height=data['Qnt'],
        tick_label=data['InsertedDate'],  # Set tick labels to the years
        color='cornflowerblue'
    )

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom', fontsize=7)

    average_y = np.mean(data['Qnt'])
    plt.axhline(y=average_y, color='r', linestyle='--', label=f'Average Y: {average_y:.1f}')
    ax.set_title(f'{country} — Deployed chargers in the last 30 days', color='white')
    ax.set_xlabel('Date', color='white')
    ax.set_ylabel('Number of deployed chargers', color='white')
    ax.grid(True, color='gray', linestyle='--', alpha=0.5)
    ax.xaxis.grid(False)
    plt.xticks(fontsize=7, ha='center')
    plt.legend()

    filepath = osp.normpath(f'{projRootPath}/data/outputs/{country}_Last30DayDeployedChargers.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)

def main():
    db_name = 'data.db'

    conn = connect_db(db_name)
    for country in load_countries(conn):
        generate_charts(conn, country)

    conn.close()

if __name__ == "__main__":
    main()