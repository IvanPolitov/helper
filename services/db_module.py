import sqlite3


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
                id INTEGER PRIMARY KEY,
                user INTEGER ,
                longitude FLOAT ,
                latitude FLOAT ,
                name TEXT,
               CONSTRAINT fk_user
                FOREIGN KEY (user)
               REFERENCES users(id) ON DELETE CASCADE
                )
                ''')

    def create_user(self, id, flag_daily_forecast, flag_weekly_forecast, default_location):
        self.cursor.execute('''
                            INSERT INTO users (id, flag_daily_forecast, flag_weekly_forecast, default_location) VALUES (?,?,?,?)''',
                            (id, flag_daily_forecast, flag_weekly_forecast, default_location,))
        self.connection.commit()

    def create_location(self, id, user, longitude, latitude, name):
        self.cursor.execute('''
                            INSERT INTO locations  (id, user, longitude, latitude, name) VALUES  (?,?,?,?,?)''',
                            (id, user, longitude, latitude, name,))
        self.connection.commit()

    def get_user(self, id):
        self.cursor.execute('''
                            SELECT * FROM users WHERE id = ?''', (id,))
        return self.cursor.fetchone()

    def get_location(self, id):
        self.cursor.execute('''
                            SELECT * FROM locations WHERE id = ?''', (id,))
        return self.cursor.fetchone()

    def delete_user(self, id):
        self.cursor.execute('''
                            DELETE FROM users WHERE id  =  ?''',  (id,))
        self.connection.commit()

    def delete_location(self, id):
        self.cursor.execute('''
                            DELETE FROM locations WHERE id  =  ?''',  (id,))
        self.connection.commit()

    def get_all_locations_of_user(self, id):
        self.cursor.execute('''
                            SELECT * FROM locations WHERE user = ?''', (id,))
        return self.cursor.fetchall()

    def get_all_users(self):
        self.cursor.execute('''
                            SELECT * FROM users''')
        return self.cursor.fetchall()


db = SQL()

if __name__ == '__main__':
    db = SQL()
    db.create_user(1, True, True, 'Paris')
    db.create_location(1, 1, 1.0, 1.0, 'Paris')
    db.create_location(2,  1,  2.0,  2.0,  'London')
    db.create_location(3,  1,  3.0,  3.0,   'New York')

    print(db.get_user(1))
    print(db.get_location(1))
    print(db.get_all_locations_of_user(1))

    # db.delete_user(1)
    print(db.connection)
