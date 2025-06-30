from flask import Flask, request, jsonify, render_template
from twilio.rest import Client
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB upload limit
from flask import send_from_directory


# Twilio Credentials
TWILIO_SID = 'AC6ab203e14c95d74b68686f1dc3769ddb'
TWILIO_AUTH_TOKEN = '9ac20e7e95a57ebe4e9bff23d76d3bde'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'
TO_WHATSAPP_NUMBER = 'whatsapp:+918639975947'

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Cloudinary Configuration
cloudinary.config(
    cloud_name='dndlmtrgx',               # ✅ Your Cloudinary cloud name
    api_key='874266556119923',    # 🔐 Replace with your actual API key
    api_secret='CWhw4X1Gtr4xQKBAHlJo3Tpauds'  # 🔐 Replace with your actual secret
)

# Homepage Route (Optional)

@app.route('/')
def home():
    return render_template('create.html')

# Handle Issue Submission
@app.route('/submit_issue', methods=['POST'])
def submit_issue():
    try:
        data = request.get_json()

        category = data.get('issue_type')
        description = data.get('description')
        lat = data.get('latitude')
        lng = data.get('longitude')
        address = data.get('address')
        photo_url = data.get('image_url')

        coords = f"{lat}, {lng}"

        # Compose WhatsApp message
        message_body = (
            f"🚨 *New Issue Reported*\n\n"
            f"*Category:* {category}\n"
            f"*Location:* {address or coords}\n"
            f"*Description:* {description}"
        )

        msg_data = {
            'body': message_body,
            'from_': TWILIO_WHATSAPP_NUMBER,
            'to': TO_WHATSAPP_NUMBER
        }

        if photo_url:
            msg_data['media_url'] = [photo_url]

        client.messages.create(**msg_data)

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print('❌ Error:', e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
