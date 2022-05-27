from cryptography.fernet import Fernet


# Function to encrypt Password
def encrypt_password(password):
    password = password.encode()
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(password)
    return cipher_text, key


# Function to decrypt password
def decrypt_password(cipher_text, key):
    cipher_suite = Fernet(key)
    unciphered_text = (cipher_suite.decrypt(cipher_text))
    return unciphered_text


