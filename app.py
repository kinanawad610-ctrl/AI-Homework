import streamlit as st
import google.generativeai as genai
import random
import time

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="مساعد كنان الذكي", page_icon="🤖", layout="centered")

# تحسين مظهر الدردشة بـ CSS بسيط
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; }
    .stChatInput { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 مساعد كنان الذكي")
st.caption("النسخة المطورة المستقرة")
st.markdown("---")

# 2. نظام إدارة المفاتيح الذكي
if "GEMINI_KEYS" in st.secrets:
    keys_list = st.secrets["GEMINI_KEYS"]
    if isinstance(keys_list, str): keys_list = [keys_list]

    # تهيئة الذاكرة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. معالجة الإدخال
    if prompt := st.chat_input("اسألني أي شيء يا بطل..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            # محاولة التنقل بين المفاتيح في حال فشل أحدها
            success = False
            random.shuffle(keys_list) # خلط المفاتيح لضمان التوزيع العادل
            
            for key in keys_list:
                try:
                    genai.configure(api_key=key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    with st.spinner("جاري التفكير..."):
                        response = model.generate_content(prompt)
                        full_response = response.text
                        placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        success = True
                        break # اخرج من الحلقة إذا نجح الرد
                except Exception:
                    continue # إذا فشل مفتاح، انتقل فوراً للمفتاح اللي بعده
            
            if not success:
                st.error("الموقع عليه ضغط كبير حالياً، يرجى إعادة إرسال الرسالة بعد ثوانٍ.")
else:
    st.warning("⚠️ يرجى إضافة المفاتيح في إعدادات Secrets للبدء.")
