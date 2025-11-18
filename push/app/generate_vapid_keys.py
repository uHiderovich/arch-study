from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# генерируем приватный ключ
private_key = ec.generate_private_key(ec.SECP256R1())

private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

# генерируем публичный ключ
public_key = private_key.public_key()

public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

print("VAPID_PRIVATE_KEY:")
print(private_key_pem.decode())

print("\nVAPID_PUBLIC_KEY:")
print(public_key_pem.decode())
