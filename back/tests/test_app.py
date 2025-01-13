import pytest
from back.ebookgenV1.app.app import app
from back.ebookgenV1.data.db_connection import mongodb
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test_clients"  # Use a test DB
    with app.test_client() as client:
        with app.app_context():
            # Clear and setup test DB
            mongo.db.users.delete_many({})
            mongo.db.generated_books.delete_many({})
        yield client


def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "Backend is !"


def test_register(client):
    response = client.post("/register", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully"}

    # Try registering with the same email
    response = client.post("/register", json={"email": "test@example.com", "password": "newpassword"})
    assert response.status_code == 409
    assert response.json == {"error": "Email already exists"}


def test_login(client):
    # First, register a user
    client.post("/register", json={"email": "test@example.com", "password": "password123"})

    # Correct credentials
    response = client.post("/login", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json["message"] == "Login successful"

    # Incorrect password
    response = client.post("/login", json={"email": "test@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json["error"] == "Invalid credentials"


def test_preview_cover(client, mocker):
    # Mock the `add_text_to_image_and_return_path` function
    mocker.patch("app.add_text_to_image_and_return_path", return_value="path/to/preview.png")
    response = client.post("/preview_cover", json={"title": "Test Book", "gender": "male"})
    assert response.status_code == 200


@patch("stripe.checkout.Session.create")
def test_create_checkout_session(mock_stripe, client):
    # Mock Stripe response
    mock_stripe.return_value = MagicMock(url="http://stripe-checkout-url", id="session_id")
    response = client.post("/create-checkout-session")
    assert response.status_code == 200
    assert response.json["url"] == "http://stripe-checkout-url"


@patch("stripe.Webhook.construct_event")
def test_stripe_webhook(mock_stripe_event, client, mocker):
    mock_stripe_event.return_value = {"type": "checkout.session.completed", "data": {"object": {"id": "session_id"}}}
    mocker.patch("app.handle_generate_book", return_value="generated_book_path")

    response = client.post("/webhook", json={"title": "Test Book"})
    assert response.status_code == 200


def test_check_book_ready(client):
    # Insert a dummy book record
    mongo.db.generated_books.insert_one({"book_id": "test_session", "status": "ready", "file_path": "path/to/book"})
    response = client.get("/check_book_ready/test_session")
    assert response.status_code == 200
    assert response.json["ready"] is True


def test_download_book(client):
    # Insert a dummy book record
    mongo.db.generated_books.insert_one({"book_id": "test_book", "status": "ready", "file_path": "path/to/book"})
    response = client.get("/download_book/test_book")
    assert response.status_code == 404  # Mock the file system for proper file testing
