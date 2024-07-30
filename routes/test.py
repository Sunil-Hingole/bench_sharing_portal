from werkzeug.security import generate_password_hash, check_password_hash

# Step 1: Hash the password
password = '1234'
hashed_password = generate_password_hash(password, method='scrypt')
print(f"Generated hash: {hashed_password}")

# Step 2: Verify the password
result = check_password_hash(hashed_password, password)
print(f"Password verification result: {result}")
