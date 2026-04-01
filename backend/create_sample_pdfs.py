"""
Creates 8 sample knowledge base PDFs covering common IT issues.
Usage: python create_sample_pdfs.py
"""
import os

os.makedirs("uploads", exist_ok=True)


def make_pdf(filename, title, lines):
    content_text = f"{title}\n\n" + "\n".join(lines)
    stream_content = "BT\n/F1 12 Tf\n50 750 Td\n14 TL\n"
    for line in content_text.split('\n'):
        safe = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        stream_content += f"({safe}) Tj T*\n"
    stream_content += "ET\n"
    stream_bytes = stream_content.encode('latin-1', errors='replace')

    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
        (f"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
         f"/Contents 5 0 R /Resources << /Font << /F1 4 0 R >> >> >>\nendobj\n").encode(),
        (f"5 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n").encode()
        + stream_bytes + b"\nendstream\nendobj\n",
    ]

    pdf = b"%PDF-1.4\n"
    offsets = []
    for obj in objects:
        offsets.append(len(pdf))
        pdf += obj

    xref_offset = len(pdf)
    pdf += b"xref\n"
    pdf += f"0 {len(objects) + 1}\n".encode()
    pdf += b"0000000000 65535 f \n"
    for off in offsets:
        pdf += f"{off:010d} 00000 n \n".encode()
    pdf += b"trailer\n"
    pdf += f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode()
    pdf += b"startxref\n"
    pdf += f"{xref_offset}\n".encode()
    pdf += b"%%EOF\n"

    with open(f"uploads/{filename}", 'wb') as f:
        f.write(pdf)
    print(f"  Created: {filename}")


print("Creating knowledge base PDFs...")

make_pdf("01_password_reset.pdf", "Password Reset Issue", [
    "Keywords: password reset forgot login locked account credentials",
    "",
    "Steps to reset your password:",
    "1. Go to the company login page.",
    "2. Click the Forgot Password link below the login button.",
    "3. Enter your registered company email address.",
    "4. Check your inbox for a password reset email (check spam too).",
    "5. Click the reset link in the email within 30 minutes.",
    "6. Enter and confirm your new password.",
    "7. Log in with your new password.",
    "",
    "Common Issues:",
    "- Reset email not received: Check spam or junk folder.",
    "- Link expired: Request a new reset link from the login page.",
    "- Account locked after too many attempts: Contact IT support.",
    "- New password not accepted: Must be 8+ chars with uppercase, number, symbol.",
])

make_pdf("02_vpn_not_working.pdf", "VPN Connection Issue", [
    "Keywords: VPN not connecting vpn error vpn failed remote access network",
    "",
    "Steps to fix VPN not connecting:",
    "1. Check your internet connection is working first.",
    "2. Close and fully restart the VPN client application.",
    "3. Make sure you are entering the correct VPN username and password.",
    "4. Try connecting to a different VPN server location.",
    "5. Temporarily disable your firewall or antivirus and retry.",
    "6. Uninstall and reinstall the VPN client if issue persists.",
    "",
    "Common Errors:",
    "- Authentication failed: Reset your VPN password via IT portal.",
    "- Timeout error: Try a different server or check firewall rules.",
    "- Error 800 or 619: Check network adapter settings.",
    "- Still not working: Contact IT team with the exact error message.",
])

make_pdf("03_email_not_syncing.pdf", "Outlook Email Sync Issue", [
    "Keywords: outlook email not syncing email not loading mail stuck email error",
    "",
    "Steps to fix Outlook not syncing emails:",
    "1. Restart Outlook completely (close from taskbar too).",
    "2. Check your internet connection.",
    "3. Go to File then Account Settings and verify your account.",
    "4. Click Send and Receive All Folders (F9 shortcut).",
    "5. Clear Outlook cache: close Outlook, delete the OST file, reopen.",
    "6. Run Outlook in safe mode: press Win+R, type outlook.exe /safe",
    "",
    "Advanced Fix:",
    "- Remove and re-add your email account in Account Settings.",
    "- Repair Office: Control Panel > Programs > Microsoft Office > Repair.",
    "- Check mailbox storage quota is not full.",
    "- Contact IT if issue persists after all above steps.",
])

