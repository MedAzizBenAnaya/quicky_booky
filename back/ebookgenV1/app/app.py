from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

import asyncio
import stripe
import os
from typing import Optional
import assembler

# App and Configuration
app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client.clients
users_collection = db.users
generated_books_collection = db.generated_books

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.secret_key = 'sauce'

stripe.api_key = os.getenv('STRIPE_API_KEY')
webhook_secret = os.getenv('WEBHOOK_SECRET')

preview_pic_path = 'refactoredImg/new.png'
BOOKS_DIR = os.path.join(os.getcwd(), 'generated_books')
os.makedirs(BOOKS_DIR, exist_ok=True)

data = {}


# Helper Functions
def generate_book(title, topic, gender, age, additional_info):
    return asyncio.run(make_ebook(title, topic, "english", age, gender, additional_info, 5, 3))


def add_text_to_image_and_return_path(title, gender):
    add_text_to_image(RESIZED_COVER_PATH, title, gender)
    return preview_pic_path


async def handle_generate_book(session_id, title, topic, gender, age, additional_info):
    try:
        file_path = generate_book(title, topic, gender, age, additional_info)
        generated_books_collection.update_one(
            {'book_id': session_id},
            {'$set': {'status': 'ready', 'file_path': file_path}},
            upsert=True
        )
    except Exception as e:
        generated_books_collection.update_one(
            {'book_id': session_id},
            {'$set': {'status': 'failed'}},
            upsert=True
        )
        raise e


# Routes
@app.get("/")
async def hello_world():
    return {"message": "Backend is running!"}


@app.post("/register")
async def register(email: str, password: str):
    if users_collection.find_one({'email': email}):
        raise HTTPException(status_code=409, detail="Email already exists")
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({'email': email, 'password': hashed_password})
    return {"message": "User registered successfully"}


@app.post("/login")
async def login(email: str, password: str):
    user = users_collection.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        return {"message": "Login successful", "user": {"email": email}}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/dashboard")
async def working():
    return {"message": "working"}


@app.post("/preview_cover")
async def preview_cover(request: Request):
    global data
    data = await request.json()
    title = data.get('title', '')
    gender = data.get('gender', '')
    preview_cover_path = add_text_to_image_and_return_path(title, gender)
    return FileResponse(preview_cover_path, media_type="image/png")


@app.post("/create-checkout-session")
async def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': 'price_1OzqlRKbOuLLxEKZJx2q0pcL',
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"http://localhost:3000?paymentSuccess=true",
            cancel_url=f"http://localhost:3000?paymentCanceled=true",
            automatic_tax={'enabled': True},
        )
        return {"url": checkout_session.url, "id": checkout_session.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        title = data.get('title', '')
        topic = data.get('topic', '')
        gender = data.get('gender', '')
        age = data.get('age', '')
        additional_info = data.get('additionalInfo', '')

        await handle_generate_book(session['id'], title, topic, gender, age, additional_info)

    return {"message": "Success"}


@app.get("/check_book_ready/{session_id}")
async def check_book_ready(session_id: str):
    book_record = generated_books_collection.find_one({'book_id': session_id})
    if book_record:
        return {"ready": True, "bookId": book_record['book_id']}
    return {"ready": False}, 202


@app.get("/download_book/{book_id}")
async def download_book(book_id: str):
    book_record = generated_books_collection.find_one({'book_id': book_id})
    if book_record and book_record['status'] == 'ready':
        file_path = book_record['file_path']
        return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='application/pdf')
    raise HTTPException(status_code=404, detail="Book not found or isn't ready yet")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
