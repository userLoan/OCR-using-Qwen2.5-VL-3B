import requests
import json

def extract_table_from_image_url(image_url: str, api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {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}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://pdfs-to-excel-dtl-mamwcxcar6nsbk8l4cssa6.streamlit.app/",
        "X-Title": "PDF Table Extractor"
    }

    payload = {
        "model": "qwen/qwen2.5-vl-32b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an OCR expert. Extract the table from the image and output it as a valid JSON array."
                    },
                    {
                        "type": "image",
                        "image": [image_path]
                    }
                ]
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"
