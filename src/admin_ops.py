# src/admin_ops.py

from models import Vehicle, Customer
import data_manager as dm
from utils import get_next_id


def manage_vehicles(admin_id: int):
    """Menu chính cho UC Manage Vehicles."""
    while True:
        print("\n--- QUẢN LÝ XE ---")
        print("1. Thêm xe mới")
        print("2. Sửa thông tin xe")
        print("3. Xóa xe")
        print("4. Xem tất cả xe")
        print("0. Quay lại menu Admin")
        choice = input("Nhập lựa chọn của bạn: ").strip()

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
            print("[LỖI] Lựa chọn không hợp lệ.")


def _add_vehicle(admin_id: int):
    """Hàm con để Thêm xe"""
    print("--- Thêm xe mới ---")
    brand = input("Nhập hãng xe: ").strip()
    model = input("Nhập mẫu xe: ").strip()
    license_plate = input("Nhập biển số xe: ").strip()
    try:
        price_per_day = float(input("Nhập giá thuê/ngày: "))
    except ValueError:
        print("[LỖI] Giá phải là một con số.")
        return

    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    
    for v in vehicles_data:
        if v['license_plate'] == license_plate:
            print("[LỖI] Biển số xe này đã tồn tại trong hệ thống.")
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
    print(f"Đã thêm xe '{brand} {model}' thành công.")


def _edit_vehicle():
    """Hàm con để Sửa xe"""
    _view_all_vehicles() 
    try:
        vehicle_id = int(input("Nhập ID xe bạn muốn sửa: "))
    except ValueError:
        print("[LỖI] ID phải là số.")
        return
        
    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    vehicle_found = False
    for v_data in vehicles_data:
        if v_data['vehicleID'] == vehicle_id:
            print(f"Đang sửa xe: {v_data['brand']} {v_data['model']}")
            try:
                new_price = input(f"Giá mới (hiện tại {v_data['pricePerDay']}, nhấn Enter để bỏ qua): ").strip()
                new_status = input(f"Trạng thái mới (hiện tại '{v_data['status']}', nhấn Enter để bỏ qua): ").strip()
                
                if new_price:
                    v_data['pricePerDay'] = float(new_price)
                if new_status and new_status in ['available', 'rented', 'maintenance']:
                    v_data['status'] = new_status
                
                vehicle_found = True
                break
            except ValueError:
                print("[LỖI] Giá nhập không hợp lệ.")
                return

    if vehicle_found:
        dm.save_data(dm.VEHICLES_FILE, vehicles_data)
        print("Cập nhật xe thành công.")
    else:
        print("[LỖI] Không tìm thấy xe với ID này.")


def _delete_vehicle():
    """Hàm con để Xóa xe"""
    _view_all_vehicles() 
    try:
        vehicle_id = int(input("Nhập ID xe bạn muốn XÓA: "))
    except ValueError:
        print("[LỖI] ID phải là số.")
        return
        
    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    vehicle_to_delete = None
    for v_data in vehicles_data:
        if v_data['vehicleID'] == vehicle_id:
            vehicle_to_delete = v_data
            break
    
    if vehicle_to_delete:
        confirm = input(f"Bạn có chắc muốn XÓA xe {vehicle_to_delete['brand']} {vehicle_to_delete['model']}? (Y/N): ").strip().upper()
        if confirm == 'Y':
            vehicles_data.remove(vehicle_to_delete)
            dm.save_data(dm.VEHICLES_FILE, vehicles_data)
            print("Đã xóa xe thành công.")
        else:
            print("Đã hủy thao tác xóa.")
    else:
        print("[LỖI] Không tìm thấy xe với ID này.")


def _view_all_vehicles():
    """Hàm con để Xem tất cả xe"""
    print("--- Toàn bộ xe trong hệ thống ---")
    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    if not vehicles_data:
        print("Chưa có xe nào trong hệ thống.")
        return
    for v_data in vehicles_data:
        v = dm.deserialize_vehicle(v_data)
        print(f"  [ID: {v.vehicleID}] {v.brand} {v.model} ({v.license_plate}) - Trạng thái: {v.status}")


def manage_users():
    """Triển khai Use Case Manage Users."""
    print("\n--- QUẢN LÝ NGƯỜI DÙNG (CUSTOMER) ---")
    
    users_data = dm.load_data(dm.USERS_FILE)
    customers = [dm.deserialize_user(u) for u in users_data if u['role'] == 'Customer']
    
    if not customers:
        print("Chưa có tài khoản Customer nào.")
        return
        
    print("Danh sách Customer:")
    for c in customers:
        print(f"  [ID: {c.userID}] {c.name} ({c.email}) - Trạng thái: {c.status}")
        
    try:
        user_id = int(input("Nhập ID Customer bạn muốn thay đổi trạng thái: "))
    except ValueError:
        print("[LỖI] ID phải là số.")
        return
        
    user_found = False
    for u_data in users_data:
        if u_data['userID'] == user_id and u_data['role'] == 'Customer':
            current_status = u_data['status']
            new_status = 'Locked' if current_status == 'Active' else 'Active'
            
            confirm = input(f"Bạn có chắc muốn đổi trạng thái của {u_data['name']} từ '{current_status}' sang '{new_status}'? (Y/N): ").strip().upper()
            if confirm == 'Y':
                u_data['status'] = new_status
                dm.save_data(dm.USERS_FILE, users_data)
                print(f"Đã cập nhật trạng thái tài khoản {u_data['name']} thành '{new_status}'.")
            else:
                print("Đã hủy thao tác.")
            user_found = True
            break
            
    if not user_found:
        print("[LỖI] Không tìm thấy Customer với ID này.")


def view_all_bookings():
    """Triển khai chức năng 'View All Bookings' cho Admin."""
    print("--- TẤT CẢ BOOKING TRONG HỆ THỐNG ---")
    
    all_bookings_data = dm.load_data(dm.BOOKINGS_FILE)
    if not all_bookings_data:
        print("Chưa có booking nào trong hệ thống.")
        return

    users_data = {u['userID']: u['name'] for u in dm.load_data(dm.USERS_FILE)}
    vehicles_data = {v['vehicleID']: f"{v['brand']} {v['model']}" for v in dm.load_data(dm.VEHICLES_FILE)}

    print(f"Tìm thấy tổng cộng {len(all_bookings_data)} booking:")
    for b_data in all_bookings_data:
        b = dm.deserialize_booking(b_data)
        
        customer_name = users_data.get(b.customerID, "Không rõ")
        vehicle_name = vehicles_data.get(b.vehicleID, "Không rõ")

        print("-" * 20)
        print(f"  Booking ID: {b.bookingID}")
        print(f"  Khách hàng: {customer_name} (ID: {b.customerID})")
        print(f"  Xe: {vehicle_name} (ID: {b.vehicleID})")
        print(f"  Trạng thái: {b.status}")