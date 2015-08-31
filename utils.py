import psycopg2
import os
import csv

DATA_DIR = "/Users/nickwang/Downloads/drivers/1/"

def connect_db():
    conn = psycopg2.connect("dbname='telematics' user='driver' password=''")
    return conn

def create_drive_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE driver_test (id serial PRIMARY KEY, driver_id integer, trip_id varchar, x float, y float);")
    conn.commit()

    cursor.close()
    conn.close()

def seed_data():
    for subdir, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if "csv" in file:
                driver_id = 1
                trip_id = file.split('.')[0]
                path = subdir + file
                with open(path, "rb") as infile:
                    reader = csv.reader(infile)
                    next(reader, None)
                    for row in reader:
                        yield driver_id, trip_id, row[0], row[1]

def insert_data(cursor, driver, trip, x, y):
    cursor.execute('INSERT INTO driver_test (driver_id, trip_id, x, y) VALUES (%s, %s, %s, %s)', (driver, trip, x, y))

def batch_insert():
    conn = connect_db()
    cursor = conn.cursor()
    for driver, trip, x, y in seed_data():
        insert_data(cursor, driver, trip, x, y)

    conn.commit()

    cursor.close()
    conn.close()

if __name__ == "__main__":

