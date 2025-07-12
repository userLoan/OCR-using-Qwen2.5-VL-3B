import streamlit as st
import os
import json
import tempfile
from pathlib import Path
import pandas as pd
from PIL import Image
from preprocess import pdf_to_images, process_images_in_folder, poppler_path
from main import extract_tax_data_from_image

# Cấu hình giao diện
st.set_page_config(page_title="PDFs to Excel", layout="wide")
st.title("🧾 PDFs → Excel")

uploaded_files = st.file_uploader(
    "📤 Tải lên một hoặc nhiều file PDF",
    type=["pdf"],
    accept_multiple_files=True
)

def markdown_table_to_dataframe(md_text):
    try:
        lines = md_text.strip().split('\n')
        header = [h.strip() for h in lines[0].split('|') if h.strip()]
        rows = []

        for line in lines[2:]:  # Bỏ dòng header và --- separator
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if len(cells) == len(header):
                rows.append(cells)

        df = pd.DataFrame(rows, columns=header)
        return df if not df.empty else None
    except Exception:
        return None

def try_parse_json(result):
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        # Trường hợp là chuỗi JSON object không có dấu [ ] bao quanh
        try:
            fixed = "[" + result.strip().rstrip(',') + "]"
            return json.loads(fixed)
        except Exception:
            return None

if uploaded_files:
    with tempfile.TemporaryDirectory() as temp_dir:
        for pdf_index, uploaded_file in enumerate(uploaded_files, start=1):
            st.divider()
            st.subheader(f"📄 File {pdf_index}: {uploaded_file.name}")

            # Lưu file PDF
            pdf_path = os.path.join(temp_dir, uploaded_file.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.read())

            image_dir = os.path.join(temp_dir, f"images_{pdf_index}")
            processed_dir = os.path.join(temp_dir, f"processed_{pdf_index}")
            os.makedirs(image_dir, exist_ok=True)
            os.makedirs(processed_dir, exist_ok=True)

            with st.spinner("📄 Đang tách PDF thành ảnh..."):
                image_paths = pdf_to_images(pdf_path, image_dir, poppler_path=poppler_path)

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

                            # 1. Thử parse JSON
                            parsed_json = try_parse_json(result)
                            if parsed_json:
                                df = pd.DataFrame(parsed_json)
                                st.dataframe(df)
                                all_dataframes.append(df)
                                continue

                            # 2. Thử parse Markdown
                            df_md = markdown_table_to_dataframe(result)
                            if df_md is not None:
                                st.dataframe(df_md)
                                all_dataframes.append(df_md)
                            else:
                                st.code(result)

                    if all_dataframes:
                        final_df = pd.concat(all_dataframes, ignore_index=True)
                        st.subheader("📊 Tổng hợp dữ liệu")
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
    st.info("📤 Hãy tải lên file PDF để bắt đầu.")
