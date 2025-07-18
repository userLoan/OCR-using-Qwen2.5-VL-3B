import os
from openai import OpenAI

def extract_tax_data_from_image(image_path: str) -> str:
    token = os.environ["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"]
    endpoint = "https://models.github.ai/inference"
    model = "openai/gpt-4.1"
    
    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an OCR expert.",
            },
            {
                "role": "user",
                "content": "Extract the table from the image and output it as a valid JSON array.",
            }
        ],
        temperature=1.0,
        top_p=1.0,
        model=model
    )
    
    print(response.choices[0].message.content)
