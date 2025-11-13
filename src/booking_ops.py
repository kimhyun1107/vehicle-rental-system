# src/booking_ops.py

from datetime import datetime, timedelta
from typing import List
from models import Customer, Vehicle, Booking, Payment
import data_manager as dm
from utils import get_next_id


def rent_vehicle(customer: Customer, vehicle: Vehicle) -> None:
    """UC Rent Vehicle - Thuê xe"""
    print("\n--- THUÊ XE ---")
    
    # Kiểm tra xe có sẵn không
    if vehicle.status != 'available':
        print("[LỖI] Xe này hiện không khả dụng.")
        return
    
    # Bước 2: Nhập ngày thuê
    try:
        start_date_str = input("Nhập ngày bắt đầu thuê (DD/MM/YYYY): ").strip()
        end_date_str = input("Nhập ngày trả xe (DD/MM/YYYY): ").strip()
        
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        
        if end_date <= start_date:
            print("[LỖI] Ngày trả xe phải sau ngày bắt đầu.")
            return
        
        # Kiểm tra không được thuê quá khứ
        if start_date < datetime.now():
            print("[LỖI] Không thể thuê xe trong quá khứ.")
            return
            
    except ValueError:
        print("[LỖI] Định dạng ngày không hợp lệ. Vui lòng dùng DD/MM/YYYY.")
        return
    
    # Bước 3: Kiểm tra xung đột lịch
    if _check_schedule_conflict(vehicle.vehicleID, start_date_str, end_date_str):
        print("[LỖI] Xe đã được đặt trong khoảng thời gian này.")
        return
    
    # Bước 4: Tính tổng tiền
    num_days = (end_date - start_date).days
    if num_days == 0:
        num_days = 1  # Tối thiểu 1 ngày
    total_cost = num_days * vehicle.pricePerDay
    
    # Bước 5: Xác nhận thanh toán
    print(f"\nTổng chi phí: {total_cost:,.0f} VND ({num_days} ngày x {vehicle.pricePerDay:,.0f} VND/ngày)")
    confirm = input("Xác nhận thanh toán? (Y/N): ").strip().upper()
    
    if confirm != 'Y':
        print("Đã hủy đặt xe.")
        return
    
    # Bước 7: Mô phỏng thanh toán (include Make Payment)
    payment_success = _make_payment(total_cost)
    
    if not payment_success:
        print("[LỖI] Thanh toán thất bại.")
        return
    
    # Bước 8: Lưu booking
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
    
    # Lưu payment
    _save_payment(next_booking_id, total_cost)
    
    # Cập nhật trạng thái xe
    _update_vehicle_status(vehicle.vehicleID, 'rented')
    
    # Bước 9: Thông báo thành công
    print(f"\n✓ Đặt xe thành công! Mã booking: {next_booking_id}")


def cancel_booking(customer: Customer, bookings: List[Booking]) -> None:
    """UC Cancel Booking - Hủy booking"""
    
    # Bước 1: Chọn booking để hủy
    try:
        booking_id = int(input("\nNhập ID booking muốn hủy (0 để quay lại): "))
        if booking_id == 0:
            return
    except ValueError:
        print("[LỖI] ID phải là số.")
        return
    
    # Tìm booking
    booking_found = None
    for b in bookings:
        if b.bookingID == booking_id:
            booking_found = b
            break
    
    if not booking_found:
        print("[LỖI] Không tìm thấy booking này.")
        return
    
    # Bước 2: Xác nhận hủy
    print(f"\nBooking #{booking_found.bookingID}: {booking_found.startDate} -> {booking_found.endDate}")
    confirm = input("Bạn có chắc muốn hủy booking này? (Y/N): ").strip().upper()
    
    if confirm != 'Y':
        print("Đã hủy thao tác.")
        return
    
    # Bước 4: Kiểm tra chính sách hủy
    if booking_found.status == 'Cancelled':
        print("[LỖI] Booking này đã được hủy trước đó.")
        return
    
    try:
        start_date = datetime.strptime(booking_found.startDate, "%d/%m/%Y")
        days_until = (start_date - datetime.now()).days
        
        if days_until < 1:
            print("[LỖI] Không thể hủy, đã quá hạn hủy (phải trước 1 ngày).")
            return
    except ValueError:
        pass  # Nếu lỗi parse date, vẫn cho phép hủy
    
    # Bước 5: Cập nhật trạng thái booking
    bookings_data = dm.load_data(dm.BOOKINGS_FILE)
    for b_data in bookings_data:
        if b_data['bookingID'] == booking_id:
            b_data['status'] = 'Cancelled'
            break
    
    dm.save_data(dm.BOOKINGS_FILE, bookings_data)
    
    # Cập nhật trạng thái xe về available
    _update_vehicle_status(booking_found.vehicleID, 'available')
    
    # Bước 6: Thông báo thành công
    print("✓ Đã hủy booking thành công.")


def _check_schedule_conflict(vehicle_id: int, start: str, end: str) -> bool:
    """Kiểm tra xung đột lịch đặt xe"""
    bookings_data = dm.load_data(dm.BOOKINGS_FILE)
    
    for b in bookings_data:
        if b['vehicleID'] == vehicle_id and b['status'] in ['Confirmed', 'Pending']:
            # Kiểm tra overlap (đơn giản hóa: so sánh string)
            if not (end <= b['startDate'] or start >= b['endDate']):
                return True  # Có xung đột
    
    return False


def _make_payment(amount: float) -> bool:
    """Mô phỏng thanh toán (include Make Payment UC)"""
    print(f"\n--- MÔ PHỎNG THANH TOÁN {amount:,.0f} VND ---")
    print("Đang xử lý thanh toán...")
    print("✓ Thanh toán thành công!")
    return True


def _save_payment(booking_id: int, amount: float) -> None:
    """Lưu thông tin thanh toán"""
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
    """Cập nhật trạng thái xe"""
    vehicles_data = dm.load_data(dm.VEHICLES_FILE)
    
    for v in vehicles_data:
        if v['vehicleID'] == vehicle_id:
            v['status'] = new_status
            break
    
    dm.save_data(dm.VEHICLES_FILE, vehicles_data)