from app import create_app, db
from app.models import User
from app.extensions import bcrypt

app = create_app('development')
app.app_context().push()

email_to_update = "test4@example.com"
new_password = "testpassword"  # The password you want to set

user = User.query.filter_by(email=email_to_update).first()

if not user:
    print(f"User with email {email_to_update} not found.")
else:
    user.set_password(new_password)
    db.session.commit()
    print(f"✅ Password for {email_to_update} updated to '{new_password}'")
