import sqlite3
import json

def setup_and_import():
    conn = sqlite3.connect('transport.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS Favorites")
    cursor.execute("DROP TABLE IF EXISTS User")
    cursor.execute("DROP TABLE IF EXISTS Cities")
    cursor.execute("DROP TABLE IF EXISTS Country")


    cursor.execute('''
        CREATE TABLE User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE Country (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE Cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_id INTEGER,
            city_name TEXT,
            region TEXT,
            transport_type TEXT,
            official_app TEXT,
            price_range TEXT,
            tips TEXT,
            FOREIGN KEY (country_id) REFERENCES Country(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            city_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES User(id),
            FOREIGN KEY (city_id) REFERENCES Cities(id)
        )
    ''')

    with open('transport.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        region_name = item.get('region', 'PACA')
        cursor.execute("INSERT INTO Country (country_name) VALUES (?)", (region_name,))
        country_id = cursor.lastrowid
        
        for city in item.get('cities', []):
            cursor.execute('''
                INSERT INTO Cities (country_id, city_name, region, transport_type, official_app, price_range, tips)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (country_id, city['city_name'], region_name, city['transport_type'], 
                  city['official_app'], city['price_range'], city['tips']))

    conn.commit()
    conn.close()
    print("ok")

if __name__ == "__main__":
    setup_and_import()