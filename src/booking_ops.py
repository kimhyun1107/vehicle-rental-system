from datetime import datetime, timedelta
from typing import List
from models import Customer, Vehicle, Booking, Payment
import data_manager as dm
from utils import get_next_id


def rent_vehicle(customer: Customer, vehicle: Vehicle) -> None:
    print("\n--- RENT VEHICLE ---")
    
    if vehicle.status != 'available':
        print("[ERROR] This vehicle is currently not available.")
        return
    
    try:
        start_date_str = input("Enter rental start date (DD/MM/YYYY): ").strip()
        end_date_str = input("Enter rental end date (DD/MM/YYYY): ").strip()
        
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        
        if end_date <= start_date:
            print("[ERROR] End date must be after the start date.")
            return
        
        if start_date < datetime.now():
            print("[ERROR] Cannot rent a vehicle in the past.")
            return
            
    except ValueError:
        print("[ERROR] Invalid date format. Please use DD/MM/YYYY.")
        return
    
    if _check_schedule_conflict(vehicle.vehicleID, start_date_str, end_date_str):
        print("[ERROR] This vehicle is already booked during this time.")
        return
    
    num_days = (end_date - start_date).days
    if num_days == 0:
        num_days = 1
    total_cost = num_days * vehicle.pricePerDay
    
    print(f"\nTotal cost: {total_cost:,.0f} VND ({num_days} days x {vehicle.pricePerDay:,.0f} VND/day)")
    confirm = input("Confirm payment? (Y/N): ").strip().upper()
    
    if confirm != 'Y':
        print("Booking cancelled.")
        return
    
    payment_success = _make_payment(total_cost)
    
    if not payment_success:
        print("[ERROR] Payment failed.")
        return
    
    bookings_data = dm.load_data(dm.BOOKINGS_FILE)
    next_booking_id = get_next_id(bookings_data, 'bookingID')
    
    new_booking = Booking(
        bookingID=next_booking_id,
        customerID=customer.userID,
        vehicleID=vehicle.vehicleID,
        startDate=start_date_str,
        endDate=end_date_str,
        totalAmount=total_cost,
        status='Confirmed'
    )
    
    bookings_data.append(dm.serialize(new_booking))
    dm.save_data(dm.BOOKINGS_FILE, bookings_data)
    
    _save_payment(next_booking_id, total_cost)
    
    _update_vehicle_status(vehicle.vehicleID, 'rented')
    
    print(f"\n✓ Booking successful. Booking ID: {next_booking_id}")


def cancel_booking(customer: Customer, bookings: List[Booking]) -> None:
    try:
        booking_id = int(input("\nEnter the booking ID to cancel (0 to go back): "))
        if booking_id == 0:
            return
    except ValueError:
        print("[ERROR] ID must be a number.")
        return
    
    booking_found = None
    for b in bookings:
        if b.bookingID == booking_id:
            booking_found = b
            break
    
    if not booking_found:
        print("[ERROR] Booking not found.")
        return
    
    print(f"\nBooking #{booking_found.bookingID}: {booking_found.startDate} -> {booking_found.endDate}")
    confirm = input("Are you sure you want to cancel this booking? (Y/N): ").strip().upper()
    
    if confirm != 'Y':
        print("Action cancelled.")
        return
    
    if booking_found.status == 'Cancelled':
        print("[ERROR] This booking has already been cancelled.")
        return
    
    try:
        start_date = datetime.strptime(booking_found.startDate, "%d/%m/%Y")
        days_until = (start_date - datetime.now()).days
        
        if days_until < 1:
            print("[ERROR] Cannot cancel; cancellation must be at least 1 day before the start date.")
            return
    except ValueError:
        pass
    
    bookings_data = dm.load_data(dm.BOOKINGS_FILE)
    for b_data in bookings_data:
        if b_data['bookingID'] == booking_id:
            b_data['status'] = 'Cancelled'
            break
    
    dm.save_data(dm.BOOKINGS_FILE, bookings_data)
    
    _update_vehicle_status(booking_found.vehicleID, 'available')
    
    print("✓ Booking cancelled successfully.")


def _check_schedule_conflict(vehicle_id: int, start: str, end: str) -> bool:
    bookings_data = dm.load_data(dm.BOOKINGS_FILE)
    
    for b in bookings_data:
        if b['vehicleID'] == vehicle_id and b['status'] in ['Confirmed', 'Pending']:
            if not (end <= b['startDate'] or start >= b['endDate']):
                return True
    
    return False


def _make_payment(amount: float) -> bool:
    print(f"\n--- PAYMENT SIMULATION {amount:,.0f} VND ---")
    print("Processing payment...")
    print("✓ Payment successful!")
    return True


def _save_payment(booking_id: int, amount: float) -> None:
    payments_data = dm.load_data(dm.PAYMENTS_FILE)
    next_payment_id = get_next_id(payments_data, 'paymentID')
    
    new_payment = Payment(
        paymentID=next_payment_id,
        bookingID=booking_id,
        paymentDate=datetime.now().strftime("%d/%m/%Y"),
        amount=amount,
        status='Success',
        paymentMethod='Simulated'
    )
    
    payments_data.append(dm.serialize(new_payment))
    dm.save_data(dm.PAYMENTS_FILE, payments_data)


def _update_vehicle_status(vehicle_id: int, new_status: str) -> None:
    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    
    for v in vehicles_data:
        if v['vehicleID'] == vehicle_id:
            v['status'] = new_status
            break
    
    dm.save_data(dm.VEHICLES_FILE, vehicles_data)
