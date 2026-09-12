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

class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: str
    note_text: str
    created_at: datetime

class TicketDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: str
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str
    status: str
    notes: list[NoteResponse]
    created_at: datetime
    updated_at: datetime

class TicketListResponse(BaseModel):
    ticket_id: str
    customer_name: str
    subject: str
    status:str
    created_at: datetime