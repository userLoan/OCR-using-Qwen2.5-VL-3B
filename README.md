## Prerequisites

- Python 3.9+
- Ollama installed and running locally
- The Qwen2.5-VL-3B model downloaded in Ollama

Install the required packages:

```bash
pip install -r requirements.txt
```

## Project Structure

```
pdf-qa-system/
├── streamlit.py
├── main.py                # Main application file
├── temp                   # Temporary directory
├── requirements.txt       # Project dependencies
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

## Dependencies

```
streamlit
langchain_core
langchain_community
langchain_ollama
pypdf
pdf2image
pillow
faiss-cpu
openpyxl
numpy==1.24.3
typing-extensions==4.5.0
```

## Usage

1. Start the Ollama service and ensure the Qwen2.5-VL-3B model is available:

```bash
ollama run qwen2.5vl:3b
```

2. Run the Streamlit application:

```bash
streamlit run streamlit.py
```

3. Access the application in your web browser at `http://localhost:8501`

4. Upload a PDF document using the file uploader

5. OCR

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ollama for the local language model hosting
- Streamlit for the web interface framework
