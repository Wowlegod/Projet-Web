import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def get_db():
    db = sqlite3.connect('transport.sqlite')
    db.row_factory = sqlite3.Row
    return db

def new_user(username, password):
    db = get_db()
    if db.execute('SELECT id FROM User WHERE username = ?', (username,)).fetchone():
        return False
        
    hashed_password = generate_password_hash(password)
    db.execute('INSERT INTO User (username, password) VALUES (?, ?)', (username, hashed_password))
    db.commit()
    return True

def login_user(username, password):
    db = get_db()
    user = db.execute("SELECT * FROM User WHERE username = ?", (username,)).fetchone()
    
    if user and check_password_hash(user['password'], password):
        return {'id': user['id'], 'username': user['username']}
    return None

def search_entities(query):
    db = get_db()
    return db.execute(
        "SELECT * FROM Cities WHERE city_name LIKE ?", 
        ('%' + query + '%',)
    ).fetchall()

def get_city_details(city_id):
    db = get_db()
    return db.execute("SELECT * FROM Cities WHERE id = ?", (city_id,)).fetchone()

def get_favorites(user_id):
    db = get_db()
    return db.execute("""
        SELECT Cities.* FROM Cities 
        JOIN Favorites ON Cities.id = Favorites.city_id 
        WHERE Favorites.user_id = ?
    """, (user_id,)).fetchall()

def add_favorite(user_id, city_id):
    db = get_db()
    db.execute("INSERT INTO Favorites (user_id, city_id) VALUES (?, ?)", (user_id, city_id))
    db.commit()

def remove_favorite(user_id, city_id):
    db = get_db()
    db.execute("DELETE FROM Favorites WHERE user_id = ? AND city_id = ?", (user_id, city_id))
    db.commit()