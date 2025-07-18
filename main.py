import base64
import requests

def extract_tax_data_from_image(image_path: str) -> str:
    # Đọc ảnh và encode thành base64
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

    headers = {
        "Authorization": "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",
        "HTTP-Referer": "https://pdfs-to-excel-dtl-mamwcxcar6nsbk8l4cssa6.streamlit.app/",
        "X-Title": "PDFs to Excel",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen/qwen2.5-vl-72b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "You are an OCR expert. Extract the table from the image and return it as a valid JSON array."},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                ]
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"Lỗi: {response.status_code} - {response.text}")
