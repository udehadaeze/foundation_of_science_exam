from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publication_year = db.Column(db.Integer)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/books")
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route("/add_book", methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = int(request.form['publication_year'])

        new_book = Book(title=title, author=author, publication_year=publication_year)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books'))
    else:
        return render_template('add_book.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
