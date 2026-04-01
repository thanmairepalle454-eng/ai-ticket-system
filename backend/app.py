from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

from rag_service import build_index, query_rag
from db import create_ticket, get_all_tickets, get_ticket, resolve_ticket
from mailer import notify_employee_raised, notify_admin_new_ticket, notify_employee_resolved

app = Flask(__name__, static_folder=None)
CORS(app)

UPLOAD_FOLDER = "uploads"
FRONTEND_DIR  = os.path.join(os.path.dirname(__file__), "..", "frontend")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ── Serve pages ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_file(os.path.abspath(os.path.join(FRONTEND_DIR, "index.html")))

@app.route("/admin")
def admin():
    return send_file(os.path.abspath(os.path.join(FRONTEND_DIR, "admin.html")))


# ── Employee: raise ticket ────────────────────────────────────────────────────

@app.route("/api/tickets", methods=["POST"])
def api_create_ticket():
    data  = request.json or {}
    name  = data.get("name",  "").strip()
    email = data.get("email", "").strip()
    issue = data.get("issue", "").strip()

    if not name or not email or not issue:
        return jsonify({"error": "Name, email and issue are required"}), 400

    # AI reads the ticket and finds solution
    solution = query_rag(issue)

    # Save to DB
    ticket = create_ticket(name, email, issue, solution)

    # Send email to employee: ticket confirmation
    emp_ok, emp_err = notify_employee_raised(ticket)
    if not emp_ok:
        print(f"[WARN] Employee confirmation email failed: {emp_err}")

    # Send email to admin: new ticket alert with AI solution
    adm_ok, adm_err = notify_admin_new_ticket(ticket)
    if not adm_ok:
        print(f"[WARN] Admin notification email failed: {adm_err}")

    return jsonify({
        "ticket_id":        ticket["id"],
        "issue":            ticket["issue"],
        "solution":         ticket["solution"],
        "status":           ticket["status"],
        "created_at":       ticket["created_at"],
        "employee_emailed": emp_ok,
        "admin_emailed":    adm_ok,
    })


# ── Admin: list all tickets ───────────────────────────────────────────────────

@app.route("/api/admin/tickets", methods=["GET"])
def api_list_tickets():
    return jsonify(get_all_tickets())


# ── Admin: resolve a ticket ───────────────────────────────────────────────────

@app.route("/api/admin/tickets/<ticket_id>/resolve", methods=["POST"])
def api_resolve_ticket(ticket_id):
    ticket = resolve_ticket(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    # Send resolution email to employee
    ok, err = notify_employee_resolved(ticket)
    if not ok:
        print(f"[WARN] Resolution email failed: {err}")

    return jsonify({
        "ticket_id":   ticket["id"],
        "status":      ticket["status"],
        "resolved_at": ticket["resolved_at"],
        "email_sent":  ok,
    })


# ── Admin: upload knowledge PDF ───────────────────────────────────────────────

@app.route("/api/upload", methods=["POST"])
def api_upload_pdf():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    build_index()
    return jsonify({"message": f"'{file.filename}' uploaded and indexed successfully!"})


# ── Admin: list uploaded PDFs ─────────────────────────────────────────────────

@app.route("/api/admin/pdfs", methods=["GET"])
def api_list_pdfs():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(".pdf")]
    return jsonify(sorted(files))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from waitress import serve

    port = int(os.environ.get("PORT", 5000))
    print("Indexing existing PDFs...")
    build_index()
    print(f"\n✅  Employee portal : http://localhost:{port}")
    print(f"✅  Admin dashboard : http://localhost:{port}/admin\n")
    serve(app, host="0.0.0.0", port=port)
