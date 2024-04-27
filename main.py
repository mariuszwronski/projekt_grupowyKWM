from flask import Flask, render_template, request, redirect, url_for, flash, session
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
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('search'))
    else:
        flash('Błędna nazwa użytkownika lub hasło', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    # Pobieranie wszystkich książek z bazy danych
    books = Book.query.all()

    # Filtrowanie książek na podstawie parametrów zapytania
    title_filter = request.args.get('title_filter')
    author_filter = request.args.get('author_filter')
    if title_filter:
        books = [book for book in books if title_filter.lower() in book.title.lower()]
    if author_filter:
        books = [book for book in books if author_filter.lower() in book.author.lower()]

    # Sortowanie książek na podstawie parametru sortowania
    sort_by = request.args.get('sort_by')
    if sort_by == 'title':
        books.sort(key=lambda x: x.title)
    elif sort_by == 'author':
        books.sort(key=lambda x: x.author)
    elif sort_by == 'release_date':
        books.sort(key=lambda x: x.release_date)

    return render_template('search.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    if 'logged_in' not in session:
        flash('Musisz być zalogowany, aby dodać książkę', 'error')
        return redirect(url_for('index'))

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

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'logged_in' not in session:
        flash('Musisz być zalogowany, aby edytować książkę', 'error')
        return redirect(url_for('index'))

    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.release_date = request.form['release_date']
        db.session.commit()
        flash('Książka zaktualizowana pomyślnie', 'success')
        return redirect(url_for('search'))

    return render_template('edit_book.html', book=book)

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 'logged_in' not in session:
        flash('Musisz być zalogowany, aby usunąć książkę', 'error')
        return redirect(url_for('index'))

    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Książka usunięta pomyślnie', 'success')
    return redirect(url_for('search'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
