# Resume & Skill Gap Analyzer 

An AI-powered web application that analyzes resumes against job requirements, identifies skill gaps, and provides personalized learning recommendations.

##  Features

- **Resume Upload**: Support for PDF and DOCX formats
- **Job Matching**: Compare resume against 5+ job roles (Data Scientist, Web Developer, ML Engineer, etc.)
- **Skill Gap Analysis**: Identify missing skills with categorization
- **Match Scoring**: Get overall match percentage with detailed breakdown
- **Learning Resources**: Receive curated course recommendations for missing skills
- **Beautiful UI**: Clean, interactive Streamlit interface


##  Requirements

```txt
streamlit
pdfminer.six
python-docx
scikit-learn
```

##  Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

##  Project Structure

```
resume-analyzer/
├── streamlit_app.py          # Main Streamlit application
├── resume_parser.py           # Resume text extraction & skill parsing
├── job_matcher.py             # Job matching algorithm
├── data/
│   └── job_descriptions.json  # Job requirements database
├── requirements.txt           # Python dependencies
└── README.md
```

##  How It Works

1. **Upload Resume**: User uploads their resume (PDF/DOCX)
2. **Select Job**: Choose target job title from dropdown
3. **AI Analysis**: 
   - Extracts skills using regex pattern matching
   - Compares with job requirements using TF-IDF similarity
   - Calculates match percentage
4. **Get Results**: View detailed breakdown with missing skills and learning resources

##  Technologies Used

- **Streamlit**: Interactive web interface
- **Scikit-learn**: Text similarity (TF-IDF)
- **PDFMiner**: PDF text extraction
- **Python-docx**: Word document processing

##  Supported Job Titles

- Data Scientist
- Web Developer
- Machine Learning Engineer
- UI/UX Designer
- DevOps Engineer

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

##  License

MIT License - feel free to use this project for learning or personal use.



##  Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Job descriptions curated from industry standards

---

**Note**: This project uses client-side processing. No data is stored or transmitted to external servers.
