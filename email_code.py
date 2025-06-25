import imaplib
import email
from email.header import decode_header

def get_recent_emails(username, password, num=5, imap_server='imap.gmail.com'):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    mail.select("inbox")

    status, data = mail.search(None, "ALL")
    mail_ids = data[0].split()
    recent_ids = reversed(mail_ids[-num:])

    email_list = []

    for mail_id in recent_ids:
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # Decode subject
        subject, _ = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(errors="ignore")

        # Extract plain text body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_dispo = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_dispo:
                    try:
                        body = part.get_payload(decode=True).decode(errors="ignore")
                    except:
                        body = "(Could not decode body)"
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        email_list.append({
            "from": msg.get("From"),
            "subject": subject,
            "date": msg.get("Date"),
            "text": body.strip()
        })

    mail.logout()
    return email_list
