"""
Email service using Python's built-in smtplib.
No extra packages needed.
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config


def _send(to_email, subject, html_body):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = config.SMTP_USER
        msg["To"]      = to_email
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.sendmail(config.SMTP_USER, to_email, msg.as_string())
        return True, "sent"
    except Exception as e:
        print(f"[MAIL ERROR] to={to_email} | {e}")
        return False, str(e)


# ── 1. Employee confirmation: ticket raised ───────────────────────────────────

def notify_employee_raised(ticket):
    """Email employee confirming their ticket was received."""
    subject = f"🎫 Ticket Raised Successfully — {ticket['id']}"
    html = f"""
    <div style="font-family:Segoe UI,sans-serif;max-width:600px;margin:auto;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1)">
      <div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:28px 32px">
        <h2 style="color:#fff;margin:0;font-size:1.4rem">🎫 Your Ticket Has Been Raised</h2>
        <p style="color:rgba(255,255,255,0.85);margin:6px 0 0;font-size:14px">AI Ticket System — IT Support</p>
      </div>
      <div style="background:#fff;padding:28px 32px;border:1px solid #e8eaf6;border-top:none">
        <p style="color:#333;font-size:15px;margin:0 0 20px">
          Hi <strong>{ticket['employee_name']}</strong>, your support ticket has been received and is being reviewed by the IT team.
        </p>
        <table style="width:100%;border-collapse:collapse;margin-bottom:20px;background:#f8f9ff;border-radius:10px;overflow:hidden">
          <tr style="border-bottom:1px solid #e8eaf6">
            <td style="padding:12px 16px;color:#888;font-size:13px;font-weight:600;width:130px">Ticket ID</td>
            <td style="padding:12px 16px;font-weight:700;color:#5c6bc0;font-size:15px">{ticket['id']}</td>
          </tr>
          <tr style="border-bottom:1px solid #e8eaf6">
            <td style="padding:12px 16px;color:#888;font-size:13px;font-weight:600">Status</td>
            <td style="padding:12px 16px"><span style="background:#fef3c7;color:#92400e;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700">🟡 OPEN</span></td>
          </tr>
          <tr>
            <td style="padding:12px 16px;color:#888;font-size:13px;font-weight:600">Raised At</td>
            <td style="padding:12px 16px;color:#333;font-size:13px">{ticket['created_at']}</td>
          </tr>
        </table>

        <div style="background:#fff8f0;border-left:4px solid #f59e0b;padding:14px 18px;border-radius:0 8px 8px 0;margin-bottom:20px">
          <p style="font-size:12px;color:#92400e;font-weight:700;margin:0 0 6px;text-transform:uppercase;letter-spacing:0.5px">Your Issue</p>
          <p style="color:#333;margin:0;line-height:1.6;font-size:14px">{ticket['issue']}</p>
        </div>

        <div style="background:#f0fdf4;border-left:4px solid #22c55e;padding:14px 18px;border-radius:0 8px 8px 0;margin-bottom:20px">
          <p style="font-size:12px;color:#166534;font-weight:700;margin:0 0 6px;text-transform:uppercase;letter-spacing:0.5px">💡 AI Suggested Solution</p>
          <pre style="color:#1a2e1a;font-family:Segoe UI,sans-serif;white-space:pre-wrap;margin:0;line-height:1.7;font-size:14px">{ticket['solution']}</pre>
        </div>

        <p style="color:#666;font-size:13px;margin:0;line-height:1.6">
          The IT admin has also been notified. You will receive another email once your ticket is resolved.<br/>
          Please keep your ticket ID <strong>{ticket['id']}</strong> for reference.
        </p>
      </div>
      <div style="padding:14px 32px;background:#f8f9ff;font-size:12px;color:#aaa;text-align:center">
        This is an automated message from AI Ticket System. Do not reply to this email.
      </div>
    </div>
    """
    return _send(ticket["employee_email"], subject, html)


# ── 2. Admin notification: new ticket ────────────────────────────────────────

def notify_admin_new_ticket(ticket):
    """Email admin with full ticket details + AI solution."""
    subject = f"🎫 New Ticket {ticket['id']} from {ticket['employee_name']}"
    html = f"""
    <div style="font-family:Segoe UI,sans-serif;max-width:600px;margin:auto;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1)">
      <div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:28px 32px">
        <h2 style="color:#fff;margin:0;font-size:1.4rem">🎫 New Support Ticket Received</h2>
        <p style="color:rgba(255,255,255,0.85);margin:6px 0 0;font-size:14px">Action required — please review and resolve</p>
      </div>
      <div style="background:#fff;padding:28px 32px;border:1px solid #e8eaf6;border-top:none">
        <table style="width:100%;border-collapse:collapse;margin-bottom:20px;background:#f8f9ff;border-radius:10px;overflow:hidden">
          <tr style="border-bottom:1px solid #e8eaf6">
            <td style="padding:12px 16px;color:#888;font-size:13px;font-weight:600;width:130px">Ticket ID</td>
            <td style="padding:12px 16px;font-weight:700;color:#5c6bc0;font-size:15px">{ticket['id']}</td>
          </tr>
          <tr style="border-bottom:1px solid #e8eaf6">
            <td style="padding:12px 16px;color:#888;font-size:13px;font-weight:600">Employee</td>
            <td style="padding:12px 16px;color:#333;font-size:14px">{ticket['employee_name']}</td>
          </tr>
          <tr style="border-bottom:1px solid #e8eaf6">
            <td style="padding:12px 16px;color:#888;font-size:13px;font-weight:600">Email</td>
            <td style="padding:12px 16px;color:#333;font-size:14px">{ticket['employee_email']}</td>
          </tr>
          <tr>
            <td style="padding:12px 16px;color:#888;font-size:13px;font-weight:600">Raised At</td>
            <td style="padding:12px 16px;color:#333;font-size:13px">{ticket['created_at']}</td>
          </tr>
        </table>

        <div style="background:#fff8f0;border-left:4px solid #f59e0b;padding:14px 18px;border-radius:0 8px 8px 0;margin-bottom:20px">
          <p style="font-size:12px;color:#92400e;font-weight:700;margin:0 0 6px;text-transform:uppercase;letter-spacing:0.5px">Issue Reported by Employee</p>
          <p style="color:#333;margin:0;line-height:1.6;font-size:14px">{ticket['issue']}</p>
        </div>

        <div style="background:#f0fdf4;border-left:4px solid #22c55e;padding:14px 18px;border-radius:0 8px 8px 0;margin-bottom:24px">
          <p style="font-size:12px;color:#166534;font-weight:700;margin:0 0 6px;text-transform:uppercase;letter-spacing:0.5px">💡 AI Suggested Solution (Auto-Generated)</p>
          <pre style="color:#1a2e1a;font-family:Segoe UI,sans-serif;white-space:pre-wrap;margin:0;line-height:1.7;font-size:14px">{ticket['solution']}</pre>
        </div>

        <a href="http://localhost:5000/admin"
           style="display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:13px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:14px">
          Open Admin Dashboard to Resolve →
        </a>
      </div>
      <div style="padding:14px 32px;background:#f8f9ff;font-size:12px;color:#aaa;text-align:center">
        This is an automated message from AI Ticket System. Do not reply to this email.
      </div>
    </div>
    """
    return _send(config.ADMIN_EMAIL, subject, html)


# ── 3. Employee notification: ticket resolved ─────────────────────────────────

def notify_employee_resolved(ticket):
    """Email employee that their ticket has been resolved."""
    subject = f"✅ Your Ticket {ticket['id']} Has Been Resolved"
    html = f"""
    <div style="font-family:Segoe UI,sans-serif;max-width:600px;margin:auto;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1)">
      <div style="background:linear-gradient(135deg,#22c55e,#16a34a);padding:28px 32px">
        <h2 style="color:#fff;margin:0;font-size:1.4rem">✅ Your Ticket Has Been Resolved</h2>
        <p style="color:rgba(255,255,255,0.85);margin:6px 0 0;font-size:14px">Your issue has been fixed by the IT team</p>
      </div>
      <div style="background:#fff;padding:28px 32px;border:1px solid #e8eaf6;border-top:none">
        <p style="color:#333;font-size:15px;margin:0 0 20px">
          Hi <strong>{ticket['employee_name']}</strong>, great news! Your support ticket has been resolved by the IT team.
        </p>
        <table style="width:100%;border-collapse:collapse;margin-bottom:20px;background:#f8f9ff;border-radius:10px;overflow:hidden">
          <tr style="border-bottom:1px solid #e8eaf6">
            <td style="padding:12px 16px;color:#888;font-size:13px;font-weight:600;width:130px">Ticket ID</td>
            <td style="padding:12px 16px;font-weight:700;color:#5c6bc0;font-size:15px">{ticket['id']}</td>
          </tr>
          <tr style="border-bottom:1px solid #e8eaf6">
            <td style="padding:12px 16px;color:#888;font-size:13px;font-weight:600">Status</td>
            <td style="padding:12px 16px"><span style="background:#dcfce7;color:#166534;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700">✅ RESOLVED</span></td>
          </tr>
          <tr>
            <td style="padding:12px 16px;color:#888;font-size:13px;font-weight:600">Resolved At</td>
            <td style="padding:12px 16px;color:#333;font-size:13px">{ticket['resolved_at']}</td>
          </tr>
        </table>

        <div style="background:#fff8f0;border-left:4px solid #f59e0b;padding:14px 18px;border-radius:0 8px 8px 0;margin-bottom:20px">
          <p style="font-size:12px;color:#92400e;font-weight:700;margin:0 0 6px;text-transform:uppercase;letter-spacing:0.5px">Your Issue</p>
          <p style="color:#333;margin:0;line-height:1.6;font-size:14px">{ticket['issue']}</p>
        </div>

        <div style="background:#f0fdf4;border-left:4px solid #22c55e;padding:14px 18px;border-radius:0 8px 8px 0;margin-bottom:20px">
          <p style="font-size:12px;color:#166534;font-weight:700;margin:0 0 6px;text-transform:uppercase;letter-spacing:0.5px">💡 Solution Applied</p>
          <pre style="color:#1a2e1a;font-family:Segoe UI,sans-serif;white-space:pre-wrap;margin:0;line-height:1.7;font-size:14px">{ticket['solution']}</pre>
        </div>

        <p style="color:#666;font-size:13px;margin:0;line-height:1.6">
          If you still experience issues, please raise a new ticket. We're always here to help!
        </p>
      </div>
      <div style="padding:14px 32px;background:#f8f9ff;font-size:12px;color:#aaa;text-align:center">
        This is an automated message from AI Ticket System. Do not reply to this email.
      </div>
    </div>
    """
    return _send(ticket["employee_email"], subject, html)
