import os
from dotenv import load_dotenv

load_dotenv()

def load_hmac_key():
    """
    Loads the HMAC secret key from the environment variables.
    
    Returns:
        bytes: The HMAC secret key as bytes.
    """
    key = os.getenv('HMAC_SECRET_KEY')

    if not key:
        raise ValueError("HMAC_SECRET_KEY not found in environment variables.")

    return key.encode('utf-8')