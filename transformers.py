import hmac
import hashlib
from config import load_hmac_key
import re
from datetime import datetime, date

def pseudonymize_client_id(client_id):
    """
    Pseudonymizes the client_id using HMAC with a secret key.
    
    Args:
        client_id (int): The original client ID to be pseudonymized.
        
    Returns:
        str: A hexadecimal string representing the pseudonymized client ID.
    """
    if client_id is None:
        return None

    key = load_hmac_key()  #load key from env variables
    #ecnodes string into bytes 
    value = str(client_id).encode('utf-8')
    digest = hmac.new(
        key,
        value,
        hashlib.sha256
    ).hexdigest()
    return "CUST_" + digest[:8]  #takes the first 12 characters of the HMAC output and adds CUST_ so obvious its referring to a customer ID 

def sanitize_name(name):
    """
    Sanitizes the name by transforming all into 'Jane Doe' to protect name privacy. Actual names provide little to no analytical value. 
    
    Args:
        name (str): The original name to be sanitized.

    Returns:
        str: "Jane Doe"
    """
    if name is None:
        return None
    return "Jane Doe"

def sanitize_email(email, client_id):
    """
    Sanitizes the email by pseudonymizing it with the client ID.
    
    Args:
        email (str): The original email to be sanitized.
        client_id (int): The client ID to use for pseudonymization.

    Returns:
        str: The pseudonymized email, keeping the domain intact. 
    """
    if email is None:
        return None

    domain = email.split('@')[-1]  #extract the domain from the original email
    pseudonym = pseudonymize_client_id(client_id)  
    return pseudonym.lower() + "@" + domain  #combine the pseudonymized client ID with the original domain to create a new email address

def sanitize_ssn(ssn):
    """
    Sanitize SSN by redaction

    Args:
        ssn (str): The original SSN to be sanitized.
    
        Returns:
        str: [REDACTED]
    """
    if ssn is None:
        return None
    return "[REDACTED]"

def mask_phone_number(phone):
    """
    Masks the last 7 digits of the phone number with astericks, keepin the area code intact 

    Args:
        phone (str): The original phone number to be masked.
    Returns:
        str: The masked phone number.
    """
    if phone is None:
        return None

    digits = re.sub(r'\D', '', phone)  #remove non-digit characters
    area_code = digits[:3]  #extract the area code

    return f"{area_code}-***-****"  #return the masked phone number with the area code intact

def dob_to_age_range(dob):
    """
    Converts date of birth to an age range.

    Args:
        dob (str): The date of birth in 'YYYY-MM-DD' format.

    Returns:
        str: The age range as a string.
    """
    if dob is None:
        return None

    birth_date = datetime.strptime(dob, "%Y-%m-%d").date() #convert into a Python date object
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    if age < 18:
        return "Under 18"
    elif 18 <= age <= 25:
        return "18-25"
    elif 26 <= age <= 35:
        return "26-35"
    elif 36 <= age <= 45:
        return "36-45"
    elif 46 <= age <= 55:
        return "46-55"
    elif 56 <= age <= 65:
        return "56-65"
    else:
        return "66+"

def generalize_zip_code(zip_code):
    """
    Generalizes the zip code to the first 3 digits.

    Args:
        zip_code (str): The original zip code to be generalized.

    Returns:
        str: The generalized zip code.
    """
    if zip_code is None:
        return None

    return zip_code[:3] + "**"  #replace the last two digits with '**' to generalize the zip code