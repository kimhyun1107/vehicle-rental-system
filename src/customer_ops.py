from typing import List, Optional
from models import Customer, Vehicle, Booking
import data_manager as dm


def view_vehicle_list() -> List[Vehicle]:
    print("\n Vehicle List")
    
    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    
    if not vehicles_data:
        print("There are currently no vehicles available for rent.")
        return []
    
    vehicles = []
    print(f"{'ID':<5} {'Brand':<15} {'Model':<15} {'Plate':<12} {'Price/Day':<15} {'Status':<12}")
    print("-" * 90)
    
    for v_data in vehicles_data:
        v = dm.deserialize_vehicle(v_data)
        vehicles.append(v)
        print(f"{v.vehicleID:<5} {v.brand:<15} {v.model:<15} {v.license_plate:<12} {v.pricePerDay:>12,.0f} VND {v.status:<12}")
    
    return vehicles


def view_vehicle_details(vehicles: List[Vehicle]) -> Optional[Vehicle]:
    try:
        vehicle_id = int(input("\nEnter vehicle ID to view details (0 to go back): "))
        if vehicle_id == 0:
            return None
    except ValueError:
        print("(Error) ID must be a number.")
        return None
    
    vehicle_found = None
    for v in vehicles:
        if v.vehicleID == vehicle_id:
            vehicle_found = v
            break

    if not vehicle_found:
        print("(Error) No vehicle found with this ID.")
        return None

    print("\n" + "=" * 40)
    print("Vehicle Details")
    print("=" * 40)
    print(vehicle_found.getDetails())
    print("=" * 40)
    
    return vehicle_found


def view_booking_history(customer: Customer) -> List[Booking]:
    print("\n Booking History ")
    
    all_bookings_data = dm.load_data(dm.BOOKINGS_FILE)
    customer_bookings = [
        dm.deserialize_booking(b)
        for b in all_bookings_data
        if b['customerID'] == customer.userID
    ]
    
    if not customer_bookings:
        print("You have no booking history.")
        return []

    vehicles_data = {
        v['vehicleID']: f"{v['brand']} {v['model']}"
        for v in dm.load_data(dm.VEHICLES_FILE)
    }
    
    print(f"{'ID':<5} {'Vehicle':<25} {'From':<12} {'To':<12} {'Total':<15} {'Status':<12}")
    print("-" * 95)
    
    for b in customer_bookings:
        vehicle_name = vehicles_data.get(b.vehicleID, "Unknown")
        print(f"{b.bookingID:<5} {vehicle_name:<25} {b.startDate:<12} {b.endDate:<12} {b.totalAmount:>12,.0f} VND {b.status:<12}")
    
    return customer_bookings
