from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

@app.route("/api/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    books_list = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year
        } for book in books
    ]
    return jsonify(
        {
            "success": True, 
            "data": books_list, 
            "total": len(books_list)
        }
    ), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)

    if book is None:
        return jsonify(
            {
                "success": False, 
                "error": "Book not found"
            }
        ), HTTPStatus.NOT_FOUND

    return jsonify(
        {
            "success": True, 
            "data": {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "year": book.year
            }
        }
    ), HTTPStatus.OK

@app.route("/api/books", methods=["POST"])
def create_book():
    pass

@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    pass

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    pass

@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {
            "success": False, 
            "error": "Resource not found"
        }
    ), HTTPStatus.NOT_FOUND

@app.errorhandler(500)
def internal_error(error):
    return jsonify(
        {
            "success": False, 
            "error": "Internal Server Error"
        }
    ), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == "__main__":
    app.run(debug=True)
