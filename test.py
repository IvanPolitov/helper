import sqlite3 as sql


connection = sql.connect('test.db')
cursor = connection.cursor()

cursor.execute('''
               PRAGMA foreign_keys = ON''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
                flag_daily_forecast BOOLEAN,
                flag_weekly_forecast BOOLEAN,
                default_location TEXT
                               )
                ''')


cursor.execute('''
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


cursor.execute('''
               SELECT * FROM locations WHERE user =?''',
               (111111,)
               )

r = cursor.fetchall()
print(r)


# cursor.execute('''
#     INSERT INTO users (id, flag_daily_forecast, flag_weekly_forecast, default_location) VALUES(?, ?, ?, ?) ''',
#                (111111, True, True, 'Уфа')
#                )

# cursor.execute('''
#    INSERT INTO locations (user, longitude, latitude, name) VALUES(?, ?, ?, ?)''',
#                (111111, 54.7431, 55.9678, 'Уфа')
#                )

# cursor.execute('''
#    INSERT INTO locations (user, longitude, latitude, name) VALUES(?, ?, ?, ?)''',
#                (111111, 22.7431, 22.9678, 'second')
#                )

cursor.execute('''
               SELECT * FROM locations WHERE user =?''',
               (111111,)
               )

r = cursor.fetchall()
print(r)

cursor.execute('''
               DELETE from users WHERE id =?''',
               (111111,))

cursor.execute('''
               SELECT * FROM locations WHERE user =?''',
               (111111,)
               )

r = cursor.fetchall()
print(r)

connection.commit()
connection.close()


'''
user_db = {}

user_dict_template = {
    'locations': {
        'Уфа': (54.7431, 55.9678),
        'second': (22.7431, 22.9678),
    },
    'flag_daily_forecast': False,
    'flag_weekly_forecast': False,
    'default_location': 'Уфа',
}
'''
