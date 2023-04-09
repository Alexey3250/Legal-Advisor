
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv
import os
from twilio.rest import Client

# Load the keys.env file
load_dotenv("keys.env")

# Access the keys
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")


client = Client(account_sid, auth_token)

message = client.conversations \
                .v1 \
                .conversations('CHcabdeb29214d42d495ab438954a22d98') \
                .messages \
                .create(author='system', body='')

print(message.sid)
