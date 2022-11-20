import os

from dotenv import load_dotenv

load_dotenv()

def fetch_client_id():
    return os.environ.get('CLIENT_ID')

def fetch_userpool_id():
    return os.environ.get('USERPOOL_ID')

def fetch_template_url():
    return os.environ.get('TEMPLATE_URL')
