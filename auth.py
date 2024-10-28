from models import User, Role

users_db = {
    "cs_user": User("cs_user", "cs", Role.CUSTOMER_SERVICE),
    "scs_user": User("scs_user", "scs", Role.SENIOR_CUSTOMER_SERVICE),
    "fm_user": User("fm_user", "fm", Role.FINANCIAL_MANAGER),
    "am_user": User("am_user", "am", Role.ADMINISTRATIVE_MANAGER),
    "pm_user": User("pm_user", "pm", Role.PRODUCTION_MANAGER),
    "team_user": User("team_user", "team", Role.TEAM_MEMBER)
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
