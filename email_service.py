import smtplib
from email.message import EmailMessage
import qrcode
from io import BytesIO
import base64

def generate_qr_code(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def send_qr_email(email, qr_data):
    try:
        qr_code_base64 = generate_qr_code(str(qr_data))
        msg = EmailMessage()
        msg['Subject'] = "Your Approved Outpass QR Code"
        msg['From'] = "your-email@example.com"
        msg['To'] = email

        # Email body with QR code embedded
        msg.set_content(f"""
        Your outpass has been approved.
        Details:
        - Student: {qr_data['studentName']}
        - Type: {qr_data['type']}
        - Valid From: {qr_data['validFrom']}
        - Valid Until: {qr_data['validUntil']}
        
        Attached is your QR Code for security verification.
        """)
        
        # Attach QR Code
        qr_attachment = BytesIO(base64.b64decode(qr_code_base64))
        msg.add_attachment(qr_attachment.read(), maintype='image', subtype='png', filename='outpass_qr.png')

        # Email Configuration
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("your-email@example.com", "your-email-password")
            server.send_message(msg)

        print("Email Sent Successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
