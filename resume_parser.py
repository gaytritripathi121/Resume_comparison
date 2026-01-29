import re
from pdfminer.high_level import extract_text
from docx import Document
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Common tech skills keywords (expanded list)
SKILL_KEYWORDS = {
    'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
    'go', 'rust', 'typescript', 'r', 'matlab', 'scala', 'perl',
    'html', 'css', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'oracle',
    'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
    'machine learning', 'deep learning', 'ai', 'nlp', 'computer vision',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
    'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
    'aws', 'azure', 'gcp', 'cloud', 'devops', 'ci/cd',
    'rest api', 'graphql', 'microservices', 'agile', 'scrum',
    'linux', 'unix', 'bash', 'shell', 'powershell',
    'tableau', 'power bi', 'excel', 'data visualization',
    'spark', 'hadoop', 'kafka', 'redis', 'elasticsearch',
    'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
    'ux', 'ui', 'wireframing', 'prototyping', 'user research',
    'terraform', 'ansible', 'puppet', 'chef',
    'monitoring', 'prometheus', 'grafana', 'elk',
    'security', 'networking', 'vpn', 'firewall',
    'jira', 'confluence', 'slack', 'trello',
    'testing', 'junit', 'pytest', 'selenium', 'jest',
    'webpack', 'babel', 'npm', 'yarn',
    'responsive design', 'bootstrap', 'tailwind', 'sass', 'less',
    'redux', 'mobx', 'vuex', 'next.js', 'nuxt.js',
    'mlops', 'model deployment', 'feature engineering',
    'neural networks', 'cnn', 'rnn', 'lstm', 'transformer',
    'statistics', 'probability', 'mathematics', 'algorithms',
    'data structures', 'object-oriented programming', 'functional programming',
    'api', 'json', 'xml', 'yaml', 'regex'
}


def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""


def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""


def clean_text(text):
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep important punctuation
    text = re.sub(r'[^\w\s\.\,\-\+\#]', ' ', text)
    return text.strip()


def extract_skills(text):
    """Extract skills from text using keyword matching and NLP"""
    text_lower = text.lower()
    found_skills = set()
    
    # Method 1: Direct keyword matching
    for skill in SKILL_KEYWORDS:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
    
    # Method 2: Multi-word phrase detection
    # Handle special cases like "machine learning", "deep learning", etc.
    multi_word_skills = [
        'machine learning', 'deep learning', 'computer vision',
        'natural language processing', 'nlp', 'data science',
        'data visualization', 'web development', 'mobile development',
        'cloud computing', 'artificial intelligence', 'big data',
        'user experience', 'user interface', 'responsive design',
        'rest api', 'feature engineering', 'model deployment',
        'neural networks', 'object-oriented programming',
        'functional programming', 'data structures'
    ]
    
    for skill in multi_word_skills:
        if skill in text_lower:
            found_skills.add(skill)
    
    # Method 3: Using spaCy for entity recognition (optional enhancement)
    doc = nlp(text[:1000000])  # Limit text size for performance
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE']:
            skill_text = ent.text.lower()
            if skill_text in SKILL_KEYWORDS:
                found_skills.add(skill_text)
    
    return list(found_skills)


def extract_email(text):
    """Extract email from resume"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None


def extract_phone(text):
    """Extract phone number from resume"""
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    return phones[0] if phones else None


def parse_resume(file_path):
    """Main function to parse resume and extract information"""
    # Determine file type and extract text
    if file_path.lower().endswith('.pdf'):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        raw_text = extract_text_from_docx(file_path)
    else:
        return {
            'error': 'Unsupported file format. Please upload PDF or DOCX.'
        }
    
    if not raw_text:
        return {
            'error': 'Could not extract text from file.'
        }
    
    # Clean text
    cleaned_text = clean_text(raw_text)
    
    # Extract information
    skills = extract_skills(cleaned_text)
    email = extract_email(cleaned_text)
    phone = extract_phone(cleaned_text)
    
    return {
        'raw_text': raw_text,
        'cleaned_text': cleaned_text,
        'skills': skills,
        'email': email,
        'phone': phone,
        'skill_count': len(skills)
    }


if __name__ == "__main__":
    # Test the parser
    test_file = "sample_resume.pdf"
    result = parse_resume(test_file)
    print("Extracted Skills:", result.get('skills', []))
    print("Email:", result.get('email'))
    print("Phone:", result.get('phone'))