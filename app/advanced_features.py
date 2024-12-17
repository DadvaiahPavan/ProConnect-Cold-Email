import pytesseract
from pdf2image import convert_from_path
import spacy
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import pandas as pd
import torch
from transformers import pipeline
import re
import email_validator

# Optional import with fallback
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    print("Warning: python-magic not available. File type detection will be limited.")

class AdvancedResumeParser:
    def __init__(self):
        # Load NLP models
        self.nlp = spacy.load('en_core_web_sm')
        nltk.download('punkt')
        
    def ocr_document(self, file_path):
        """
        Perform OCR on complex document layouts
        """
        images = convert_from_path(file_path)
        ocr_text = ""
        for image in images:
            ocr_text += pytesseract.image_to_string(image)
        return ocr_text
    
    def extract_skills(self, text):
        """
        Machine learning-based skill extraction
        """
        # Use spaCy for named entity recognition
        doc = self.nlp(text)
        skills = [ent.text for ent in doc.ents if ent.label_ in ['SKILL', 'TECH']]
        return list(set(skills))
    
    def skill_gap_analysis(self, resume_skills, job_description_skills):
        """
        Analyze skill gaps between resume and job description
        """
        vectorizer = TfidfVectorizer()
        skill_matrix = vectorizer.fit_transform([' '.join(resume_skills), ' '.join(job_description_skills)])
        similarity = cosine_similarity(skill_matrix)[0][1]
        return {
            'match_percentage': similarity * 100,
            'missing_skills': list(set(job_description_skills) - set(resume_skills))
        }

class EmailComplianceChecker:
    def __init__(self):
        self.bias_detector = pipeline('text-classification')
    
    def check_appropriateness(self, email_text):
        """
        AI-powered email appropriateness scoring
        """
        bias_result = self.bias_detector(email_text)
        return {
            'is_appropriate': bias_result[0]['label'] == 'APPROPRIATE',
            'confidence': bias_result[0]['score']
        }
    
    def anonymize_data(self, text):
        """
        Anonymize sensitive information
        """
        # Basic anonymization - can be expanded
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE]', text)
        return text

class EmailPerformanceTracker:
    def __init__(self):
        self.performance_data = []
    
    def log_email_performance(self, email_details):
        """
        Track email performance metrics
        """
        self.performance_data.append(email_details)
    
    def generate_performance_insights(self):
        """
        Generate performance analytics
        """
        df = pd.DataFrame(self.performance_data)
        fig = px.line(df, x='timestamp', y='open_rate', title='Email Performance Over Time')
        return fig

class IntegrationManager:
    def __init__(self):
        # Placeholders for integration services
        self.linkedin_client = None
        self.slack_client = None
    
    def import_linkedin_profile(self, profile_url):
        """
        Import LinkedIn profile data
        """
        # Implement LinkedIn profile scraping
        pass
    
    def send_slack_notification(self, message):
        """
        Send Slack notification
        """
        # Implement Slack notification
        pass

# Utility functions
def validate_email(email):
    """
    Validate email format
    """
    try:
        email_validator.validate_email(email)
        return True
    except email_validator.EmailNotValidError:
        return False

def detect_file_type(file_path):
    """
    Detect file type using magic if available
    """
    if MAGIC_AVAILABLE:
        file_type = magic.from_file(file_path)
        return file_type
    else:
        # Fallback method if magic is not available
        import os
        return os.path.splitext(file_path)[1]
