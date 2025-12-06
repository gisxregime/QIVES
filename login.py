from auth import verify_user, create_user


def signup():
    print("\n=== SIGN UP ===")
    username = input("Username: ").strip()
    if not username:
        print("Username required.")
        return None, None
    password = input("Password: ").strip()
    if not password:
        print("Password required.")
        return None, None
    uid = create_user(username, password)
    if uid:
        return uid, username
    return None, None

def login():
    print("\n=== LOG IN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    uid = verify_user(username, password)
    if uid:
        return uid, username
    print("Invalid credentials.")
    return None, None