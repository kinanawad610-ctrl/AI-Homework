import streamlit as st
import google.generativeai as genai
import random

# 1. إعدادات المتصفح الاحترافية
st.set_page_config(
    page_title="مساعد كنان الذكي",
    page_icon="🤖",
    layout="centered"
)

# 2. تصميم الواجهة (أفضل وأوضح)
st.title("🤖 مساعد كنان الذكي")
st.markdown("---")

# 3. نظام "الخزنة السرية" الذكي
if "GEMINI_KEYS" in st.secrets:
    keys_list = st.secrets["GEMINI_KEYS"]
    
    # التأكد أن المفاتيح في قائمة جاهزة للتوزيع
    if isinstance(keys_list, str):
        keys_list = [keys_list]

    # 4. نظام ذاكرة المحادثة (عشان يتذكر الكلام السابق)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الدردشة بشكل أنيق
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. منطقة إدخال الأسئلة
    if prompt := st.chat_input("اسألني أي شيء يا بطل..."):
        # عرض سؤال المستخدم فوراً
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # اختيار أسرع مفتاح متوفر حالياً (Random Load Balancing)
            selected_key = random.choice(keys_list)
            genai.configure(api_key=selected_key)
            
            # استخدام أقوى وأسرع محرك (Gemini 1.5 Flash)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # توليد الرد مع خاصية الانتظار
            with st.spinner("جاري جلب أفضل إجابة..."):
                response = model.generate_content(prompt)
                
                if response.text:
                    with st.chat_message("assistant"):
                        st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("عذراً، لم أستطع توليد رد، حاول مرة أخرى.")
        
        except Exception as e:
            st.error("الموقع عليه ضغط كبير حالياً بسبب كثرة الزوار، يرجى المحاولة بعد قليل.")
else:
    # تنبيه في حال نسيت وضع المفتاح في Secrets
    st.warning("⚠️ نظام 'الأسرار' غير مفعل. يرجى إضافة GEMINI_KEYS في الإعدادات.")
