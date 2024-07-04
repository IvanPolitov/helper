import sqlite3
from typing import Tuple


class SQL:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
               PRAGMA foreign_keys = ON''')

        self.cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
                flag_daily_forecast BOOLEAN,
                flag_weekly_forecast BOOLEAN,
                default_location TEXT
                               )
                ''')

        self.cursor.execute('''
               CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user INTEGER ,
                longitude FLOAT ,
                latitude FLOAT ,
                name TEXT,
               CONSTRAINT fk_user
                FOREIGN KEY (user)
               REFERENCES users(id) ON DELETE CASCADE
                )
                ''')
        self.connection.close()

    def create_user(self, id, flag_daily_forecast=False, flag_weekly_forecast=False, default_location=None):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                            INSERT INTO users (id, flag_daily_forecast, flag_weekly_forecast, default_location) VALUES (?,?,?,?)''',
                            (id, flag_daily_forecast, flag_weekly_forecast, default_location,))
        self.connection.commit()
        self.connection.close()

    def create_location(self, user, longitude, latitude, name):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                            INSERT INTO locations  (user, longitude, latitude, name) VALUES  (?,?,?,?)''',
                            (user, longitude, latitude, name,))
        self.connection.commit()
        self.connection.close()

    def get_user(self, id) -> Tuple[int, bool, bool, str]:
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        res = self.cursor.execute('''
                            SELECT * FROM users WHERE id = ?''', (id,)).fetchone()
        self.connection.close()
        return res

    def set_user_default_location(self, id, default_location):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                            UPDATE users
                            SET default_location = ?
                            WHERE id = ?''', (default_location, id))
        self.connection.commit()
        self.connection.close()

    def set_user_flag_daily_forecast(self, id, flag):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                            UPDATE users
                            SET flag_daily_forecast = ?
                            WHERE id = ?''', (flag, id))
        self.connection.commit()
        self.connection.close()

    def set_user_flag_weekly_forecast(self, id, flag):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                            UPDATE users
                            SET flag_weekly_forecast = ?
                            WHERE id = ?''', (flag, id))
        self.connection.commit()
        self.connection.close()

    def get_user_default_location(self, id):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        res = self.cursor.execute('''
                            SELECT * FROM locations
                            WHERE user = ? AND
                                name =
                                (SELECT default_location FROM users WHERE id = ?)
                            ''', (id, id)).fetchone()
        self.connection.close()
        return res

    def get_locations(self, id):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        res = self.cursor.execute('''
                            SELECT name, longitude, latitude 
                            FROM locations 
                            WHERE user = ?''', (id,)).fetchall()
        self.connection.close()
        return res

    def get_location(self, id, name):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        res = self.cursor.execute('''
                            SELECT longitude, latitude 
                            FROM locations 
                            WHERE user = ? AND name = ?''', (id, name)).fetchone()
        self.connection.close()
        return res

    def delete_user(self, id):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                            DELETE FROM users WHERE id  =  ?''',  (id,))
        self.connection.commit()
        self.connection.close()

    def delete_location(self, id, loc):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                            DELETE FROM locations WHERE name = ? AND user = ?''',  (loc, id))
        self.connection.commit()
        self.connection.close()

    def get_all_locations_of_user(self, id):
        # [(1, 55555, 1.0, 1.0, 'Paris'), (3, 55555, 3.0, 3.0, 'New York')]
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        res = self.cursor.execute('''
                            SELECT * FROM locations WHERE user = ?''', (id,)).fetchall()
        self.connection.close()
        return res

    def get_all_users(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        res = self.cursor.execute('''
                            SELECT * FROM users''').fetchall()
        self.connection.close()
        return res


db = SQL()

if __name__ == '__main__':
    db = SQL()
    # db.create_user(1393291388, False, False, None)
    # db.create_location(1393291388, 1.0, 1.0, 'Paris')
    # db.create_location(1393291388,  2.0,  2.0,  'London')
    # db.create_location(1393291388,  3.0,  3.0,   'New York')

    print(db.get_user(1393291388))
    print(db.get_location(1393291388, 'г Уфа'))
    # db.set_user_default_location(1393291388, 'Paris')
    # print(db.get_locations(1393291388))
    # print(db.get_all_locations_of_user(1))
    # print(db.get_user(1393291388))
    # print(db.get_user_default_location(1393291388))
    # db.delete_location(1393291388, 'London')
    # print(db.connection)
