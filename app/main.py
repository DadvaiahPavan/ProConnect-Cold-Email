import streamlit as st
import os
import sys
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to load environment variables
try:
    # Try loading from .env in the app directory
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
except Exception as e:
    st.warning(f"Could not load .env file: {e}")

# Set USER_AGENT to identify requests
os.environ['USER_AGENT'] = 'ColdEmailGenerator/1.0'

# Function to get API key with multiple fallback methods
def get_groq_api_key():
    # Method 1: Environment variable
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        st.info("")
        return api_key
    
    # Method 2: Streamlit secrets
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        st.info("GROQ API Key loaded from Streamlit secrets")
        return api_key
    except Exception as e:
        st.error(f"Could not load GROQ API Key: {e}")
        st.error("Please set GROQ_API_KEY in environment variables or Streamlit secrets")
        return None

# Add global error handling
def global_exception_handler():
    st.error("An unexpected error occurred. Please check your configuration and try again.")
    st.error("Possible issues:")
    st.error("1. Missing API keys")
    st.error("2. Dependency conflicts")
    st.error("3. Environment configuration problems")

# Function to get API key with multiple fallback methods
def get_groq_api_key():
    # Method 1: Environment variable
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        st.info("GROQ API Key loaded successfully from environment")
        return api_key
    
    # Method 2: Streamlit secrets
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        st.info("GROQ API Key loaded from Streamlit secrets")
        return api_key
    except Exception as e:
        st.error(f"Could not load GROQ API Key: {e}")
        st.error("Please set GROQ_API_KEY in environment variables or Streamlit secrets")
        return None

# Add global error handling
def global_exception_handler():
    st.error("An unexpected error occurred. Please check your configuration and try again.")
    st.error("Possible issues:")
    st.error("1. Missing API keys")
    st.error("2. Dependency conflicts")
    st.error("3. Environment configuration problems")

# Modify create_streamlit_app to include error handling
def create_streamlit_app():
    try:
        # Get Groq API Key
        groq_api_key = get_groq_api_key()
        
        if not groq_api_key:
            st.error("Cannot proceed without a valid Groq API Key")
            return

        st.title("🚀 Advanced Cold Email Generator")
        
        # Initialize advanced feature managers if available
        if ADVANCED_FEATURES_AVAILABLE:
            compliance_checker = EmailComplianceChecker()
            performance_tracker = EmailPerformanceTracker()
            integration_manager = IntegrationManager()
        
        # Sidebar for User Input
        st.sidebar.subheader("Upload Your Resume")
        uploaded_resume = st.sidebar.file_uploader("Choose a PDF or DOCX resume", type=["pdf", "docx"])
        
        # Personalization Inputs
        recipient_name = st.sidebar.text_input("Recipient's Name", placeholder="John Doe")
        company_name = st.sidebar.text_input("Company Name", placeholder="Tech Innovations Inc.")
        sender_name = st.sidebar.text_input("Your Name", placeholder="Your Full Name")
        
        # Job Description Input with Enhanced Options
        st.sidebar.subheader("Job Context")
        job_description_input = st.sidebar.text_area("Job Description", placeholder="Paste job description or URL")
        
        # Email Customization Controls
        st.sidebar.subheader("Email Customization")
        tone_options = ["Professional", "Friendly", "Formal", "Casual"]
        email_tone = st.sidebar.selectbox("Email Tone", tone_options)
        
        # Compliance and Privacy Toggle
        if ADVANCED_FEATURES_AVAILABLE:
            st.sidebar.subheader("Privacy & Compliance")
            anonymize_data = st.sidebar.checkbox("Anonymize Sensitive Information")
        
        # Generate Email Button
        generate_email = st.sidebar.button("Generate Personalized Email")
        
        if generate_email:
            # Process Resume if uploaded
            resume_text = ""
            if uploaded_resume:
                resume_text = extract_text_from_file(uploaded_resume)
                if not resume_text:
                    st.error("Could not extract text from the resume.")
                    return
            
            # Get Job Description
            job_description = get_job_description(job_description_input)
            
            # Compliance Check
            if ADVANCED_FEATURES_AVAILABLE and anonymize_data:
                resume_text = compliance_checker.anonymize_data(resume_text)
                job_description = compliance_checker.anonymize_data(job_description)
            
            # Generate Email Text
            email_text = generate_email_text(
                resume_text, 
                job_description, 
                recipient_name, 
                company_name, 
                email_tone,
                sender_name  # Pass sender name to the function
            )
            
            # Email Appropriateness Check
            if ADVANCED_FEATURES_AVAILABLE:
                compliance_result = compliance_checker.check_appropriateness(email_text)
                
                if not compliance_result['is_appropriate']:
                    st.warning("Generated email may contain inappropriate content.")
            
            # Display Generated Email
            st.subheader("Generated Email")
            st.write(email_text)
            
            # Performance Tracking
            if ADVANCED_FEATURES_AVAILABLE:
                performance_tracker.log_email_performance({
                    'timestamp': pd.Timestamp.now(),
                    'recipient': recipient_name,
                    'company': company_name,
                    'tone': email_tone,
                    'compliance_score': compliance_result.get('confidence', 1.0)
                })
    except Exception as e:
        global_exception_handler()
        st.exception(e)

