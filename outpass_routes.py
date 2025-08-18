from flask import Blueprint, request, jsonify
from services.firebase_service import db 
from services.email_service import send_qr_email 
from firebase_admin import firestore

outpass_bp = Blueprint('outpass_routes', __name__)

# Create Outpass Request
@outpass_bp.route('/create_outpass', methods=['POST'])
def create_outpass():
    data = request.json
    try:
        outpass_ref = db.collection('outpasses').document(data['outpassId'])
        outpass_ref.set({
            "studentName": data['studentName'],
            "type": data['type'],
            "validFrom": data['validFrom'],
            "validUntil": data['validUntil'],
            "status": "PendingFaculty",
            "scans": []
        })
        return jsonify({"message": "Outpass request created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Approve Outpass (Faculty/Warden)
@outpass_bp.route('/approve_outpass/<outpass_id>', methods=['POST'])
def approve_outpass(outpass_id):
    try:
        outpass_ref = db.collection('outpasses').document(outpass_id)
        outpass_data = outpass_ref.get().to_dict()

        if not outpass_data:
            return jsonify({"error": "Outpass not found"}), 404

        # Update status to approved
        outpass_ref.update({"status": "Approved"})
        qr_data = {
            "outpassId": outpass_id,
            "studentName": outpass_data['studentName'],
            "type": outpass_data['type'],
            "validFrom": outpass_data['validFrom'],
            "validUntil": outpass_data['validUntil'],
            "approvedBy": "Faculty/Warden"
        }
        send_qr_email(outpass_data['email'], qr_data)
        
        return jsonify({"message": "Outpass approved and QR sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
