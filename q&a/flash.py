from dotenv import load_dotenv
load_dotenv()

# for x in genai.list_models():
#     print(x.name)

import streamlit  as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro Model and get response
model = genai.GenerativeModel('gemini-1.5-flash')


def get_gemini_response(input,image):
    if input !="":
        response=model.generate_content([input,image])
    else:
        response=model.generate_content(image)
    return response.text


st.set_page_config("Geminni Image Demo")
st.header("Gemini Application")
input=st.text_input("input prompt: ",key="input")

# Create a file uploader section that accepts only image files
uploaded_image = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
img=""
# Check if an image file is uploaded
if uploaded_image is not None:
    st.success(f"Image '{uploaded_image.name}' uploaded successfully!")

    # Open the uploaded image file
    img = Image.open(uploaded_image)
    
    # Display the image in the app
    st.image(img, caption=f"Uploaded Image: {uploaded_image.name}", use_column_width=True)
else:
    st.info("Please upload an image file.")

submit=st.button("Tell me about the image")


## if submit is clicked
if submit:
    response=get_gemini_response(input,img)
    st.subheader("The response is...")
    st.write(response)

