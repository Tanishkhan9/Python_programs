#code to create a unique secret key
import secrets

def generate_secret_key(length: int = 32) -> str:
    """
    Generate a random secret key for API authentication or JWT signing.
    
    Args:
        length (int): The number of bytes for the key. Default is 32 (256 bits).
        
    Returns:
        str: A securely generated hexadecimal secret key.
    """
    return secrets.token_hex(length)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(f"Your generated secret key:\n{secret_key}")
