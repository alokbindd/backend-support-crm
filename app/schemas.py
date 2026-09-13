from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from enum import Enum

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

    @field_validator("status",mode="before")
    @classmethod
    def get_status_display_name(cls, value):
        return value.display_name

class TicketListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: str
    customer_name: str
    subject: str
    status:str
    created_at: datetime

    @field_validator("status",mode="before")
    @classmethod
    def get_status_display_name(cls, value):
        return value.display_name

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class TicketUpdate(BaseModel):
    status: TicketStatus
    notes: str | None=None

class TicketUpdateResponse(BaseModel):
    success: bool
    updated_at: datetime
