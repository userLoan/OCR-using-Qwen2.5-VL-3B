import base64
import requests
import json

def extract_tax_data_from_image(image_path):
    # Đọc ảnh và encode base64
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    # Chuẩn bị headers
    headers = {
        "Authorization": "Bearer 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",
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
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code != 200:
        raise Exception(f"Lỗi: {response.status_code} - {response.text}")

    return response.json()["choices"][0]["message"]["content"]
