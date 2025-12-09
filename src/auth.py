import hashlib
from typing import Optional, Union
from models import Customer, Admin
import data_manager as dm
from utils import get_next_id


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register() -> None:
    print("\n Register Account ")

    name = input("Enter full name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone number: ").strip()
    password = input("Enter password: ").strip()
    re_password = input("Re-enter password: ").strip()

    if password != re_password:
        print("(Error) Passwords do not match.")
        return

    users_data = dm.load_data(dm.USERS_FILE)
    for user in users_data:
        if user['email'] == email:
            print("(Error) Email is already in use.")
            return

    next_id = get_next_id(users_data, 'userID')
    new_customer = Customer(
        userID=next_id,
        name=name,
        email=email,
        password=hash_password(password),
        phoneNumber=phone,
        bookingHistory=[],
        status='Active',
        role='Customer'
    )

    users_data.append(dm.serialize(new_customer))
    dm.save_data(dm.USERS_FILE, users_data)

    print("✓ Registration successful!")


def login() -> Optional[Union[Customer, Admin]]:
    print("\n Login")

    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    users_data = dm.load_data(dm.USERS_FILE)
    hashed_pw = hash_password(password)

    for user_data in users_data:
        if user_data['email'] == email and user_data['password'] == hashed_pw:
            user_obj = dm.deserialize_user(user_data)
            print(f"✓ Login successful! Welcome {user_obj.name}.")
            return user_obj

    print("[ERROR] Incorrect email or password.")
    return None
