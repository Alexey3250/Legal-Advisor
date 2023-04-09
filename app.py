import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

from gpt4_handler import setup_gpt4_handler, get_gpt4_response # Import the functions from gpt4_handler.py

# Load the keys.env file
load_dotenv("keys.env")

# Access the keys
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

client = Client(account_sid, auth_token)

app = Flask(__name__)

# Set up GPT-4 handler
docsearch, chain = setup_gpt4_handler()

@app.route('/whatsapp', methods=['POST'])
def receive_message():
    message = request.form.get('Body')  # Change this line
    print(f"Received message: {message}")

    if message:
        # Generate GPT-4 response
        gpt4_response = get_gpt4_response(message, docsearch, chain)
        print(f"GPT-4 response: {gpt4_response}")

        # Send GPT-4 response via WhatsApp
        response = f"GPT-4 says: {gpt4_response}"
        twilio_message = client.messages.create(
            body=response,
            from_='whatsapp:+14155238886',  # Replace with your Twilio phone number
            to='whatsapp:+971527846185'  # Replace with the recipient's phone number
        )
        print(twilio_message.sid)
    else:
        response = "Hello, no message received."

    return response


@app.route("/status_callback", methods=["POST"])
def status_callback():
    message_sid = request.values.get("MessageSid", "")
    message_status = request.values.get("MessageStatus", "")

    print(f"Message SID: {message_sid} | Status: {message_status}")

    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
