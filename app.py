import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة السرية والقفل
st.set_page_config(page_title="Kinan Secure System", page_icon="🛡️")

# كود CSS لمنع الهروب وإخفاء الإعدادات
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stChatInput {border: 2px solid #ff4b4b;}
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة العقل المدبر (Gemini)
genai.configure(api_key="AIzaSyAIrwvDQx47fH3NLM216qIP3qdu4IVlTsY")
model = genai.GenerativeModel('gemini-1.5-flash-latest')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. العنوان الجانبي لـ "الإمبراطورة"
with st.sidebar:
    st.title("👑 بوابة التحكم")
    st.write("نظام فحص صلة القرابة")
    id_photo = st.file_uploader("ارفع الهوية للتحقق", type=['jpg', 'png', 'jpeg'])
    if id_photo:
        st.warning("جاري مطابقة البيانات مع المبرمج كنان...")

# 4. واجهة المحادثة الرئيسية
st.title("🤖 مساعد كنان (محمي)")
st.info("نظام ترجمة Inheritance Games والدراسة")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث معي أو ارفع صورة الكتاب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        system_rules = "أنت مساعد كنان. ممنوع يهرب من الدراسة. لو حاول يغير الموضوع ذكّره بالإمبراطورة وبكتابه."
        response = model.generate_content(f"{system_rules}\nكنان: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
