# 🧳 Tourist Survey System with YOLO + Streamlit

This is a Streamlit-based web application that uses YOLOv8 for real-time person detection via webcam, along with attribute classification (age, gender, glasses, clothing), followed by a short survey. Captured data and images are saved locally.

## Features

- 📸 Real-time webcam capture with YOLOv8 person detection  
- 🧑‍🦱 Attribute classification: Age group, Gender, Glasses, Clothing  
- 📝 Survey form for tourist feedback  
- 💾 Automatically saves images and metadata locally  
- 🌞 Auto brightness enhancement (gamma correction + CLAHE)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/yolo_tourist_survey.git
   cd yolo_tourist_survey

2. pip install -r requirements.txt

3. run the app
   streamlit run yolo_tourist_survey.py

Important: This application is designed to run locally only.
It may not function properly on cloud platforms such as Streamlit Community Cloud due to limitations in webcam access, file saving, and OpenCV usage.

This is a three-step real-time tourist attribute and survey collection app built with **YOLOv8**, **OpenCV**, and **Streamlit**.

It enables:
1. Real-time webcam detection using YOLOv8
2. Automatic attribute classification (age, gender, clothing, glasses)
3. Dynamic form collection for tourist interests
4. Local image saving and Excel-based data logging

---

## 📸 App Demo Flow

1. **Camera Detection & Snapshot**
2. **Attribute Survey**
3. **Thank You Message + Reset**

---

⚙️ Features
✅ Real-time person detection (YOLOv8n)
✅ Brightness enhancement with gamma and CLAHE
✅ Auto-filled survey options (simulated attribute classifier)
✅ Save user data and image locally
✅ Seamless 3-step UI experience

