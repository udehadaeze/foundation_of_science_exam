from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Database URI
db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publication_year = db.Column(db.Integer)

# Initialize database
@app.before_first_request
def addcontext():
    with app.app_context():
        db.create_all()  # Create tables if not exist

# Route for displaying book list
@app.route('/books')
def books():
    books = Book.query.all()  # Get all books from database
    return render_template('books.html', books=books)

# Route for adding a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']

        new_book = Book(title=title, author=author, publication_year=publication_year)
        db.session.add(new_book)  # Add new book to database
        db.session.commit()  # Save changes

        return redirect('/')  # Redirect to main page

    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)
