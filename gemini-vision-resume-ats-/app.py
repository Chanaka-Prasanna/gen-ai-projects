import base64
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
from PIL import Image
import pdf2image 
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page configuration with light theme and pink accent
st.set_page_config(
    page_title="Resume ATS Scanner",
    page_icon="📄",
    layout="wide",
)

# Custom CSS for light mode with pink primary color
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Headers and text styling */
    h1, h2, h3 {
        color: #FF4B91;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Custom button styling */
        /* Custom button styling */
    .stButton>button {
        background-color: #FF4B91;
        color: white !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 500;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        width: 100%;
        margin-bottom: 10px;
    }
    
    .stButton>button:hover {
        background-color: #FF69B4;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
        color: white !important;
    }
    
    .stButton>button:active, .stButton>button:focus, .stButton>button:visited {
        color: white !important;
        background-color: #FF4B91;
    }
    
    /* Fix text input and textarea background */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Fix file uploader background */
    .stFileUploader>div {
        background-color: #ffffff !important;
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 2px dashed #FF4B91;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #FFB6C1;
    }
    
    /* Card-like container for sections */
    .card {
        background-color: #FAFAFA;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Success message */
    .success-message {
        background-color: #E6F7FF;
        color: #006699;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #FF4B91;
    }
    
    /* Response container */
    .response-container {
        background-color: #F8F8F8;
        border-left: 4px solid #FF4B91;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel(model_name='gemini-2.0-flash')
    response =  model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_image):
    if uploaded_image is not None:
        images = pdf2image.convert_from_bytes(uploaded_image.read())
        first_page =  images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr= img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode()

            }
        ]
        return pdf_parts

    else:
        raise FileNotFoundError("File not found. Please upload a PDF file.")

# App Header with modern styling
# Use an image instead of text for the header
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <img src="https://raw.githubusercontent.com/streamlit/streamlit/master/frontend/public/favicon.png" width="50">
    <h1 style='color: #FF4B91; margin-top: 10px;'>ATS Resume Scanner</h1>
    <p style='color: #666;'>Optimize your resume for Applicant Tracking Systems</p>
</div>
""", unsafe_allow_html=True)

# Create a two-column layout
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("<div class='card' style='background-color: #f8f9fa;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #FF4B91;'>📋 Job Description</h3>", unsafe_allow_html=True)
    input = st.text_area("Paste the job description here:", height=200, key='input', 
                        help="Enter the job description you want to match your resume against")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card' style='background-color: #f8f9fa;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #FF4B91;'>📤 Upload Resume</h3>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("Upload your resume (PDF format)", type=["pdf"], 
                                    help="We'll analyze the first page of your resume")
    
    if uploaded_image is not None:
        st.markdown("<div class='success-message'>✅ Resume uploaded successfully!</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card' style='background-color: #f8f9fa;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #FF4B91;'>🔍 Analysis Options</h3>", unsafe_allow_html=True)
    st.markdown("Choose an analysis option below:")
    
    # Buttons in a column instead of a row
    submit1 = st.button("📊 Resume Analysis")
    submit2 = st.button("📈 Improvement Tips")
    submit3 = st.button("🎯 Match Score")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Create input prompts
input_prompt1 = """
    You are a senior HR professional with expertise in tech hiring. Carefully analyze the candidate's resume in relation to the provided job description.

    - Provide an overview of the candidate's experience and qualifications.
    - Identify the key technical and soft skills the candidate possesses.
    - Mention notable achievements, certifications, or projects if any.
    - Comment on the overall structure and clarity of the resume.

    Make your evaluation detailed but easy to understand. Use bullet points where needed.
"""

input_prompt2 = """
    Act like a hiring manager at a top tech firm. Evaluate the resume for improvement opportunities in terms of:

    - Missing keywords or relevant skills based on the job description.
    - Unclear or weak sections in the resume (e.g., summary, experience, education).
    - Suggestions to improve formatting, structure, or readability.
    - How to better tailor the resume to match the job description.

    Give actionable suggestions and specific wording changes where possible.
"""

input_prompt3 = """
    You are an advanced ATS (Applicant Tracking System) with deep ATS functionality. Compare the resume with the given job description.

    Output only:
    1. A percentage match score based on skills, experience, and education.
    2. A bullet list of missing or weak points from the resume in relation to the job description.

    Avoid detailed analysis or personal opinions. Just give the score and what's missing, and missing keywords.

    Use this equation to calculate the score:
    \text{ATS Match Score (\%)} = \left( \frac{K_{\text{resume}}}{K_{\text{job}}} \right) \times 100

    K_job: Number of important keywords in the job description

    K_resume: Number of those keywords actually found in the resume
    """

# Add response container at the bottom
st.markdown("<div class='card' style='background-color: #f8f9fa;'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #FF4B91;'>🚀 Results</h3>", unsafe_allow_html=True)

if submit1 or submit2 or submit3:
    if uploaded_image is not None and input:
        try:
            pdf_content = input_pdf_setup(uploaded_image)
            
            if submit1:
                response = get_gemini_response(input, pdf_content, input_prompt1)
                st.markdown("<h4 style='color: #FF4B91;'>📊 Resume Analysis</h4>", unsafe_allow_html=True)
            elif submit2:
                response = get_gemini_response(input, pdf_content, input_prompt2)
                st.markdown("<h4 style='color: #FF4B91;'>📈 How to Improve Your Resume</h4>", unsafe_allow_html=True)
            elif submit3:
                response = get_gemini_response(input, pdf_content, input_prompt3)
                st.markdown("<h4 style='color: #FF4B91;'>🎯 ATS Match Score</h4>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='response-container' style='background-color: white; color:black'>{response}</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    elif not uploaded_image:
        st.error("Please upload your resume PDF file.")
    elif not input:
        st.error("Please enter a job description.")
else:
    st.info("Upload your resume and job description, then select an analysis option to get started.")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px; margin-top: 30px; font-size: 0.8em;'>
    Powered by Gemini 2.0 | Resume ATS Scanner © 2025
</div>
""", unsafe_allow_html=True)