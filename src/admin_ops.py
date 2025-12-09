from models import Vehicle, Customer
import data_manager as dm
from utils import get_next_id


def manage_vehicles(admin_id: int):
    while True:
        print("\n--- VEHICLE MANAGEMENT ---")
        print("1. Add new vehicle")
        print("2. Edit vehicle information")
        print("3. Delete vehicle")
        print("4. View all vehicles")
        print("0. Back to Admin menu")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            _add_vehicle(admin_id)
        elif choice == '2':
            _edit_vehicle()
        elif choice == '3':
            _delete_vehicle()
        elif choice == '4':
            _view_all_vehicles()
        elif choice == '0':
            break
        else:
            print("[ERROR] Invalid choice.")


def _add_vehicle(admin_id: int):
    print("--- Add new vehicle ---")
    brand = input("Enter vehicle brand: ").strip()
    model = input("Enter vehicle model: ").strip()
    license_plate = input("Enter license plate: ").strip()
    try:
        price_per_day = float(input("Enter rental price/day: "))
    except ValueError:
        print("[ERROR] Price must be a number.")
        return

    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    
    for v in vehicles_data:
        if v['license_plate'] == license_plate:
            print("[ERROR] This license plate already exists in the system.")
            return
            
    next_id = get_next_id(vehicles_data, 'vehicleID')
    new_vehicle = Vehicle(
        vehicleID=next_id,
        license_plate=license_plate,
        brand=brand,
        model=model,
        pricePerDay=price_per_day,
        status='available'
    )
    
    vehicles_data.append(dm.serialize(new_vehicle))
    dm.save_data(dm.VEHICLES_FILE, vehicles_data)
    print(f"Vehicle '{brand} {model}' added successfully.")


def _edit_vehicle():
    _view_all_vehicles() 
    try:
        vehicle_id = int(input("Enter the ID of the vehicle you want to edit: "))
    except ValueError:
        print("[ERROR] ID must be a number.")
        return
        
    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    vehicle_found = False
    for v_data in vehicles_data:
        if v_data['vehicleID'] == vehicle_id:
            print(f"Editing vehicle: {v_data['brand']} {v_data['model']}")
            try:
                new_price = input(f"New price (current {v_data['pricePerDay']}, press Enter to skip): ").strip()
                new_status = input(f"New status (current '{v_data['status']}', press Enter to skip): ").strip()
                
                if new_price:
                    v_data['pricePerDay'] = float(new_price)
                if new_status and new_status in ['available', 'rented', 'maintenance']:
                    v_data['status'] = new_status
                
                vehicle_found = True
                break
            except ValueError:
                print("[ERROR] Invalid price.")
                return

    if vehicle_found:
        dm.save_data(dm.VEHICLES_FILE, vehicles_data)
        print("Vehicle updated successfully.")
    else:
        print("[ERROR] No vehicle found with this ID.")


def _delete_vehicle():
    _view_all_vehicles() 
    try:
        vehicle_id = int(input("Enter the ID of the vehicle you want to DELETE: "))
    except ValueError:
        print("[ERROR] ID must be a number.")
        return
        
    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    vehicle_to_delete = None
    for v_data in vehicles_data:
        if v_data['vehicleID'] == vehicle_id:
            vehicle_to_delete = v_data
            break
    
    if vehicle_to_delete:
        confirm = input(f"Are you sure you want to DELETE vehicle {vehicle_to_delete['brand']} {vehicle_to_delete['model']}? (Y/N): ").strip().upper()
        if confirm == 'Y':
            vehicles_data.remove(vehicle_to_delete)
            dm.save_data(dm.VEHICLES_FILE, vehicles_data)
            print("Vehicle deleted successfully.")
        else:
            print("Delete action canceled.")
    else:
        print("[ERROR] No vehicle found with this ID.")


def _view_all_vehicles():
    print("--- All vehicles in the system ---")
    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    if not vehicles_data:
        print("No vehicles in the system.")
        return
    for v_data in vehicles_data:
        v = dm.deserialize_vehicle(v_data)
        print(f"  [ID: {v.vehicleID}] {v.brand} {v.model} ({v.license_plate}) - Status: {v.status}")


def manage_users():
    print("\n--- USER MANAGEMENT (CUSTOMER) ---")
    
    users_data = dm.load_data(dm.USERS_FILE)
    customers = [dm.deserialize_user(u) for u in users_data if u['role'] == 'Customer']
    
    if not customers:
        print("No Customer accounts found.")
        return
        
    print("Customer list:")
    for c in customers:
        print(f"  [ID: {c.userID}] {c.name} ({c.email}) - Status: {c.status}")
        
    try:
        user_id = int(input("Enter the Customer ID you want to change status: "))
    except ValueError:
        print("[ERROR] ID must be a number.")
        return
        
    user_found = False
    for u_data in users_data:
        if u_data['userID'] == user_id and u_data['role'] == 'Customer':
            current_status = u_data['status']
            new_status = 'Locked' if current_status == 'Active' else 'Active'
            
            confirm = input(f"Are you sure you want to change status of {u_data['name']} from '{current_status}' to '{new_status}'? (Y/N): ").strip().upper()
            if confirm == 'Y':
                u_data['status'] = new_status
                dm.save_data(dm.USERS_FILE, users_data)
                print(f"Account status of {u_data['name']} updated to '{new_status}'.")
            else:
                print("Action canceled.")
            user_found = True
            break
            
    if not user_found:
        print("[ERROR] No Customer found with this ID.")


def view_all_bookings():
    print("--- ALL BOOKINGS IN THE SYSTEM ---")
    
    all_bookings_data = dm.load_data(dm.BOOKINGS_FILE)
    if not all_bookings_data:
        print("No bookings found in the system.")
        return

    users_data = {u['userID']: u['name'] for u in dm.load_data(dm.USERS_FILE)}
    vehicles_data = {v['vehicleID']: f"{v['brand']} {v['model']}" for v in dm.load_data(dm.VEHICLES_FILE)}

    print(f"Found a total of {len(all_bookings_data)} bookings:")
    for b_data in all_bookings_data:
        b = dm.deserialize_booking(b_data)
        
        customer_name = users_data.get(b.customerID, "Unknown")
        vehicle_name = vehicles_data.get(b.vehicleID, "Unknown")

        print("-" * 20)
        print(f"  Booking ID: {b.bookingID}")
        print(f"  Customer: {customer_name} (ID: {b.customerID})")
        print(f"  Vehicle: {vehicle_name} (ID: {b.vehicleID})")
        print(f"  Status: {b.status}")
