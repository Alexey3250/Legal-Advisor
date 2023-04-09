# Import the required libraries
from app import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import docsearch
import chain

app = Flask(__name__)

# Define a route to handle incoming messages from Twilio
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    # Get the incoming message text
    incoming_msg = request.values.get("Body", "").strip()

    # Perform similarity search and generate an answer
    docs = docsearch.similarity_search(incoming_msg)
    answer = chain.run(input_documents=docs, question=incoming_msg)

    # Create a Twilio MessagingResponse object to send the answer
    response = MessagingResponse()
    response.message(answer)

    return str(response)

if __name__ == "__main__":
    app.run()
