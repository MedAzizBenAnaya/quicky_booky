from flask import Flask, request, redirect, send_file, jsonify, session, send_from_directory
from flask_cors import CORS
from coverPageGen import add_text_to_image, RESIZED_COVER_PATH
from openai_test import make_ebook
from dotenv import load_dotenv


import os

from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

import stripe

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/clients"
app.secret_key = 'sauce'
mongo = PyMongo(app)

CORS(app)

# Ensure the path is correctly pointing to where your PDF will be saved
path_to_pdf = 'pdf/myEbook.pdf'
# path = 'myEbook.pdf'

preview_pic_path = 'refactoredImg/new.png'

BOOKS_DIR = os.path.join(app.root_path, 'generated_books')
if not os.path.exists(BOOKS_DIR):
    os.makedirs(BOOKS_DIR)


def generate_book(title, topic, gender, age, additionalInfo):
    return make_ebook(title, topic, "english", age, gender, additionalInfo)


def add_text_to_image_and_return_path(title, gender):
    add_text_to_image(RESIZED_COVER_PATH, title, gender)
    return preview_pic_path


def handle_generate_book(session_id):
    data = request.json

    title = data.get('title', '')  # Ensure key names match those used in the frontend
    topic = data.get('topic', '')
    gender = data.get('gender', '')
    age = data.get('age', '')
    additional_info = data.get('additionalInfo', '')

    try:
        file_path = generate_book(title, topic, gender, age, additional_info)

        mongo.db.generated_books.update_one(
            {'book_id': session_id},
            {'$set': {'status': 'ready', 'file_path': file_path}},
            upsert=True
        )
        print(f'successful eBook generation for session {session_id}')

    except Exception as e:
        print(f"Failed to generate eBook for session {session_id}: {e}")

        mongo.db.generated_books.update_one(
            {'book_id': session_id},
            {'$set': {'status': 'failed'}},
            upsert=True
        )

    return file_path


@app.route('/')
def hello_world():
    return 'Backend is !'


@app.route('/register', methods=['POST'])
def register():
    users = mongo.db.users  # Access the 'users' collection
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    if email and password:
        # Check if the email already exists in the database
        if users.find_one({'email': email}):
            return jsonify({"error": "Email already exists"}), 409
        else:
            hashed_password = generate_password_hash(password)
            users.insert_one({
                'email': email,
                'password': hashed_password
            })
            return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"error": "Missing email or password"}), 400


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = users.find_one({'email': email})

    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful", "user": {"email": email}}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/dashboard', methods=['GET'])
def working():
    return jsonify({"message": "working"}), 200


@app.route('/preview_cover', methods=['POST'])
def preview_cover():
    data = request.json

    title = data.get('title', '')
    gender = data.get('gender', '')
    preview_cover_path = add_text_to_image_and_return_path(title, gender)
    return send_file(preview_cover_path, mimetype='image/png')


stripe.api_key = os.getenv('STRIPE_API_KEY')

YOUR_DOMAIN = 'http://localhost:3000'


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1OzqlRKbOuLLxEKZJx2q0pcL',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '?paymentSuccess=true',
            cancel_url=YOUR_DOMAIN + '?paymentCanceled=true',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return jsonify({'url': checkout_session.url, 'id': checkout_session.id})


webhook_secret = os.getenv('WEBHOOK_SECRET')


@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        print(e)
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        print(e)
        return 'Invalid signature', 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print('Payment was successful. Session ID:', session.id)

        handle_generate_book(session.id)

    return jsonify({'message': 'Success'}), 200


@app.route('/check_book_ready/<session_id>', methods=['GET'])
def check_book_ready(session_id):
    book_record = mongo.db.generated_books.find_one({'book_id': session_id})
    if book_record:
        print("yo BRO")
        return jsonify({'ready': True, 'bookId': book_record['book_id']})
    else:
        return jsonify({'ready': False}), 202


@app.route('/download_book/<book_id>', methods=['GET'])
def download_book(book_id):
    book_record = mongo.db.generated_books.find_one({'book_id': book_id})
    if book_record and book_record['status'] == 'ready':
        path = book_record['file_path']
        print("Bruv" + path)

        return send_from_directory(directory=os.path.dirname(path),
                                   path=os.path.basename(path),
                                   as_attachment=True)
    return jsonify({'error': "Book not found or isn't ready yet"}), 404


if __name__ == '__main__':
    app.run(debug=True)
