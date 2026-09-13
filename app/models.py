from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    ticket_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    customer_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    customer_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status_id: Mapped[int] = mapped_column(
        ForeignKey('ticket_statuses.id'),
        nullable=False,
    )

    status: Mapped["Ticketstatus"] = relationship(
        "Ticketstatus",
        back_populates="tickets",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    notes: Mapped[list["Note"]] = relationship(
        "Note",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )

class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    ticket_id: Mapped[str] = mapped_column(
        ForeignKey("tickets.ticket_id"),
        nullable=False,
        index=True,
    )

    note_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    ticket: Mapped["Ticket"] = relationship(
        "Ticket",
        back_populates="notes",
    )

class Ticketstatus(Base):
    __tablename__ = "ticket_statuses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="status",
    )