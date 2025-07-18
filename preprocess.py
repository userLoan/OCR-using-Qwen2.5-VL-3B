import os
import cv2
import glob
import fitz
import numpy as np
from PIL import Image
from pdf2image import convert_from_path

def pdf_to_images(pdf_path, output_dir, zoom=2):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))  # Zoom giúp tăng DPI
        image_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(image_path)
        image_paths.append(image_path)

    return image_paths

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
