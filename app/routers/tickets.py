from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ticket
from app.schemas import TicketCreate, TicketCreatedResponse

router = APIRouter(
    prefix="/api/tickets",
    tags=["Tickets"],
)

@router.post("",response_model=TicketCreatedResponse, status_code=status.HTTP_201_CREATED,)
def createticket(ticketdata: TicketCreate, db: Session = Depends(get_db)):
    ticket = Ticket(
        ticket_id = "TEMP",
        customer_name = ticketdata.customer_name,
        customer_email= ticketdata.customer_email,
        subject= ticketdata.subject,
        description= ticketdata.description,
        status="open",
    )

    db.add(ticket)
    db.flush()

    ticket.ticket_id = f"TKT-{ticket.id:03d}"

    db.commit()
    db.refresh(ticket)

    return ticket