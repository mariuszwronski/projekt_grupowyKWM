from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Ścieżka do bazy SQLite
db = SQLAlchemy(app)

# Definicja modelu Książki
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.String(20), nullable=True)
    borrowed = db.Column(db.Boolean, default=False)
    borrowed_by = db.Column(db.String(100), nullable=True)



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

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    release_date = request.form['release_date']

    # Tworzenie nowej książki i dodawanie jej do bazy danych
    new_book = Book(title=title, author=author, release_date=release_date)
    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('search'))

@app.route('/borrow_book/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    book = Book.query.get(book_id)
    if book:
        if not book.borrowed:
            # Ustawienie flagi wypożyczenia i nazwy użytkownika, który wypożyczył książkę
            book.borrowed = True
            book.borrowed_by = request.form['borrower']
            db.session.commit()
            return redirect(url_for('search'))
        else:
            return 'Książka jest już wypożyczona'
    else:
        return 'Nie znaleziono książki'


if _name_ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
