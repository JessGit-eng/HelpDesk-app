from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
from datetime import date
from pathlib import Path
from typing import Literal
from ai_triage import triage_ticket 

app = FastAPI()
ATTACHMENTS_DIR = Path("attachments")
ATTACHMENTS_DIR.mkdir(exist_ok=True)

app.add_middleware(
    CORSMiddleware,
   allow_origins=[
    "http://127.0.0.1:5501",
    "http://localhost:5501",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#tickets = []

def get_db_connection():
    conn = sqlite3.connect("helpdesk.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            Priority TEXT,
            Date_Created DATE,
            Team TEXT,
            Date_Resolved DATE,
            attachment_filename TEXT,
            attachment_media_type TEXT,
            status TEXT NOT NULL DEFAULT 'open'
        )
    """)

    columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(tickets)").fetchall()
    }
    for column, definition in {
        "attachment_filename": "TEXT",
        "attachment_media_type": "TEXT",
    }.items():
        if column not in columns:
            conn.execute(f"ALTER TABLE tickets ADD COLUMN {column} {definition}")

    conn.commit()
    conn.close()

create_table()


@app.get("/tickets")
def get_tickets():

    conn = get_db_connection()

    rows = conn.execute(
        "SELECT * FROM tickets"
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):

    conn = get_db_connection()

    row = conn.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    ).fetchone()

    conn.close()

    return dict(row)
      
@app.post("/tickets")
async def create_ticket(
    title: str = Form(..., min_length=5, max_length=100),
    description: str = Form(...),
    category: str = Form(...),
    attachment: UploadFile | None = File(default=None)
):
    attachment_filename = None
    attachment_media_type = None

    if attachment and attachment.filename:
        if not attachment.content_type or not attachment.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image attachments are supported")

        attachment_data = await attachment.read()
        if len(attachment_data) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Attachment must be 10 MB or smaller")

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO tickets (
            title, description, category, Date_Created,
            attachment_filename, attachment_media_type
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            category,
            date.today().isoformat(),
            attachment_filename,
            attachment_media_type
        )
    )

    conn.commit()

    ticket_id = cursor.lastrowid

    if attachment and attachment.filename:
        extension = Path(attachment.filename).suffix.lower() or ".img"
        attachment_filename = f"ticket-{ticket_id}{extension}"
        attachment_media_type = attachment.content_type
        (ATTACHMENTS_DIR / attachment_filename).write_bytes(attachment_data)
        conn.execute(
            """
            UPDATE tickets
            SET attachment_filename = ?, attachment_media_type = ?
            WHERE id = ?
            """,
            (attachment_filename, attachment_media_type, ticket_id)
        )
        conn.commit()

    conn.close()

    return {
        "message": "Ticket created",
        "id": ticket_id,
        "attachment": attachment_filename
    }


@app.get("/tickets/{ticket_id}/attachment")
def download_attachment(ticket_id: int):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT attachment_filename, attachment_media_type FROM tickets WHERE id = ?",
        (ticket_id,)
    ).fetchone()
    conn.close()

    if not row or not row["attachment_filename"]:
        raise HTTPException(status_code=404, detail="Attachment not found")

    attachment_path = ATTACHMENTS_DIR / row["attachment_filename"]
    if not attachment_path.is_file():
        raise HTTPException(status_code=404, detail="Attachment file not found")

    return FileResponse(
        attachment_path,
        media_type=row["attachment_media_type"],
        filename=row["attachment_filename"],
        content_disposition_type="attachment"
    )


@app.post("/tickets/{ticket_id}/triage")
def triage_existing_ticket(ticket_id: int):

    conn = get_db_connection()

    row = conn.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    ).fetchone()

    conn.close()

    ticket = dict(row)

    recommendation = triage_ticket(
        ticket["title"],
        ticket["description"],
        ticket["category"]
    )

    lines = recommendation.splitlines()

    priority = ""
    confidence = ""
    reason = ""

    for line in lines:
        if line.startswith("Priority:"):
            priority = line.replace("Priority:", "").strip()

        elif line.startswith("Confidence:"):
            confidence = line.replace("Confidence:", "").strip()

        elif line.startswith("Reason:"):
            reason = line.replace("Reason:", "").strip()

    return {
        "priority": priority,
        "confidence": confidence,
        "reason": reason
    }

class PriorityUpdate(BaseModel):
    priority: str


class StatusUpdate(BaseModel):
    status: Literal["open", "in progress", "resolved"]


@app.put("/tickets/{ticket_id}/priority")
def update_priority(ticket_id: int, update: PriorityUpdate):

    print("Updating ticket:", ticket_id)
    print("New priority:", update.priority)

    conn = get_db_connection()

    cursor = conn.execute(
        """
        UPDATE tickets
        SET Priority = ?
        WHERE id = ?
        """,
        (
            update.priority,
            ticket_id
        )
    )

    conn.commit()

    print("Rows updated:", cursor.rowcount)

    conn.close()

    return {
        "message": "Priority updated",
        "ticket_id": ticket_id,
        "priority": update.priority
    }


@app.put("/tickets/{ticket_id}/status")
def update_status(ticket_id: int, update: StatusUpdate):

    resolved_date = date.today().isoformat() if update.status == "resolved" else None

    conn = get_db_connection()

    cursor = conn.execute(
        """
        UPDATE tickets
        SET status = ?, Date_Resolved = ?
        WHERE id = ?
        """,
        (
            update.status,
            resolved_date,
            ticket_id
        )
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {
        "message": "Status updated",
        "ticket_id": ticket_id,
        "status": update.status,
        "Date_Resolved": resolved_date
    }
