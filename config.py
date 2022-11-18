import os

from dotenv import load_dotenv

load_dotenv()

def fetch_client_id():
    return os.environ.get('CLIENT_ID')
