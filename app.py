import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="مساعد كنان", layout="centered")

st.title("مساعد كنان 🤖")
st.caption("نظامك الخاص للترجمة والدراسة")

api_key = st.text_input("أدخل مفتاح Gemini الجديد:", type="password")

if api_key:
    try:
        # الإعداد الأساسي
        genai.configure(api_key=api_key)
        
        # التعديل الجوهري هنا لحل خطأ 404
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("اسألني أي شيء..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # استدعاء الموديل مباشرة عند الضغط
            model = genai.GenerativeModel('gemini-pro') 
            response = model.generate_content(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
else:
    st.info("انسخ المفتاح الجديد من AI Studio والحقه هنا!")
