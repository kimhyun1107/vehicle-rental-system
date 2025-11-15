

Nhóm 15 | Công Nghệ Phần Mềm

---

I. GIỚI THIỆU

Hệ thống quản lý thuê xe (Vehicle Rental System) là ứng dụng console 
- Khách hàng**: Đăng ký, đăng nhập, xem xe, thuê xe, quản lý booking
- Quản trị viên**: Quản lý xe, quản lý người dùng, xem báo cá
---
 TÍNH NĂNG

Chức năng Customer:
- Đăng ký tài khoản
- Đăng nhập/Đăng xuất
- Xem danh sách xe
- Xem chi tiết xe
- Thuê xe (bao gồm thanh toán)
- Xem lịch sử đặt xe
- Hủy booking

 Chức năng Admin:
-  Quản lý xe (Thêm/Sửa/Xóa/Xem)
-  Quản lý người dùng (Khóa/Mở khóa)
- Xem tất cả booking
CÔNG NGHỆ
Python
JSON
Docker 
VScode
excel

---





 Chạy với Docker
```bash
# Build image
docker build -t vehicle-rental-system .

# Chạy container
docker run -it vehicle-rental-system

# Chạy với volume (lưu dữ liệu)
docker run -it -v $(pwd)/data:/app/data vehicle-rental-system
```

---

TÀI KHOẢN TEST
Admin
- Email: admin@rental.com
- Password: admin

Customer
- Email: customer@gmail.com
- Password: customer


