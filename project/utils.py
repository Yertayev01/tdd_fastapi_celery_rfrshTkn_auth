import uuid
import os
import bcrypt  # Import the bcrypt library

# Initialize the password context with bcrypt
# Note: You don't need to specify "deprecated" as it's not used with bcrypt
pwd_context = bcrypt

async def hash_password(password: str):
    """
    Hashes a password using the initialized password context.

    Args:
    - password (str): The plain-text password to hash.

    Returns:
    - str: The hashed password string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

async def verify_password(plain_password, hashed_password):
    """
    Verifies a plain-text password against a hashed password string.

    Args:
    - plain_password (str): The plain-text password to verify.
    - hashed_password (str): The hashed password string to compare against.

    Returns:
    - bool: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

async def save_photo(photo):
    file_location = f"static/{str(uuid.uuid4())}.{str(photo.filename).split('.')[-1]}"
    with open(file_location, "wb+") as file_object:
        file_object.write(photo.file.read())
    
    return os.path.join("/api", file_location)
