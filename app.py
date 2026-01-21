import streamlit as st
import google.generativeai as genai

# 1. Setup - Paste your API Key here
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# 2. Automatically find the best available model
@st.cache_resource
def get_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # We prefer 1.5-flash, then 1.5-pro, then gemini-pro
    for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
        if preferred in available_models:
            return genai.GenerativeModel(preferred)
    # If none of those are found, just take the first one available
    return genai.GenerativeModel(available_models[0])

try:
    model = get_model()
    model_name = model.model_name
except Exception as e:
    st.error(f"Could not find any models: {e}")
    st.stop()

# 3. User Interface
st.set_page_config(page_title="AI Resume Builder", page_icon="📝")
st.title("🚀 AI Resume & Portfolio Builder")
st.caption(f"Connected using model: {model_name}")

name = st.text_input("Full Name")
job_title = st.text_input("Target Job Title")
raw_experience = st.text_area("What did you do? (Simple words)")

if st.button("Generate Resume Content"):
    if raw_experience:
        try:
            with st.spinner('Generating...'):
                prompt = f"Rewrite this for a professional resume using Google XYZ formula: {raw_experience}. Target Job: {job_title}"
                response = model.generate_content(prompt)
                
                st.success("Professional Bullet Points:")
                st.write(response.text)
                
                st.divider()
                st.subheader("💻 Portfolio Bio")
                bio_response = model.generate_content(f"Write a 2-sentence professional bio for {name}, a {job_title}.")
                st.info(bio_response.text)
        except Exception as e:
            st.error(f"AI Error: {e}")
    else:

        st.warning("Please enter your experience.")
