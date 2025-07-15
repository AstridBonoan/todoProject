from app import create_app, db
from app.models import User
from app.extensions import bcrypt  # Import bcrypt from your extensions

# Create Flask app context
app = create_app('development')
app.app_context().push()

# Email and password to check
email_to_check = "test4@example.com"
password_to_check = "testpassword"  # Replace with the password you want to verify

# Query user from database
user = User.query.filter_by(email=email_to_check).first()

if user:
    print("Stored password hash:", user.password_hash)
    if user.password_hash and bcrypt.check_password_hash(user.password_hash, password_to_check):
        print("✅ Password matches.")
    else:
        print("❌ Password does NOT match.")
else:
    print("User not found.")
