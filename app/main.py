from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import tickets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Support CRM API",
    description="Customer Support Ticketing CRM API",
    version="1.0.0",
)

app.include_router(tickets.router)

@app.get("/")
def root():
    return {"message": "Support CRM API is running"}