 # py code beginning

import streamlit as st
import numpy as np
import pandas as pd
import os
from datetime import datetime

from PIL import Image, ImageEnhance
from ultralytics import YOLO
import random
import uuid

# ------------------ 基本設定 ------------------
DATA_FOLDER = "tourist_data"
IMAGE_FOLDER = os.path.join(DATA_FOLDER, "images")
SURVEY_FILE = os.path.join(DATA_FOLDER, "tourist_survey.xlsx")
os.makedirs(IMAGE_FOLDER, exist_ok=True)


# ------------------ 模型載入 ------------------
yolo_model = YOLO("yolov8n.pt")

# ------------------ 屬性分類器（模擬） ------------------
def dummy_attribute_classifier(image):
    return {
        "Age": random.choice(["Child", "Teen", "Adult", "Senior"]),
        "Gender": random.choice(["Male", "Female"]),
        "Glasses": random.choice(["Yes", "No"]),
        "Upper Wear": random.choice(["T-shirt", "Jacket", "Shirt"]),
        "Lower Wear": random.choice(["Shorts", "Jeans", "Skirt"])
    }

# ------------------ 影像亮度增強 ------------------
def enhance_brightness_pil(image_pil, factor=1.5):
    enhancer = ImageEnhance.Brightness(image_pil)
    return enhancer.enhance(factor)



# ------------------ 問卷儲存 ------------------
def save_survey(data):
    df = pd.DataFrame([data])
    if os.path.exists(SURVEY_FILE):
        old_df = pd.read_excel(SURVEY_FILE)
        df = pd.concat([old_df, df], ignore_index=True)
    df.to_excel(SURVEY_FILE, index=False)

# ------------------ Step 1：拍照 ------------------
def run_camera_pil():
    st.subheader("Step 1: 拍照與亮度調整")

    brightness = st.slider("亮度調整", 1.0, 3.0, 1.5, 0.1)
    img_file_buffer = st.camera_input("請對準鏡頭拍張照")

    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        enhanced_image = enhance_brightness_pil(image, factor=brightness)
        st.image(enhanced_image, caption="增亮後的影像")

        if st.button("📸 拍照並進入問卷"):
            filename = f"person_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            img_path = os.path.join(IMAGE_FOLDER, filename)
            enhanced_image.save(img_path)
            st.session_state["img_path"] = img_path
            st.session_state["step"] = "survey"
            st.rerun()
    else:
        st.info("請先拍張照片")




# ------------------ Step 2：問卷 ------------------
def run_survey():
    st.subheader("Step 2: 問卷填寫與確認")

    img_path = st.session_state.get("img_path")
    if not img_path:
        st.error("⚠️ 沒有照片，請先回到 Step 1 拍照")
        return

    st.image(img_path, caption="你的照片")

    image = Image.open(img_path)
    attrs = dummy_attribute_classifier(image)

    age = st.selectbox("年齡層", ["Child", "Teen", "Adult", "Senior"], index=["Child", "Teen", "Adult", "Senior"].index(attrs["Age"]))
    gender = st.selectbox("性別", ["Male", "Female"], index=["Male", "Female"].index(attrs["Gender"]))
    glasses = st.selectbox("是否配戴眼鏡", ["Yes", "No"], index=["Yes", "No"].index(attrs["Glasses"]))
    upper = st.selectbox("上身服裝", ["T-shirt", "Jacket", "Shirt"], index=["T-shirt", "Jacket", "Shirt"].index(attrs["Upper Wear"]))
    lower = st.selectbox("下身服裝", ["Shorts", "Jeans", "Skirt"], index=["Shorts", "Jeans", "Skirt"].index(attrs["Lower Wear"]))
    activities = st.multiselect("你目前或預計參與的活動：", ["美食/品嚐", "觀光景點", "遊樂/娛樂", "購物", "其他"])
    consent = st.checkbox("✅ 我同意儲存個資與影像")

    if st.button("送出問卷") and consent:
        save_survey({
            "ID": f"record_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "Age": age,
            "Gender": gender,
            "Glasses": glasses,
            "Upper Wear": upper,
            "Lower Wear": lower,
            "Activities": ", ".join(activities),
            "Image Path": img_path,
            "Timestamp": datetime.now()
        })
        st.success("✅ 問卷已提交！謝謝你的參與。")
        st.session_state["step"] = "thank_you"
        st.rerun()

# ------------------ Step 3：感謝畫面 ------------------
def run_thank_you():
    st.subheader("Step 3: 感謝您的參與")
    st.success("🎉 問卷已提交，歡迎下一位使用者！")
    if st.button("開始下一位 ➡️"):
        st.session_state.clear()
        st.session_state["step"] = "camera"
        st.rerun()

# ------------------ 主流程 ------------------
st.set_page_config(page_title="旅遊問卷系統", layout="centered")
st.title("🧳 旅遊問卷與個人屬性辨識")

step = st.session_state.get("step", "camera")

if step == "camera":
    run_camera_pil()
elif step == "survey":
    run_survey()
elif step == "thank_you":
    run_thank_you()




