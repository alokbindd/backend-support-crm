from fastapi import FastAPI
from app.database import Base, engine
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Support CRM API",
    description="Customer Support Ticketing CRM API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "Support CRM API is running"}