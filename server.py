from flask import Flask, render_template, request, redirect, session
import data_model as model
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b'6dbb6b3863634aa6a72270de16df48e666f2564fddcc5fe3c27effe4393a7f4b'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = model.search_entities(query)
    return render_template('search_result.html', results=results, query=query)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if model.new_user(username, password):
            return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')
        user = model.login_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            return redirect('/')
        return render_template('login.html', error="Identifiants incorrects")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/')

@app.route('/city/<int:city_id>')
def city_details(city_id):
    city = model.get_city_details(city_id)
    return render_template('city_details.html', city=city)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    favorites = model.get_favorites(session['user_id'])
    return render_template('user_profile.html', favorites=favorites)

@app.route('/add-favorite', methods=['POST'])
def add_favorite():
    if 'user_id' in session:
        city_id = request.form.get('city_id')
        model.add_favorite(session['user_id'], city_id)
    return redirect('/profile')

@app.route('/remove-favorite', methods=['POST'])
def remove_favorite():
    if 'user_id' in session:
        city_id = request.form.get('city_id')
        model.remove_favorite(session['user_id'], city_id)
    return redirect('/profile')

@app.route('/marseille')
def marseille():
    city  = model.get_city_details(3) 
    return render_template('Marseille.html', city = city)
    
if __name__ == '__main__':
    app.run(debug=True, port=3000)

