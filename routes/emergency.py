import json
from flask import Flask, render_template, request, jsonify
from services.emergency_service import EmergencyService

app = Flask(__name__)

# Firebase configuration (ensure this matches your setup)
FIREBASE_CONFIG = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_PROJECT.firebaseapp.com",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_PROJECT.appspot.com",
    "messagingSenderId": "YOUR_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

# 1. Page Route: Renders emergency HTML view
@app.route('/emergency')
def emergency_page():
    try:
        # Pass firebase config safely as a JSON string
        firebase_config_json = json.dumps(FIREBASE_CONFIG)
        return render_template('emergency.html', firebase_config_json=firebase_config_json)
    except Exception as e:
        print(f"[ERROR] /emergency route failed: {e}")
        return f"Server Error rendering page: {str(e)}", 500

# 2. API Endpoint: Triggers SOS via EmergencyService
@app.route('/api/sos', methods=['POST'])
def trigger_sos():
    try:
        data = request.get_json() or {}
        
        # Validate required input safely
        uid = data.get('uid', 'anonymous')
        patient_name = data.get('patient_name', 'Unknown')
        phone = data.get('phone', '')
        latitude = data.get('latitude', 0.0)
        longitude = data.get('longitude', 0.0)
        emergency_type = data.get('emergency_type', 'Medical General')

        # Generate SOS payload using EmergencyService
        sos_payload = EmergencyService.create_emergency_sos(
            uid=uid,
            patient_name=patient_name,
            phone=phone,
            latitude=latitude,
            longitude=longitude,
            emergency_type=emergency_type
        )

        return jsonify({"status": "success", "data": sos_payload}), 200

    except Exception as e:
        print(f"[ERROR] /api/sos failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500