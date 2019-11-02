import sqlite3
import os
from kivy.utils import platform

DB_FILE_PATH = 'geolocalizationapp.db'

class HandlerOfLocationsData:

    LIST_FIELDS = ["id", "name", "lat", "lon", "date", "photopath"]

    def __init__(self, name_file):
        self.name_file = name_file
        if not os.path.exists(name_file):
            self.create_table()
            self.insert_data_example()

    def create_table(self):
        sql =  '''
        CREATE TABLE IF NOT EXISTS locations(
            id integer PRIMARY KEY,
            name text NOT NULL,
            lat real NOT NULL,
            lon real NOT NULL,
            date text NOT NULL,
            photopath text NOT NULL
        )
        '''
        with sqlite3.connect(self.name_file) as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()

    def get_all_locations(self):
        result = []
        sql = "SELECT * FROM locations"
        with sqlite3.connect(self.name_file) as connection:
            cursor = connection.cursor()
            result_query = cursor.execute(sql).fetchall()
            for row in result_query:
                result.append(self.row_dict(row))

        return result

    def delete_location(self, id_location):
        sql = "DELETE FROM locations WHERE id = ?"
        with sqlite3.connect(self.name_file) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, (id_location,))
            connection.commit()

    def insert_data_example(self):
        data = [
            ("Alterosa", -21.249214, -46.1478561, "19/08/2017", "locations/alterosa.jpg"),
            ("Carmo do Rio Claro", -20.97152, -46.1234176,"23/11/2017", "locations/carmodorioclaro.jpg"),
            ("Areado", -21.3574435, -46.1609584, "05/02/2018", "locations/areado.jpg"),
            ("Alfenas", -21.4273559, -45.9963879, "08/02/2018", "locations/alfenas.jpg"),
            ("Passos", -20.7233071, -46.6496642, "10/03/2018", "locations/passos.jpg")
        ]
        sql = "INSERT INTO locations(name, lat, lon, date, photopath) VALUES (?, ?, ?, ?, ?)"
        with sqlite3.connect(self.name_file) as connection:
            cursor = connection.cursor()
            cursor.executemany(sql, data)
            connection.commit()

    def insert_location(self, data):
        sql = "INSERT INTO locations(name, lat, lon, date, photopath) VALUES (?, ?, ?, ?, ?)"
        values = (data["name"], data["lat"], data["lon"], data["date"], data["photopath"])
        with sqlite3.connect(self.name_file) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()

    def row_dict(self, row):
        d = {}
        cont = 0
        for field in self.LIST_FIELDS:
            d[field] = row[cont]
            cont += 1
        return d


db = HandlerOfLocationsData(DB_FILE_PATH)
