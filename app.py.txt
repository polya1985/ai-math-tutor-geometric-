import streamlit as st
import google.generativeai as genai
from PIL import Image

# 頁面配置
st.set_page_config(page_title="AI 幾何解題導師", layout="wide")

# Sidebar: 設定區
with st.sidebar:
    st.title("🛠️ 設定中心")
    api_key = st.text_input("輸入 Gemini API Key", type="password")
    model_choice = st.selectbox("選擇模型", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.divider()
    st.info("本系統採引導式教學，不會直接給予答案，旨在培養解題邏輯。")

# 主頁面
st.title("🎓 AI 幾何引導式學習系統")
st.write("上傳幾何題目，讓 AI 帶領你一步步破解難關！")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("選擇題目圖片...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="待解題目", use_column_width=True)

with col2:
    if uploaded_file and api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_choice)
        
        # 定義引導按鈕
        tab1, tab2, tab3 = st.tabs(["💡 知識點分析", "🧠 引導式思考", "📝 詳細解析"])

        with tab1:
            if st.button("分析題目背後的知識點"):
                prompt = "請分析這張幾何題目圖片，列出解題所需的核心知識點（如：外角性質、等腰三角形、勾股定理等），請以條列式呈現，不要直接給出答案。"
                response = model.generate_content([prompt, image])
                st.success("本題涉及的關鍵武器：")
                st.write(response.text)

        with tab2:
            if st.button("給我一點提示（不顯示答案）"):
                prompt = "針對這張幾何題，請設計三個引導學生的問題，帶領他們思考解題路徑，例如：『觀察某個角，你能發現什麼？』，請保持教學導向。"
                response = model.generate_content([prompt, image])
                st.info("思考看看：")
                st.write(response.text)

        with tab3:
            if st.button("查看完整解題步驟"):
                prompt = "請詳細解析這張幾何題。格式要求：1. 求出各關鍵線段與角度。2. 建立輔助線（如有必要）。3. 最後計算答案。請使用繁體中文，並以專業老師的口吻撰寫。"
                response = model.generate_content([prompt, image])
                st.write(response.text)
                st.balloons()
    else:
        st.warning("請先上傳圖片並確保已輸入 API Key。")

# 加強功能：互動 Chatbot
st.divider()
st.subheader("💬 對這題還有疑問？直接問 AI 老師")
user_question = st.text_input("例如：為什麼要作那條輔助線？")
if user_question and uploaded_file:
    # 這裡可以加入對話邏輯
    st.write(f"AI 老師正在解答關於「{user_question}」的問題...")