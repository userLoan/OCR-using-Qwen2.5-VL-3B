import streamlit as st
import os
import json
import tempfile
import re
from pathlib import Path
import pandas as pd
from PIL import Image
from preprocess import pdf_to_images, process_images_in_folder
from main import extract_tax_data_from_image

# Giao diện
st.set_page_config(page_title="PDFs to Excel", layout="wide")
st.title("🧾 PDFs → Excel")

uploaded_files = st.file_uploader(
    "📤 Tải lên một hoặc nhiều file PDF",
    type=["pdf"],
    accept_multiple_files=True
)

def try_parse_json(result):
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        try:
            fixed = "[" + result.strip().rstrip(',') + "]"
            return json.loads(fixed)
        except Exception:
            return None

def clean_and_parse_json_blocks(text):
    """Xử lý chuỗi trả về bị encode sai và chuyển thành danh sách dict"""
    blocks = re.findall(r"\{[^}]+\}", text, re.DOTALL)
    cleaned = []
    for block in blocks:
        try:
            block_fixed = block.replace('"""', '"').replace('\n', '').strip(',')
            block_fixed = re.sub(r'""([^""]+?)""', r'"\1"', block_fixed)
            cleaned.append(json.loads(block_fixed))
        except json.JSONDecodeError:
            continue
    return cleaned if cleaned else None

if uploaded_files:
    with tempfile.TemporaryDirectory() as temp_dir:
        for pdf_index, uploaded_file in enumerate(uploaded_files, start=1):
            st.divider()
            st.subheader(f"📄 File {pdf_index}: {uploaded_file.name}")

            pdf_path = os.path.join(temp_dir, uploaded_file.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.read())

            image_dir = os.path.join(temp_dir, f"images_{pdf_index}")
            processed_dir = os.path.join(temp_dir, f"processed_{pdf_index}")
            os.makedirs(image_dir, exist_ok=True)
            os.makedirs(processed_dir, exist_ok=True)

            with st.spinner("📄 Đang tách PDF thành ảnh..."):
                image_paths = pdf_to_images(pdf_path, image_dir)

            if not image_paths:
                st.warning("⚠️ Không tạo được ảnh từ file PDF.")
                continue

            st.success(f"✅ Đã tạo {len(image_paths)} ảnh.")

            with st.spinner("🖼️ Đang tiền xử lý ảnh..."):
                processed_paths = process_images_in_folder(image_dir, processed_dir)

            st.markdown("#### 📸 Ảnh sau tiền xử lý:")
            image_dict = dict(zip([os.path.basename(p) for p in processed_paths], processed_paths))
            selected_images = []
            select_all = st.checkbox("📌 Chọn tất cả ảnh", key=f"select_all_{pdf_index}")
            cols = st.columns(2)

            for i, (name, path) in enumerate(image_dict.items()):
                with cols[i % 2]:
                    st.image(Image.open(path), caption=name, use_container_width=True)
                    if st.checkbox(f"Chọn: {name}", value=select_all, key=f"{pdf_index}_{i}"):
                        selected_images.append(path)

            if selected_images:
                if st.button(f"🧠 Chạy OCR cho {len(selected_images)} ảnh", key=f"ocr_btn_{pdf_index}"):
                    all_dataframes = []

                    for idx, img_path in enumerate(selected_images):
                        with st.spinner(f"🧠 Đang OCR ảnh {idx + 1}/{len(selected_images)}..."):
                            result = extract_tax_data_from_image(img_path)
                            st.markdown(f"**📷 Ảnh: `{Path(img_path).name}`**")

                            parsed_json = try_parse_json(result)
                            if not parsed_json:
                                parsed_json = clean_and_parse_json_blocks(result)

                            if parsed_json:
                                df = pd.DataFrame(parsed_json)
                                all_dataframes.append(df)

                    if all_dataframes:
                        final_df = pd.concat(all_dataframes, ignore_index=True)
                        st.subheader("📊 Output")
                        st.dataframe(final_df)

                        output_path = os.path.join(temp_dir, f"output_{pdf_index}.xlsx")
                        final_df.to_excel(output_path, index=False)

                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="📥 Tải xuống Excel",
                                data=f,
                                file_name=f"output_{pdf_index}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"download_{pdf_index}"
                            )
                    else:
                        st.warning("⚠️ Không có dữ liệu hợp lệ.")
            else:
                st.info("📸 Vui lòng chọn ảnh để OCR.")
else:
    st.info("📤 Hãy tải lên file PDF để bắt đầu.")
