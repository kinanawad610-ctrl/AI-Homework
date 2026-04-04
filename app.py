import streamlit as st
import google.generativeai as genai
import PIL.Image

# إعداد الموقع
st.set_page_config(page_title="مساعد كنان للواجبات", page_icon="📚")
st.title("📚 مساعد الواجبات الذكي - كنان")
st.write("أهلاً بكِ يا أمي! ارفعي صورة الواجب هنا وسأحلها لكِ فوراً.")

# إعداد المفتاح
genai.configure(api_key="AIzaSyAIrwvDQx47fH3NLM216qIP3qdu4IVlTsY")
model = genai.GenerativeModel('gemini-1.5-flash')

# رفع الصورة
uploaded_file = st.file_uploader("اضغطي هنا لاختيار صورة الواجب", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    st.image(image, caption='تم رفع الصورة بنجاح!')
    
    if st.button('عرض الحل والشرح'):
        with st.spinner('جاري الحل...'):
            response = model.generate_content(["حل هذا الواجب بالتفصيل وبالعربي وبشرح مبسط للأمهات", image])
            st.success("تم الحل!")
            st.write(response.text)
          
