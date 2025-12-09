from typing import Optional, Union
from models import Customer, Admin
import auth
import customer_ops
import booking_ops
import admin_ops
from utils import clear_screen, pause


def main_menu() -> Optional[Union[Customer, Admin]]:
    print(" VEHICLE RENTAL SYSTEM ")
    print("1. Login")
    print("2. Register")
    print("0. Exit")
    choice = input("Enter your choice: ").strip()
    
    if choice == '1':
        return auth.login()
    elif choice == '2':
        auth.register()
        return None
    elif choice == '0':
        print("Thank you for using the system!")
        exit(0)
    else:
        print("Invalid choice.")
        return None


def customer_menu(customer: Customer) -> None:
    while True:
        clear_screen()
        print(f"--- CUSTOMER MENU (Welcome, {customer.name}) ---")
        print("1. View vehicle list & Rent a vehicle")
        print("2. View booking history & Cancel booking")
        print("0. Logout")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            clear_screen()
            vehicles = customer_ops.view_vehicle_list()
            if vehicles:
                vehicle_to_rent = customer_ops.view_vehicle_details(vehicles)
                if vehicle_to_rent:
                    confirm = input("\nDo you want to rent this vehicle? (Y/N): ").strip().upper()
                    if confirm == 'Y':
                        booking_ops.rent_vehicle(customer, vehicle_to_rent)
            pause()

        elif choice == '2':
            clear_screen()
            bookings = customer_ops.view_booking_history(customer)
            if bookings:
                confirm = input("\nWould you like to cancel any booking? (Y/N): ").strip().upper()
                if confirm == 'Y':
                    booking_ops.cancel_booking(customer, bookings)
            pause()
            
        elif choice == '0':
            print("Logged out.")
            break
        else:
            print("[ERROR] Invalid choice.")
            pause()


def admin_menu(admin: Admin) -> None:
    while True:
        clear_screen()
        print(f"--- ADMIN MENU (Welcome, {admin.name}) ---")
        print("1. Manage vehicles")
        print("2. Manage users")
        print("3. View all bookings")
        print("0. Logout")
        choice = input("Enter your choice: ").strip()

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
            print("Logged out.")
            break
        else:
            print("[ERROR] Invalid choice.")
            pause()


def main():
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
