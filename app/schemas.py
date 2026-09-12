from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class TicketCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str

class TicketCreatedResponse(BaseModel):
    ticket_id: str
    created_at: datetime

class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: str
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime