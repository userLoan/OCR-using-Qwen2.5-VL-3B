import ollama

def extract_tax_data_from_image(image_path: str) -> str:
    response = ollama.chat(
        model="qwen2.5vl:3b",
        messages=[
            {
                "role": "user",
                "content": ("You are an OCR expert. Extract the table from the image and output it as a valid JSON array."),
                "images": [image_path]
            }
        ]
    )
    return response['message']['content'].strip()
