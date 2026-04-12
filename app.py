import streamlit as st
import google.generativeai as genai

# إعداد واجهة التطبيق
st.set_page_config(page_title="مساعد كنان", layout="centered")

st.title("مساعد كنان 🤖")
st.caption("نظامك الخاص للترجمة والدراسة")

# خانة إدخال المفتاح السري الجديد
api_key = st.text_input("أدخل مفتاح Gemini الجديد:", type="password")

if api_key:
    try:
        # ربط المفتاح بالنظام
        genai.configure(api_key=api_key)
        
        # اختيار الموديل الصحيح والمستقر (هذا السطر هو الحل)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # إنشاء ذاكرة للمحادثة
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # عرض الرسائل السابقة
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # استقبال سؤال جديد
        if prompt := st.chat_input("تحدث معي يا كنان..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # الحصول على رد الذكاء الاصطناعي
            response = model.generate_content(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"تأكد من لصق المفتاح الجديد بشكل صحيح. الخطأ: {e}")
else:
    st.info("انسخ المفتاح الجديد من AI Studio والحقه هنا!")
