from app import create_app, db
from app.models import Role, Permission, User

app = create_app('development')

with app.app_context():
    # Create permissions
    permissions = [
        'create_todo',
        'edit_todo',
        'delete_todo',
        'view_todo',
        'manage_users',
        'manage_roles',
    ]

    permission_objs = []
    for perm_name in permissions:
        perm = Permission.query.filter_by(name=perm_name).first()
        if not perm:
            perm = Permission(name=perm_name, description=f"Permission to {perm_name.replace('_', ' ')}")
            db.session.add(perm)
        permission_objs.append(perm)

    db.session.flush()  # Ensure permissions get IDs

    # Create roles
    admin_role = Role.query.filter_by(name='Admin').first()
    if not admin_role:
        admin_role = Role(name='Admin', description='Full administrative access')

    manager_role = Role.query.filter_by(name='Manager').first()
    if not manager_role:
        manager_role = Role(name='Manager', description='Manage todos and view users')

    user_role = Role.query.filter_by(name='User').first()
    if not user_role:
        user_role = Role(name='User', description='Standard user with limited access')

    # Add roles before setting permissions to avoid SAWarning
    db.session.add_all([admin_role, manager_role, user_role])
    db.session.flush()

    # Assign permissions
    admin_role.permissions = permission_objs
    manager_role.permissions = [p for p in permission_objs if p.name in ['create_todo', 'edit_todo', 'view_todo']]
    user_role.permissions = [p for p in permission_objs if p.name in ['create_todo', 'view_todo']]

    db.session.commit()

    # Assign Admin role to your existing user for testing
    user_email = "test4@example.com"
    user = User.query.filter_by(email=user_email).first()
    if user:
        if admin_role not in user.roles:
            user.roles.append(admin_role)
            db.session.commit()
        print(f"✅ Assigned Admin role to user: {user_email}")
    else:
        print(f"⚠️ User with email {user_email} not found. Create the user first to assign roles.")

    print("✅ RBAC roles and permissions seeded successfully.")
