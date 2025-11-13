# src/customer_ops.py

from typing import List, Optional
from models import Customer, Vehicle, Booking
import data_manager as dm


def view_vehicle_list() -> List[Vehicle]:
    """UC View Vehicle List - Xem danh sách xe"""
    print("\n--- DANH SÁCH XE ---")
    
    # Bước 2: Đọc dữ liệu xe
    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    
    # Alternative Flow: Không có xe
    if not vehicles_data:
        print("Hiện tại chưa có xe nào cho thuê.")
        return []
    
    # Bước 3: Hiển thị danh sách
    vehicles = []
    print(f"{'ID':<5} {'Hãng':<15} {'Mẫu':<15} {'Biển số':<12} {'Giá/ngày':<15} {'Trạng thái':<12}")
    print("-" * 90)
    
    for v_data in vehicles_data:
        v = dm.deserialize_vehicle(v_data)
        vehicles.append(v)
        print(f"{v.vehicleID:<5} {v.brand:<15} {v.model:<15} {v.license_plate:<12} {v.pricePerDay:>12,.0f} VND {v.status:<12}")
    
    return vehicles


def view_vehicle_details(vehicles: List[Vehicle]) -> Optional[Vehicle]:
    """UC View Vehicle Details - Xem chi tiết xe"""
    
    # Bước 1: Nhập ID xe
    try:
        vehicle_id = int(input("\nNhập ID xe để xem chi tiết (0 để quay lại): "))
        if vehicle_id == 0:
            return None
    except ValueError:
        print("[LỖI] ID phải là số.")
        return None
    
    # Bước 2: Tìm xe
    vehicle_found = None
    for v in vehicles:
        if v.vehicleID == vehicle_id:
            vehicle_found = v
            break
    
    # Alternative Flow: Không tìm thấy
    if not vehicle_found:
        print("[LỖI] Không tìm thấy xe với ID này.")
        return None
    
    # Bước 3: Hiển thị chi tiết
    print("\n" + "=" * 40)
    print("CHI TIẾT XE")
    print("=" * 40)
    print(vehicle_found.getDetails())
    print("=" * 40)
    
    return vehicle_found


def view_booking_history(customer: Customer) -> List[Booking]:
    """UC View Booking History - Xem lịch sử đặt xe"""
    print("\n--- LỊCH SỬ ĐẶT XE ---")
    
    # Bước 2: Lọc booking của customer này
    all_bookings_data = dm.load_data(dm.BOOKINGS_FILE)
    customer_bookings = [
        dm.deserialize_booking(b) 
        for b in all_bookings_data 
        if b['customerID'] == customer.userID
    ]
    
    # Alternative Flow: Không có booking
    if not customer_bookings:
        print("Bạn chưa có lịch sử đặt xe nào.")
        return []
    
    # Bước 3: Hiển thị danh sách
    vehicles_data = {v['vehicleID']: f"{v['brand']} {v['model']}" 
                     for v in dm.load_data(dm.VEHICLES_FILE)}
    
    print(f"{'ID':<5} {'Xe':<25} {'Từ ngày':<12} {'Đến ngày':<12} {'Tổng tiền':<15} {'Trạng thái':<12}")
    print("-" * 95)
    
    for b in customer_bookings:
        vehicle_name = vehicles_data.get(b.vehicleID, "Không rõ")
        print(f"{b.bookingID:<5} {vehicle_name:<25} {b.startDate:<12} {b.endDate:<12} {b.totalAmount:>12,.0f} VND {b.status:<12}")
    
    return customer_bookings