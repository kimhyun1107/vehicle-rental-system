# src/auth.py

import hashlib
from typing import Optional, Union
from models import Customer, Admin
import data_manager as dm
from utils import get_next_id


def hash_password(password: str) -> str:
    """Hash password bằng SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def register() -> None:
    """UC Register Account - Đăng ký tài khoản Customer mới"""
    print("\n--- ĐĂNG KÝ TÀI KHOẢN ---")
    
    # Bước 2: Nhập thông tin
    name = input("Nhập họ tên: ").strip()
    email = input("Nhập email: ").strip()
    phone = input("Nhập số điện thoại: ").strip()
    password = input("Nhập mật khẩu: ").strip()
    re_password = input("Nhập lại mật khẩu: ").strip()
    
    # Bước 4: Kiểm tra mật khẩu khớp
    if password != re_password:
        print("[LỖI] Mật khẩu không khớp.")
        return
    
    # Bước 5: Kiểm tra email đã tồn tại
    users_data = dm.load_data(dm.USERS_FILE)
    for user in users_data:
        if user['email'] == email:
            print("[LỖI] Email đã được sử dụng.")
            return
    
    # Bước 6: Lưu Customer mới
    next_id = get_next_id(users_data, 'userID')
    new_customer = Customer(
        userID=next_id,
        name=name,
        email=email,
        password=hash_password(password),  # Hash password
        phoneNumber=phone,
        bookingHistory=[],
        status='Active',
        role='Customer'
    )
    
    users_data.append(dm.serialize(new_customer))
    dm.save_data(dm.USERS_FILE, users_data)
    
    # Bước 7: Thông báo thành công
    print("✓ Đăng ký thành công!")


def login() -> Optional[Union[Customer, Admin]]:
    """UC Login - Đăng nhập hệ thống"""
    print("\n--- ĐĂNG NHẬP ---")
    
    # Bước 2: Nhập thông tin
    email = input("Nhập email: ").strip()
    password = input("Nhập mật khẩu: ").strip()
    
    # Bước 4: Tìm kiếm user
    users_data = dm.load_data(dm.USERS_FILE)
    hashed_pw = hash_password(password)
    
    for user_data in users_data:
        if user_data['email'] == email and user_data['password'] == hashed_pw:
            # Kiểm tra trạng thái tài khoản
            if user_data.get('status') == 'Locked':
                print("[LỖI] Tài khoản đã bị khóa. Vui lòng liên hệ Admin.")
                return None
            
            # Bước 5: Đăng nhập thành công
            user_obj = dm.deserialize_user(user_data)
            print(f"✓ Đăng nhập thành công! Xin chào {user_obj.name}.")
            return user_obj
    
    # Alternative Flow: Thông tin sai
    print("[LỖI] Email hoặc mật khẩu không đúng.")
    return None