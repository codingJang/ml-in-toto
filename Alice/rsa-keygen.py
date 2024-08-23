from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

# Define the directory where you want to save the keys
directory = "./Elenor"
private_key_filename = 'elenor'
public_key_filename = 'elenor.pub'

# Ensure the directory exists
os.makedirs(directory, exist_ok=True)

# Generate an RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Serialize the private key to PEM format
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Save the private key to a file
private_key_path = os.path.join(directory, private_key_filename)
with open(private_key_path, "wb") as private_key_file:
    private_key_file.write(private_key_pem)

# Generate the corresponding public key
public_key = private_key.public_key()

# Serialize the public key to PEM format
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save the public key to a file
public_key_path = os.path.join(directory, public_key_filename)
with open(public_key_path, "wb") as public_key_file:
    public_key_file.write(public_key_pem)

print(f"Private key saved to: {private_key_path}")
print(f"Public key saved to: {public_key_path}")
