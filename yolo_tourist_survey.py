 # py code beginning

import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime
from PIL import Image
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
def enhance_brightness(image, gamma_value=1.5):
    inv_gamma = 1.0 / gamma_value
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(256)]).astype("uint8")
    image = cv2.LUT(image, table)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced = cv2.merge((cl, a, b))
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

# ------------------ 問卷儲存 ------------------
def save_survey(data):
    df = pd.DataFrame([data])
    if os.path.exists(SURVEY_FILE):
        old_df = pd.read_excel(SURVEY_FILE)
        df = pd.concat([old_df, df], ignore_index=True)
    df.to_excel(SURVEY_FILE, index=False)

# ------------------ Step 1：拍照 ------------------
def run_camera():
    st.subheader("Step 1: 即時人員偵測與拍照")

    brightness = st.slider("亮度調整 (Gamma)", 1.0, 3.0, 1.5, 0.1)

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        st.error("⚠️ 無法開啟攝影機")
        return

    frame = enhance_brightness(frame, gamma_value=brightness)
    results = yolo_model(frame[..., ::-1], classes=[0])

    face_crop = None
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            if conf > 0.5:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                face_crop = frame[y1:y2, x1:x2]

    st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", caption="即時影像")

    if face_crop is not None:
        if st.button("📸 拍照並進入問卷"):
            filename = f"person_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            img_path = os.path.join(IMAGE_FOLDER, filename)
            cv2.imwrite(img_path, face_crop)
            st.session_state["img_path"] = img_path
            st.session_state["step"] = "survey"
            st.rerun()
    else:
        st.info("請將人臉對準鏡頭再拍照")

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
    run_camera()
elif step == "survey":
    run_survey()
elif step == "thank_you":
    run_thank_you()




