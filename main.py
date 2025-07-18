import requests

def extract_tax_data_from_image(image_path):
    url = "https://api.example.com/ocr"  # URL API của Qwen2.5-VL-3B
    headers = {"Authorization": f"Bearer {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}"}
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        response = requests.post(url, headers=headers, files=files)
    response.raise_for_status()  # Ném lỗi nếu không thành công
    return response.json()
