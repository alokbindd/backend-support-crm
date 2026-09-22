from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import tickets
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Support CRM API",
    description="Customer Support Ticketing CRM API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tickets.router)

@app.get("/")
def root():
    return {"message": "Support CRM API is running"}