from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Ścieżka do bazy SQLite
app.secret_key = 'secret_key'  # Sekretne klucz używane do flash messages
db = SQLAlchemy(app)

# Definicja modelu Książki
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.String(20), nullable=True)  # Dodanie kolumny release_date


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
        flash('Błędna nazwa użytkownika lub hasło', 'error')
        return redirect(url_for('index'))

@app.route('/search')
def search():
    books = Book.query.all()  # Pobieranie wszystkich książek z bazy danych
    return render_template('search.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    release_date = request.form['release_date']

    if not title or not author or not release_date:
        flash('Wypełnij wszystkie pola', 'error')
        return redirect(url_for('search'))

    # Tworzenie nowej książki i dodawanie jej do bazy danych
    new_book = Book(title=title, author=author, release_date=release_date)
    db.session.add(new_book)
    db.session.commit()

    flash('Książka dodana pomyślnie', 'success')
    return redirect(url_for('search'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
