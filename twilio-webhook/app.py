"""
Twilio Webhook Server for LiveKit SIP Integration
Forwards incoming phone calls from Twilio to LiveKit voice agents
"""

import os
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Dial
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get LiveKit SIP URI from environment variable
LIVEKIT_SIP_URI = os.getenv('LIVEKIT_SIP_URI', 'sip:your-trunk@sip.livekit.cloud')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Railway"""
    return {'status': 'healthy', 'service': 'twilio-webhook'}, 200


@app.route('/voice', methods=['POST'])
def voice_webhook():
    """
    Twilio webhook for incoming calls
    Forwards the call to LiveKit SIP endpoint
    """
    # Get call information from Twilio
    from_number = request.form.get('From', 'Unknown')
    to_number = request.form.get('To', 'Unknown')
    call_sid = request.form.get('CallSid', 'Unknown')

    logger.info(f"Incoming call: {from_number} → {to_number} (CallSid: {call_sid})")

    # Create TwiML response
    response = VoiceResponse()

    # Forward call to LiveKit SIP endpoint
    dial = Dial()
    dial.sip(LIVEKIT_SIP_URI)
    response.append(dial)

    logger.info(f"Forwarding call to LiveKit: {LIVEKIT_SIP_URI}")

    return Response(str(response), mimetype='text/xml')


@app.route('/voice/status', methods=['POST'])
def voice_status():
    """
    Twilio webhook for call status updates
    Logs call completion and duration
    """
    call_sid = request.form.get('CallSid', 'Unknown')
    call_status = request.form.get('CallStatus', 'Unknown')
    call_duration = request.form.get('CallDuration', '0')

    logger.info(f"Call status update - SID: {call_sid}, Status: {call_status}, Duration: {call_duration}s")

    return Response('OK', mimetype='text/plain')


@app.route('/', methods=['GET'])
def index():
    """Root endpoint - shows service info"""
    return {
        'service': 'Twilio → LiveKit Webhook',
        'status': 'running',
        'livekit_sip_uri': LIVEKIT_SIP_URI,
        'endpoints': {
            'health': '/health',
            'voice': '/voice (POST)',
            'status': '/voice/status (POST)'
        }
    }, 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
