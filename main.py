import base64
import requests

def extract_tax_data_from_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    response = requests.post(
        "http://localhost:9192/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "Qwen2.5-VL-7B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are an OCR expert. Extract the table from the image and output it as a valid JSON array."
                        },
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
    )

    return response.json()["choices"][0]["message"]["content"].strip()
