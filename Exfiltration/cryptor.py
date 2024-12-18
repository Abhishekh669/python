from Cryptodome.Cipher import AES, PKCS1_OAEP  # Import AES and PKCS1_OAEP encryption schemes
from Cryptodome.PublicKey import RSA  # Import RSA key generation and handling
from Cryptodome.Random import get_random_bytes  # Import function to generate secure random bytes
from io import BytesIO  # Import BytesIO for handling byte streams in memory
import base64  # Base64 encoding and decoding for easier storage and transmission of binary data
import zlib  # Compression and decompression of data
import os  # Operating system interface for file handling (checking if files exist)

def generate():
    new_key = RSA.generate(4096)  # Generate a new RSA key pair (4096 bits for strong security)
    private_key = new_key.exportKey()  # Export the private key for storage
    public_key = new_key.public_key().exportKey()  # Export the public key for storage
    
    with open('key.pri', 'wb') as f:  # Open a file to store the private key in binary mode
        f.write(private_key)  # Write the private key to 'key.pri'
    
    with open('key.pub', 'wb') as f:  # Open a file to store the public key in binary mode
        f.write(public_key)  # Write the public key to 'key.pub'
    
    print("RSA key pair generated successfully.")  # Notify the user that the key generation was successful

def get_rsa_cipher(keytype):
    with open(f'key.{keytype}', 'rb') as f:  # Open the corresponding key file ('key.pub' or 'key.pri') in binary mode
        key = f.read()  # Read the key data from the file
    rsakey = RSA.importKey(key)  # Import the RSA key so it can be used for encryption or decryption
    return (PKCS1_OAEP.new(rsakey), rsakey.size_in_bytes())  # Return an RSA cipher object using OAEP padding, and the key size

def encrypt(plaintext):
    compressed_text = zlib.compress(plaintext)  # Compress the plaintext using zlib to reduce the size of the data
    session_key = get_random_bytes(16)  # Generate a random 16-byte session key for AES encryption
    cipher_aes = AES.new(session_key, AES.MODE_EAX)  # Create a new AES cipher object in EAX mode (provides encryption and integrity)
    ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_text)  # Encrypt the compressed data and generate an authentication tag
    
    cipher_rsa, _ = get_rsa_cipher('pub')  # Get the RSA cipher using the public key for encrypting the session key
    encrypted_session_key = cipher_rsa.encrypt(session_key)  # Encrypt the AES session key using RSA
    
    msg_payload = encrypted_session_key + cipher_aes.nonce + tag + ciphertext  # Combine the encrypted session key, AES nonce, tag, and ciphertext into a single payload
    encrypted = base64.encodebytes(msg_payload)  # Encode the entire payload in Base64 for easier transmission/storage
    return encrypted  # Return the Base64-encoded encrypted data

def decrypt(encrypted):
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted))  # Decode the Base64-encoded data and load it into a BytesIO stream for easier reading
    cipher_rsa, keysize_in_bytes = get_rsa_cipher('pri')  # Get the RSA cipher using the private key for decrypting the session key

    encrypted_session_key = encrypted_bytes.read(keysize_in_bytes)  # Read the encrypted session key from the byte stream
    nonce = encrypted_bytes.read(16)  # Read the AES nonce from the byte stream (used during encryption)
    tag = encrypted_bytes.read(16)  # Read the authentication tag from the byte stream (used for data integrity)
    ciphertext = encrypted_bytes.read()  # Read the remaining bytes (the AES-encrypted ciphertext)

    session_key = cipher_rsa.decrypt(encrypted_session_key)  # Decrypt the AES session key using RSA
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)  # Recreate the AES cipher object with the decrypted session key and nonce
    decrypted = cipher_aes.decrypt_and_verify(ciphertext, tag)  # Decrypt the ciphertext and verify its integrity using the authentication tag

    plaintext = zlib.decompress(decrypted)  # Decompress the decrypted data to retrieve the original plaintext
    return plaintext  # Return the decrypted and decompressed plaintext

if __name__ == '__main__':
    # Check if the RSA key files exist, generate new keys if they don't
    if not os.path.exists('key.pri') or not os.path.exists('key.pub'):
        print("Key files not found, generating new keys...")  # Inform the user that key files are missing and will be generated
        generate()  # Generate the RSA key pair
    
    plaintext = b'hey there you.'  # Define the plaintext message to be encrypted (as a byte string)
    encrypted_message = encrypt(plaintext)  # Encrypt the plaintext message
    print("Encrypted:", encrypted_message)  # Output the encrypted message

    decrypted_message = decrypt(encrypted_message)  # Decrypt the encrypted message
    print("Decrypted:", decrypted_message)  # Output the decrypted (original) message
