import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 初步設定 ---
st.set_page_config(page_title="Gemini 3 幾何解題導師", layout="wide", page_icon="⚡")

# 自定義 CSS 讓介面更專業
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #4A90E2; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 側邊欄設定 ---
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735303933135c4210c9.svg", width=50)
    st.title("Gemini 3 Flash 控制台")
    api_key = st.text_input("輸入 Google API Key", type="password")
    
    # 鎖定 Gemini 3 Flash
    model_choice = "gemini-3-flash-preview" 
    st.success(f"當前模型：{model_choice}")
    
    st.divider()
    st.info("💡 **引導模式已啟動**：AI 將優先使用提問方式引導，而非直接給予數值。")

# --- 主畫面設計 ---
st.title("📐 幾何逆向思考學習機")
st.write("上傳幾何題目圖片，由 **Gemini 3 Flash** 帶領你解構難題。")

col_left, col_right = st.columns([1, 1])

with col_left:
    uploaded_file = st.file_uploader("📤 上傳題目截圖", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="待分析題目", use_container_width=True)

with col_right:
    if uploaded_file and api_key:
        genai.configure(api_key=api_key)
        # 初始化模型
        model = genai.GenerativeModel(model_name=model_choice)

        # 建立引導式 Tab
        tab1, tab2, tab3 = st.tabs(["🔍 觀察已知條件", "🧠 逆向邏輯引導", "📝 最終步步解析"])

        with tab1:
            if st.button("分析圖形特徵"):
                with st.spinner("Gemini 3 Flash 正在掃描圖形..."):
                    prompt = "請分析這張幾何圖片，找出所有給定的長度、角度與點的關係（不要解題，只需列出已知條件）。請用條列式呈現。"
                    response = model.generate_content([prompt, image])
                    st.markdown(response.text)

        with tab2:
            if st.button("給予解題提示"):
                with st.spinner("生成引導問題中..."):
                    prompt = """
                    請扮演蘇格拉底式的數學老師，針對這題給出三個引導問題：
                    1. 引導學生觀察角ADC與角B的關係（外角性質）。
                    2. 引導學生觀察三角形EDC的內角（等邊三角形判定）。
                    3. 引導學生思考若要算AC，如何利用直角三角形構建輔助線。
                    請不要給出具體數值，只給思路。
                    """
                    response = model.generate_content([prompt, image])
                    st.info("🧠 試著思考以下問題：")
                    st.markdown(response.text)

        with tab3:
            if st.button("查看完整推導過程"):
                with st.spinner("正在進行深度邏輯推理..."):
                    prompt = "請詳細解析這張幾何題。包含：1.求出AD。2.求出AE與EC。3.構造輔助線。4.使用商高定理求出AC。最後給出正確答案。請使用繁體中文。"
                    response = model.generate_content([prompt, image])
                    st.success("完整的解題邏輯：")
                    st.markdown(response.text)
    else:
        st.warning("請先上傳圖片並在側邊欄填寫 API Key。")

# --- 加強功能：對話式引導 ---
if uploaded_file and api_key:
    st.divider()
    st.subheader("💬 與 AI 老師討論")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt_chat := st.chat_input("老師，為什麼這裡要用外角性質？"):
        st.session_state.messages.append({"role": "user", "content": prompt_chat})
        with st.chat_message("user"):
            st.markdown(prompt_chat)

        with st.chat_message("assistant"):
            chat_response = model.generate_content([f"學生問：{prompt_chat}。請針對這題幾何圖片給予解答與引導。", image])
            st.markdown(chat_response.text)
        st.session_state.messages.append({"role": "assistant", "content": chat_response.text})