from openai import OpenAI

def extract_tax_data_from_image(image_url: str) -> str:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",  
    )

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://pdfs-to-excel-dtl-mamwcxcar6nsbk8l4cssa6.streamlit.app/",
            "X-Title": "PDFs to Excel"
        },
        extra_body={},
        model="qwen/qwen2.5-vl-72b-instruct:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an OCR expert. Extract the table from the image and return it as a valid JSON array."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]
    )

    return completion.choices[0].message.content.strip()
