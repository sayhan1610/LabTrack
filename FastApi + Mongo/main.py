from fastapi import FastAPI
from routes.route import route # Import the router from routes/route.py

app = FastAPI()

app.include_router(route)