make_pdf("04_computer_slow.pdf", "Computer Running Slow", [
    "Keywords: computer slow laptop slow system slow performance lag freezing",
    "",
    "Steps to fix a slow computer:",
    "1. Restart your computer to clear memory and temp files.",
    "2. Close unused programs and browser tabs.",
    "3. Check Task Manager (Ctrl+Shift+Esc) for high CPU or memory usage.",
    "4. Run Disk Cleanup: search Disk Cleanup in Start menu.",
    "5. Disable startup programs: Task Manager > Startup tab.",
    "6. Check for Windows updates and install pending ones.",
    "7. Run a full antivirus scan to check for malware.",
    "",
    "If still slow:",
    "- Check if hard disk is nearly full (keep 15% free space).",
    "- Consider upgrading RAM if consistently above 90% usage.",
    "- Contact IT for hardware assessment.",
])

make_pdf("05_printer_not_working.pdf", "Printer Not Working", [
    "Keywords: printer not printing printer offline printer error cannot print",
    "",
    "Steps to fix printer issues:",
    "1. Check printer is powered on and connected (USB or network).",
    "2. Check for paper jams and clear them carefully.",
    "3. Ensure paper is loaded correctly in the tray.",
    "4. On your PC: Settings > Printers > right-click printer > Set as Default.",
    "5. Clear the print queue: Settings > Printers > Open Queue > Cancel All.",
    "6. Restart the Print Spooler: Services > Print Spooler > Restart.",
    "7. Reinstall printer driver from manufacturer website.",
    "",
    "Network Printer Issues:",
    "- Ping the printer IP to check connectivity.",
    "- Re-add the printer using its IP address.",
    "- Contact IT if printer shows offline on the network.",
])

make_pdf("06_wifi_not_connecting.pdf", "WiFi Not Connecting", [
    "Keywords: wifi not connecting no internet wireless network issue cannot connect",
    "",
    "Steps to fix WiFi issues:",
    "1. Turn WiFi off and on again on your device.",
    "2. Forget the network and reconnect: Settings > WiFi > Forget > Reconnect.",
    "3. Restart your computer.",
    "4. Restart the router or access point (unplug 30 seconds).",
    "5. Run Windows Network Troubleshooter: Settings > Network > Troubleshoot.",
    "6. Update network adapter driver via Device Manager.",
    "7. Reset network settings: open CMD as admin, run: netsh winsock reset",
    "",
    "Common Issues:",
    "- Wrong password: Verify WiFi password with IT.",
    "- IP conflict: Run ipconfig /release then ipconfig /renew in CMD.",
    "- Limited connectivity: Check DHCP server is running.",
])

make_pdf("07_software_installation.pdf", "Software Installation Issue", [
    "Keywords: software install error cannot install application setup failed",
    "",
    "Steps to fix software installation issues:",
    "1. Run the installer as Administrator: right-click > Run as administrator.",
    "2. Temporarily disable antivirus during installation.",
    "3. Check you have enough disk space (at least 2GB free).",
    "4. Download a fresh copy of the installer (file may be corrupted).",
    "5. Check Windows is up to date before installing.",
    "6. Install required prerequisites like .NET Framework or Visual C++.",
    "",
    "Common Errors:",
    "- Error 1603: Run installer as admin and check disk space.",
    "- Missing DLL: Install Visual C++ Redistributable from Microsoft.",
    "- Access denied: Check folder permissions or contact IT.",
    "- Incompatible version: Verify software supports your Windows version.",
])

make_pdf("08_account_locked.pdf", "Account Locked or Access Denied", [
    "Keywords: account locked access denied login failed cannot login blocked",
    "",
    "Steps to resolve account locked or access denied:",
    "1. Wait 15 minutes and try again (auto-unlock after failed attempts).",
    "2. Verify you are using the correct username (usually firstname.lastname).",
    "3. Check Caps Lock is not on when entering password.",
    "4. Try logging in from a different device to isolate the issue.",
    "5. Contact IT helpdesk to manually unlock your account.",
    "6. IT will verify your identity and reset access.",
    "",
    "Prevention:",
    "- Do not share your credentials with anyone.",
    "- Change password every 90 days as per company policy.",
    "- Enable account recovery options in your profile settings.",
    "- Report suspicious login attempts to IT security team immediately.",
])

print(f"\nDone! 8 PDFs created in uploads/ folder.")
print("Topics covered:")
print("  1. Password Reset")
print("  2. VPN Not Working")
print("  3. Outlook Email Sync")
print("  4. Computer Running Slow")
print("  5. Printer Not Working")
print("  6. WiFi Not Connecting")
print("  7. Software Installation")
print("  8. Account Locked / Access Denied")
