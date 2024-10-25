from models import User, Role

users_db = {
    "cs_user": User("cs_user", "pass123", Role.CUSTOMER_SERVICE),
    "scs_user": User("scs_user", "pass456", Role.SENIOR_CUSTOMER_SERVICE),
}

def login(username, password):
    user = users_db.get(username)
    if user and user.verify_password(password):
        print(f"Logged in as {user.username} with role {user.role}")
        return user
    else:
        print("Invalid credentials.")
        return None

def has_access(user, required_role):
    return user.role == required_role
