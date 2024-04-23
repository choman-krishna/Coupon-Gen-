import random
import string

def generate_random_otp(length=6):
    # Define characters to choose from
    characters = string.ascii_letters + string.digits
    
    # Generate OTP
    otp = ''.join(random.choice(characters) for _ in range(length))
    
    return otp

# Generate and print a random OTP
otp = generate_random_otp()
