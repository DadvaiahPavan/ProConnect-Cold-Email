# AI-Powered Cold Email Generator 📧

A sophisticated application that leverages AI to generate personalized and effective cold emails for job applications and professional networking. Built with Streamlit and powered by Groq's LLM API.

![Cold Email Generator Interface](https://i.ibb.co/18cw3PG/Screenshot-2024-12-16-204621.png)

## 🌟 Features

- **Smart Resume Parsing**: Automatically extracts key information from resumes in various formats (PDF, DOCX, TXT)
- **Job Description Analysis**: Processes job descriptions from URLs or direct text input
- **AI-Powered Email Generation**: Creates personalized emails using advanced LLM technology
- **Email Compliance Checking**: Ensures emails are professional and bias-free
- **Performance Analytics**: Track and analyze email performance metrics
- **Advanced Features**:
  - Skill extraction and matching
  - Data anonymization
  - Email format validation
  - Integration capabilities with LinkedIn and Slack

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Groq API Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/project-genai-cold-email-generator.git
cd project-genai-cold-email-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the app directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### Running the Application

```bash
streamlit run app/main.py
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: 
  - Groq LLM API
  - LangChain
  - Transformers
  - spaCy & NLTK
- **Document Processing**: 
  - PyPDF2
  - python-docx
  - pytesseract
- **Data Analysis**: 
  - pandas
  - scikit-learn
  - plotly

## 📝 Usage

1. **Upload Resume**: Support for PDF, DOCX, and TXT formats
2. **Input Job Details**: Paste job description or provide URL
3. **Customize Email**: 
   - Add recipient name and company
   - Choose email tone
   - Set additional preferences
4. **Generate & Review**: Get AI-generated email with compliance check
5. **Track Performance**: Monitor email effectiveness metrics

## 🔒 Security Features

- Secure API key handling
- Data anonymization capabilities
- Email content compliance checking
- Input validation and sanitization

## 📊 Advanced Analytics

- Email performance tracking
- Engagement metrics
- Success rate analysis
- Visual analytics with Plotly

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Important Notes

- Ensure your Groq API key is properly configured
- Keep your dependencies updated
- Review generated emails before sending
- Follow email best practices and compliance guidelines

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the maintainers.
