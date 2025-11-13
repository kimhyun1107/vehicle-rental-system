# src/utils.py

import os
from typing import List, Dict, Any


def clear_screen() -> None:
    """Xóa màn hình console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause() -> None:
    """Tạm dừng chương trình, chờ user nhấn Enter"""
    input("\nNhấn Enter để tiếp tục...")


def get_next_id(data_list: List[Dict[str, Any]], id_field: str) -> int:
    """Lấy ID tiếp theo cho một entity"""
    if not data_list:
        return 1
    
    max_id = max(item[id_field] for item in data_list)
    return max_id + 1


def validate_email(email: str) -> bool:
    """Kiểm tra định dạng email đơn giản"""
    return '@' in email and '.' in email.split('@')[1]


def validate_phone(phone: str) -> bool:
    """Kiểm tra số điện thoại (đơn giản)"""
    return phone.isdigit() and len(phone) >= 10