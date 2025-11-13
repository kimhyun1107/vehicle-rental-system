# src/models.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    userID: int
    name: str
    email: str
    password: str
    role: str

    def login(self) -> bool:
        print(f"User {self.name} login method called.")
        return True

    def logout(self) -> None:
        print(f"User {self.name} logged out.")

@dataclass
class Customer(User):
    phoneNumber: str = ""
    bookingHistory: List[int] = field(default_factory=list)
    status: str = 'Active'

    def __post_init__(self):
        self.role = 'Customer'

@dataclass
class Admin(User):
    def __post_init__(self):
        self.role = 'Admin'

@dataclass
class Vehicle:
    vehicleID: int 
    license_plate: str 
    brand: str 
    model: str 
    pricePerDay: float 
    status: str
    
    def getDetails(self) -> str:
        return f"  ID: {self.vehicleID}\n  Biển số: {self.license_plate}\n  Tên: {self.brand} {self.model}\n  Giá: {self.pricePerDay:,.0f} VND/ngày\n  Trạng thái: {self.status}"

@dataclass
class Booking:
    bookingID: int
    customerID: int 
    vehicleID: int 
    startDate: str
    endDate: str
    totalAmount: float
    status: str

@dataclass
class Payment:
    paymentID: int
    bookingID: int 
    paymentDate: str
    amount: float
    status: str
    paymentMethod: str = "Simulated"