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
    return conn

# Generate Charts
def generate_charts(conn):
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
            where c.InsertedDate >= date('now', '-29 days')
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
    ''', conn)

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
    ax.set_title('Deployed chargers in the last 30 days', color='white')
    ax.set_xlabel('Date', color='white')
    ax.set_ylabel('Number of deployed chargers', color='white')
    ax.grid(True, color='gray', linestyle='--', alpha=0.5)
    ax.xaxis.grid(False)
    plt.xticks(fontsize=7, ha='center')
    plt.legend()

    filepath = osp.normpath(f'{projRootPath}/data/outputs/PT_Last30DayDeployedChargers.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')

def main():
    db_name = 'data.db'

    conn = connect_db(db_name)
    generate_charts(conn)

    conn.close()

if __name__ == "__main__":
    main()