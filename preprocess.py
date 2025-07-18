import os
import cv2
import glob
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import platform

def pdf_to_images(pdf_path, output_dir, dpi=300):
    try:
        os.makedirs(output_dir, exist_ok=True)

        # Xác định poppler_path nếu chạy trên Windows
        if platform.system() == "Windows":
            poppler_path = r"F:\poppler-24.08.0\Library\bin"  # sửa lại đúng đường dẫn máy bạn
        else:
            poppler_path = None  # Trên Linux (Streamlit Cloud) không cần

        pages = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
        image_paths = []

        for i, page in enumerate(pages):
            image_name = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{i+1}.jpg"
            image_path = os.path.join(output_dir, image_name)
            page.save(image_path, "JPEG", quality=95)
            image_paths.append(image_path)

        return image_paths
    except Exception as e:
        print(f"✗ Error processing {pdf_path}: {e}")
        return []

# ====== Xử lý folder ảnh (clahe, nhị phân, giãn) ======
def preprocess_image(image_path):
    try:
        pil_img = Image.open(image_path)
        img = np.array(pil_img)

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_img = clahe.apply(gray)
        _, binary = cv2.threshold(contrast_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((1, 1), np.uint8)
        bold_img = cv2.dilate(binary, kernel, iterations=1)

        return bold_img
    except Exception as e:
        print(f"❌ Lỗi xử lý ảnh {image_path}: {e}")
        return None

# ====== Xử lý toàn bộ ảnh trong thư mục ======
def process_images_in_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    processed_paths = []

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            processed_img = preprocess_image(input_path)
            if processed_img is not None:
                Image.fromarray(processed_img).save(output_path)
                processed_paths.append(output_path)

    return processed_paths
