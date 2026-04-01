"""
Simple JSON-based ticket database.
No external DB needed — pure Python.
"""
import json
import os
import uuid
from datetime import datetime

DB_FILE = "tickets_db.json"


def _load():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_ticket(employee_name, employee_email, issue, solution):
    """Create a new ticket and return it."""
    db = _load()
    ticket_id = "TKT-" + str(uuid.uuid4())[:8].upper()
    ticket = {
        "id": ticket_id,
        "employee_name": employee_name,
        "employee_email": employee_email,
        "issue": issue,
        "solution": solution,
        "status": "open",          # open | resolved
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resolved_at": None,
    }
    db[ticket_id] = ticket
    _save(db)
    return ticket


def get_all_tickets():
    """Return all tickets sorted newest first."""
    db = _load()
    tickets = list(db.values())
    tickets.sort(key=lambda t: t["created_at"], reverse=True)
    return tickets


def get_ticket(ticket_id):
    db = _load()
    return db.get(ticket_id)


def resolve_ticket(ticket_id):
    """Mark a ticket as resolved. Returns updated ticket or None."""
    db = _load()
    if ticket_id not in db:
        return None
    db[ticket_id]["status"] = "resolved"
    db[ticket_id]["resolved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _save(db)
    return db[ticket_id]
