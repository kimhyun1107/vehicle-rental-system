# src/main.py

from typing import Optional, Union
from models import Customer, Admin
import auth
import customer_ops
import booking_ops
import admin_ops
from utils import clear_screen, pause


def main_menu() -> Optional[Union[Customer, Admin]]:
    """Hiển thị Main Menu (Đơn giản hóa)"""
    print("--- HỆ THỐNG THUÊ XE (VEHICLE RENTAL SYSTEM) ---")
    print("1. Đăng nhập")
    print("2. Đăng ký")
    print("0. Thoát") 
    choice = input("Nhập lựa chọn của bạn: ").strip()
    
    if choice == '1':
        return auth.login() 
    elif choice == '2':
        auth.register() 
        return None
    elif choice == '0':
        print("Cảm ơn đã sử dụng hệ thống!")
        exit(0)
    else:
        print("[LỖI] Lựa chọn không hợp lệ.")
        return None


def customer_menu(customer: Customer) -> None:
    """Hiển thị Customer Menu (Gộp nhóm chức năng)"""
    while True:
        clear_screen()
        print(f"--- MENU KHÁCH HÀNG (Xin chào, {customer.name}) ---")
        print("1. Xem danh sách & Thuê xe") 
        print("2. Xem lịch sử & Hủy booking") 
        print("0. Đăng xuất")
        choice = input("Nhập lựa chọn của bạn: ").strip()

        if choice == '1':
            clear_screen()
            vehicles = customer_ops.view_vehicle_list()
            if vehicles:
                vehicle_to_rent = customer_ops.view_vehicle_details(vehicles)
                if vehicle_to_rent:
                    confirm = input("\nBạn có muốn thuê xe này? (Y/N): ").strip().upper()
                    if confirm == 'Y':
                        booking_ops.rent_vehicle(customer, vehicle_to_rent)
            pause()

        elif choice == '2':
            clear_screen()
            bookings = customer_ops.view_booking_history(customer)
            if bookings:
                confirm = input("\nBạn có muốn hủy booking nào không? (Y/N): ").strip().upper()
                if confirm == 'Y':
                    booking_ops.cancel_booking(customer, bookings)
            pause()
            
        elif choice == '0':
            print("Đã đăng xuất.")
            break
        else:
            print("[LỖI] Lựa chọn không hợp lệ.")
            pause()


def admin_menu(admin: Admin) -> None:
    """Hiển thị Admin Menu"""
    while True:
        clear_screen()
        print(f"--- MENU ADMIN (Xin chào, {admin.name}) ---")
        print("1. Quản lý xe") 
        print("2. Quản lý người dùng") 
        print("3. Xem tất cả booking") 
        print("0. Đăng xuất") 
        choice = input("Nhập lựa chọn của bạn: ").strip()

        if choice == '1':
            clear_screen()
            admin_ops.manage_vehicles(admin.userID)
            pause()
        elif choice == '2':
            clear_screen()
            admin_ops.manage_users()
            pause()
        elif choice == '3':
            clear_screen()
            admin_ops.view_all_bookings()
            pause()
        elif choice == '0':
            print("Đã đăng xuất.")
            break
        else:
            print("[LỖI] Lựa chọn không hợp lệ.")
            pause()


def main():
    """Luồng chạy chính của ứng dụng"""
    current_user: Optional[Union[Customer, Admin]] = None
    
    while True:
        clear_screen()
        if current_user is None:
            current_user = main_menu()
            pause()
        elif current_user.role == 'Customer':
            customer_menu(customer=current_user)
            current_user = None 
            pause()
        elif current_user.role == 'Admin':
            admin_menu(admin=current_user)
            current_user = None 
            pause()


if __name__ == "__main__":
    main()