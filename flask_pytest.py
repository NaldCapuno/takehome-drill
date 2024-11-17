import pytest
from flask_drill_v2 import app, db, Book

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all() 
            db.session.add_all([
                Book(title="To Kill a Mockingbird", author="Harper Lee", year=1960),
                Book(title="1984", author="George Orwell", year=1949)
            ])
            db.session.commit()
        yield client

def test_get_book(client):
    response = client.get("/api/books/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["title"] == "To Kill a Mockingbird"

    response = client.get("/api/books/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Book not found"

def test_create_book(client):
    new_book = {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925}
    response = client.post("/api/books", json=new_book)
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["title"] == "The Great Gatsby"

    response = client.get("/api/books")
    assert len(response.get_json()["data"]) == 5

def test_update_book(client):
    update_data = {"title": "Brave New World", "year": 1932}
    response = client.put("/api/books/1", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["title"] == "Brave New World"
    assert data["data"]["year"] == 1932

    response = client.put("/api/books/999", json=update_data)
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Book not found"

def test_delete_book(client):
    response = client.delete("/api/books/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Book deleted successfully"

    response = client.get("/api/books")
    assert len(response.get_json()["data"]) == 8

    response = client.delete("/api/books/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Book not found"

def test_not_found_error(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Resource not found"
