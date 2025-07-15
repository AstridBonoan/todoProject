import bcrypt

password = b"testpassword"

# Generate a salt and hash the password
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print("Hashed password:", hashed.decode())

# Verify password
if bcrypt.checkpw(password, hashed):
    print("Password matches.")
else:
    print("Password does NOT match.")
