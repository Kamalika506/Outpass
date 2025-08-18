from flask import Flask, request, jsonify
import qrcode
import base64
from io import BytesIO
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Function to generate QR code
def generate_qr_code(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{qr_data}"

# Route to approve outpass and generate QR code
@app.route('/outpass/approve_outpass/<outpass_id>', methods=['POST'])
def approve_outpass(outpass_id):
    qr_code = generate_qr_code(f"Outpass ID: {outpass_id}")
    return jsonify({'qrCode': qr_code})

# Route to send email with QR code
@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    email = data.get('email')
    qr_code = data.get('qrCodeData')

    try:
        msg = EmailMessage()
        msg['Subject'] = 'Your Approved Outpass QR Code'
        msg['From'] = 'your-email@gmail.com'
        msg['To'] = email
        msg.set_content(f"Here is your QR code for the approved outpass.\n\n{qr_code}")

        # Gmail SMTP settings
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('your-email@gmail.com', 'your-email-password')
            smtp.send_message(msg)

        return jsonify({'message': 'Email sent successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
