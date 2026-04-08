import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة والاسم اللي بيظهر على الشاشة
st.set_page_config(page_title="مساعد كنان", layout="centered")

st.title("مساعد كنان 🤖 (محمي)")
st.caption("نظام ترجمة والدراسة لـ Inheritance Games")

# خانة إدخال المفتاح السري - عشان يشتغل التطبيق
api_key = st.text_input("أدخل مفتاح Gemini لبدء التشغيل:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        user_input = st.chat_input("تحدث معي أو ارفع صورة الكتاب...")
        
        if user_input:
            response = model.generate_content(user_input)
            st.write(response.text)
            
    except Exception as e:
        st.error(f"حدث خطأ في المفتاح: {e}")
else:
    st.warning("يرجى إدخال المفتاح السري (API Key) في الخانة أعلاه لتفعيل التطبيق.")