from langchain_community.document_loaders import WebBaseLoader
import PyPDF2
import docx
import io
import validators
import pandas as pd

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Optional import with fallback for advanced features
try:
    from advanced_features import (
        AdvancedResumeParser, 
        EmailComplianceChecker, 
        EmailPerformanceTracker,
        IntegrationManager,
        validate_email,
        detect_file_type
    )
    ADVANCED_FEATURES_AVAILABLE = True
except ImportError:
    st.warning("Advanced features are not available. Some functionality may be limited.")
    ADVANCED_FEATURES_AVAILABLE = False
    
    # Provide fallback classes
    class AdvancedResumeParser:
        def __init__(self):
            pass
        def extract_skills(self, text):
            return []
    
    class EmailComplianceChecker:
        def check_appropriateness(self, email_text):
            return {'is_appropriate': True, 'confidence': 1.0}
        def anonymize_data(self, text):
            return text
    
    class EmailPerformanceTracker:
        def log_email_performance(self, email_details):
            pass
    
    class IntegrationManager:
        pass

def extract_text_from_file(uploaded_file):
    """
    Enhanced document text extraction with advanced parsing
    """
    try:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Temporary save file for advanced parsing
        with open(uploaded_file.name, 'wb') as f:
            f.write(uploaded_file.getvalue())
        
        # Detect file type and choose appropriate parsing method
        if file_extension == '.pdf':
            # Try standard PDF parsing
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        elif file_extension in ['.docx', '.doc']:
            doc = docx.Document(uploaded_file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        else:
            st.error(f"Unsupported file type: {file_extension}")
            return None
        
        # Extract skills from parsed text if advanced features are available
        if ADVANCED_FEATURES_AVAILABLE:
            parser = AdvancedResumeParser()
            skills = parser.extract_skills(text)
            st.sidebar.write("Extracted Skills:", skills)
        
        return text
    
    except Exception as e:
        st.error(f"Error reading document: {e}")
        return None

def get_job_description(url_or_text):
    """
    Retrieve job description from URL or direct text input.
    """
    if not url_or_text:
        return ""
    
    # Check if input is a valid URL
    if validators.url(url_or_text):
        try:
            loader = WebBaseLoader([url_or_text])
            return clean_text(loader.load().pop().page_content)
        except Exception as e:
            st.warning(f"Could not load job description from URL: {e}")
            return ""
    
    # If not a URL, treat as direct text input
    return url_or_text

def generate_email_text(resume_text, job_description, recipient_name, company_name, email_tone, sender_name=None):
    """
    Generate personalized email text based on input parameters
    """
    # Initialize Chain and Portfolio
    chain = Chain()
    portfolio = Portfolio()
    
    # Combine Context
    full_context = f"""
    Job Context:
    - Recipient Name: {recipient_name}
    - Company: {company_name}
    - Job Description: {job_description}
    
    Resume Summary: {resume_text[:1000]}  # Limit to first 1000 chars
    """
    
    # Portfolio Preparation
    portfolio.load_portfolio()
    
    # Extract Skills
    skills = chain.extract_skills(full_context)
    
    # Find Relevant Portfolio Links
    links = portfolio.query_links(skills)
    
    # Generate Email
    email = chain.write_personalized_mail(
        context=full_context, 
        job_description=job_description, 
        links=links,
        tone=email_tone,
        sender_name=sender_name  # Pass sender name to the method
    )
    
    return email

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Advanced Cold Email Generator", page_icon="📧")
    create_streamlit_app()
