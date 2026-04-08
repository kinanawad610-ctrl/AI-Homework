import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة والاسم
st.set_page_config(page_title="مساعد كنان", layout="centered")

st.title("مساعد كنان 🤖 (محمي)")
st.caption("نظام الدراسة والترجمة الخاص بكنان")

# خانة المفتاح السري
api_key = st.text_input("أدخل مفتاح Gemini لبدء التشغيل:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # استخدمنا gemini-pro لأنه الأضمن حالياً
        model = genai.GenerativeModel('gemini-pro')
        
        # مكان الدردشة
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("تحدث معي أو ارفع صورة الكتاب..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            response = model.generate_content(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
else:
    st.warning("يرجى إدخال المفتاح السري (API Key) في الخانة أعلاه لتفعيل التطبيق.")
