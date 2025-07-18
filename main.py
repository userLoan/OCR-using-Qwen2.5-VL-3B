import base64
import requests
import json
import os
from dotenv import load_dotenv
import streamlit as st

# Load biến môi trường
load_dotenv()
API_KEY = os.getenv("API_KEY", "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")

def extract_tax_data_from_image(image_path):
    # Đọc ảnh và encode base64
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    # Chuẩn bị headers
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-app-name.streamlit.app/",
        "X-Title": "My OCR App"
    }

    # Tạo request body
    data = {
        "model": "qwen/qwen2.5-vl-72b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the table and return JSON:"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    }

    # Gửi request
    try:
        response = requests.post(
            headers=headers,
            data=json.dumps(data),
            timeout=30  # Thêm timeout để tránh treo
        )
        response.raise_for_status()  # Ném lỗi nếu không thành công
    except requests.exceptions.RequestException as e:
        raise Exception(f"Lỗi: {e.response.status_code if hasattr(e.response, 'status_code') else 'Kết nối thất bại'} - {str(e)}")

    return response.json()["choices"][0]["message"]["content"]
