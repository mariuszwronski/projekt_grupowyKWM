from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dane do logowania - symulacja
users = {'admin': 'admin123', 'user': 'user123'}

# Dane książek - symulacja
books = [
    {'title': 'W pustyni i w puszczy', 'author': 'Henryk Sienkiewicz'},
    {'title': 'Pan Tadeusz', 'author': 'Adam Mickiewicz'},
    {'title': 'Harry Potter i Kamień Filozoficzny', 'author': 'J.K. Rowling'},
    # Dodaj więcej książek według potrzeb
]

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
    return render_template('search.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
