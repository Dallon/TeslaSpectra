import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def new_entry(conn, entry):
    """
    Create a new entry into the US_vehicle_prices table using the parameters
    """
    sql = ''' INSERT INTO US_vehicle_prices(name, price, date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"C:\sqlite\db\teslaspectra.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new entry

if __name__ == '__main__':
    main()

