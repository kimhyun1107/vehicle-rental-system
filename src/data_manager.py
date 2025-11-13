# src/data_manager.py

import json
import os
from typing import List, Dict, Any
from dataclasses import asdict


# Đường dẫn file dữ liệu
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
VEHICLES_FILE = os.path.join(DATA_DIR, "vehicles.json")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.json")
PAYMENTS_FILE = os.path.join(DATA_DIR, "payments.json")


def init_data_files() -> None:
    """Khởi tạo các file dữ liệu nếu chưa tồn tại"""
    
    # Tạo thư mục data nếu chưa có
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Khởi tạo các file JSON rỗng
    for file_path in [USERS_FILE, VEHICLES_FILE, BOOKINGS_FILE, PAYMENTS_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)


def load_data(file_path: str) -> List[Dict[str, Any]]:
    """Đọc dữ liệu từ file JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(file_path: str, data: List[Dict[str, Any]]) -> None:
    """Lưu dữ liệu vào file JSON"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def serialize(obj: Any) -> Dict[str, Any]:
    """Chuyển đối tượng thành dictionary để lưu JSON"""
    return asdict(obj)


def deserialize_user(data: Dict[str, Any]):
    """Chuyển dictionary thành đối tượng User (Customer/Admin)"""
    from models import Customer, Admin
    
    if data['role'] == 'Customer':
        return Customer(
            userID=data['userID'],
            name=data['name'],
            email=data['email'],
            password=data['password'],
            phoneNumber=data['phoneNumber'],
            bookingHistory=data.get('bookingHistory', []),
            status=data.get('status', 'Active'),
            role='Customer'
        )
    elif data['role'] == 'Admin':
        return Admin(
            userID=data['userID'],
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role='Admin'
        )


def deserialize_vehicle(data: Dict[str, Any]):
    """Chuyển dictionary thành đối tượng Vehicle"""
    from models import Vehicle
    
    return Vehicle(
        vehicleID=data['vehicleID'],
        license_plate=data['license_plate'],
        brand=data['brand'],
        model=data['model'],
        pricePerDay=data['pricePerDay'],
        status=data['status']
    )


def deserialize_booking(data: Dict[str, Any]):
    """Chuyển dictionary thành đối tượng Booking"""
    from models import Booking
    
    return Booking(
        bookingID=data['bookingID'],
        customerID=data['customerID'],
        vehicleID=data['vehicleID'],
        startDate=data['startDate'],
        endDate=data['endDate'],
        totalAmount=data['totalAmount'],
        status=data['status']
    )


def deserialize_payment(data: Dict[str, Any]):
    """Chuyển dictionary thành đối tượng Payment"""
    from models import Payment
    
    return Payment(
        paymentID=data['paymentID'],
        bookingID=data['bookingID'],
        paymentDate=data['paymentDate'],
        amount=data['amount'],
        status=data['status'],
        paymentMethod=data.get('paymentMethod', 'Simulated')
    )


# Khởi tạo file khi import module
init_data_files()