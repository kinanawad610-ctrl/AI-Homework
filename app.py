import streamlit as st
import google.generativeai as genai
import random

st.set_page_config(page_title="مساعد كنان", layout="centered")

st.title("مساعد كنان 🤖")

# النظام يسحب المفتاح من الأسرار تلقائياً
if "GEMINI_KEYS" in st.secrets:
    keys = st.secrets["GEMINI_KEYS"]
    api_key = random.choice(keys) if isinstance(keys, list) else keys
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("تحدث معي يا كنان..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            response = model.generate_content(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("الموقع مضغوط، جرب مرة أخرى.")
else:
    st.info("جاري إعداد النظام... يرجى الانتظار")
