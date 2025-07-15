from flask import Flask
from flask_bcrypt import Bcrypt

# Create Flask app and Bcrypt instance
app = Flask(__name__)
bcrypt = Bcrypt(app)

# Plain password to hash and test
plain_password = "testpassword"

# Generate hash
hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')
print("Hashed password:", hashed_password)

# Check password (correct)
if bcrypt.check_password_hash(hashed_password, plain_password):
    print("✅ Password matches.")
else:
    print("❌ Password does NOT match.")

# Check password (wrong)
if bcrypt.check_password_hash(hashed_password, "wrongpassword"):
    print("❌ Wrong password matched (should NOT happen).")
else:
    print("✅ Wrong password does NOT match (correct).")
