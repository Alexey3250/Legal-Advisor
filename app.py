import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Load the keys.env file
load_dotenv("keys.env")

# Access the keys
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

client = Client(account_sid, auth_token)

app = Flask(__name__)

def handle_incoming_message(message):
    # Replace the following line with the actual code to get the answer using your model
    answer = "Hello, Alex!"
    return answer



@app.route('/whatsapp', methods=['POST'])
def receive_message():
    message = request.form.get('Body')
    from_number = request.form.get('From')
    to_number = request.form.get('To')

    if message:
        response = handle_incoming_message(message)

        # Send the response using Twilio API
        twilio_message = client.messages.create(
            body=response,
            from_=to_number,
            to=from_number
        )
        print(f"Sent message with SID: {twilio_message.sid}")
        return ('', 204)
    else:
        return ('', 204)

@app.route("/status_callback", methods=["POST"])
def status_callback():
    message_sid = request.values.get("MessageSid", "")
    message_status = request.values.get("MessageStatus", "")

    print(f"Message SID: {message_sid} | Status: {message_status}")

    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
