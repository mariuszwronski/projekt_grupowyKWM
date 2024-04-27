from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Ścieżka do bazy SQLite
db = SQLAlchemy(app)

# Definicja modelu Książki
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

# Dane do logowania - symulacja
users = {'admin': 'admin123', 'user': 'user123'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        return redirect(url_for('search'))
    else:
        return 'Błędna nazwa użytkownika lub hasło'

@app.route('/search')
def search():
    books = Book.query.all()  # Pobieranie wszystkich książek z bazy danych
    return render_template('search.html', books=books)


    # Tworzenie tabeli książek w bazie danych, jeśli nie istnieje
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

