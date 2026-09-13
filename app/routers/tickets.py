from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ticket, Note, Ticketstatus
from app.schemas import TicketCreate, TicketCreatedResponse, TicketListResponse, TicketDetailResponse, TicketUpdate, TicketUpdateResponse
from typing import Optional
from sqlalchemy import or_

router = APIRouter(
    prefix="/api/tickets",
    tags=["Tickets"],
)

@router.post("",response_model=TicketCreatedResponse, status_code=status.HTTP_201_CREATED,)
def createticket(ticketdata: TicketCreate, db: Session = Depends(get_db)):
    open_status = db.query(Ticketstatus).filter(Ticketstatus.code=='open').first()

    if not open_status:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default ticket status not configured",
        )
    
    ticket = Ticket(
        ticket_id = "TEMP",
        customer_name = ticketdata.customer_name,
        customer_email= ticketdata.customer_email,
        subject= ticketdata.subject,
        description= ticketdata.description,
        status_id=open_status.id,
    )

    db.add(ticket)
    db.flush()

    ticket.ticket_id = f"TKT-{ticket.id:03d}"

    db.commit()
    db.refresh(ticket)

    return ticket

@router.get("",response_model=list[TicketListResponse])
def get_tickets(status:Optional[str]=None, search:Optional[str] = None, db: Session = Depends(get_db)):
    query =  db.query(Ticket)

    if status:
        query = query.join(Ticketstatus).filter(Ticketstatus.code==status)

    if search:
        search_term = (f"%{search}%").lower()
        query = query.filter(
            or_(
                Ticket.customer_name.ilike(search_term),
                Ticket.ticket_id.ilike(search_term),
                Ticket.customer_email.ilike(search_term),
                Ticket.description.ilike(search_term),
            )
        )

    tickets = query.order_by(Ticket.created_at.desc()).all()

    return tickets

@router.get("/{ticket_id}",response_model=TicketDetailResponse)
def ticket_detail(ticket_id: str, db:Session = Depends(get_db)):
    ticket = (db.query(Ticket).filter(Ticket.ticket_id==ticket_id).first())

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket

@router.put('/{ticket_id}', response_model=TicketUpdateResponse)
def update_ticket(ticket_id: str, ticket_data: TicketUpdate, db: Session = Depends(get_db)):
    ticket = (db.query(Ticket).filter(Ticket.ticket_id==ticket_id).first())

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    status_record = (db.query(Ticketstatus).filter(Ticketstatus.code==ticket_data.status.value).first())
    if not status_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid ticket status"
        )

    ticket.status_id = status_record.id
    
    if ticket_data.notes:
        note = Note(
            ticket_id=ticket.ticket_id,
            note_text=ticket_data.notes,
        )

        db.add(note)

    db.commit()
    db.refresh(ticket)

    return {
        "success":True,
        "updated_at":ticket.updated_at,
    }
    