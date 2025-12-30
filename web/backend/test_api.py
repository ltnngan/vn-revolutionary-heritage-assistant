# test_api.py

import requests
import os

BASE_URL = 'http://localhost:8000/api'
IMAGE_PATH = '../../data/images/hau_giang/chien_thang_chay_dap/7.png'


def test_health_check():
    """Kiểm tra server đã sẵn sàng chưa"""
    response = requests.get(f'{BASE_URL}/health/')
    print("Health Check:", response.json())


def test_prediction():
    """Test VQA prediction"""
    # Kiểm tra file ảnh
    if not os.path.exists(IMAGE_PATH):
        print(f"\nKhông tìm thấy: {IMAGE_PATH}")
        print("Kiểm tra lại đường dẫn!")
        exit(1)
    
    print(f"✓ Tìm thấy ảnh: {IMAGE_PATH}\n")
    
    # Gửi request
    with open(IMAGE_PATH, 'rb') as f:
        files = {'image': f}
        data = {'question': 'Những hình ảnh nào có thể được quan sát trong bức ảnh?'}
        
        response = requests.post(
            f'{BASE_URL}/predict/',
            files=files,
            data=data
        )
    
    print("Prediction:", response.json())


if __name__ == '__main__':
    test_health_check()
    test_prediction()