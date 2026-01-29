import json
from sentence_transformers import SentenceTransformer, util
import torch

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')


def load_job_descriptions():
    """Load job descriptions from JSON file"""
    try:
        with open('data/job_descriptions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Job descriptions file not found!")
        return {}


def calculate_semantic_similarity(resume_text, job_description):
    """Calculate semantic similarity between resume and job description"""
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    
    similarity = util.cos_sim(resume_embedding, job_embedding)
    
    match_percentage = round(float(similarity[0][0]) * 100, 2)
    
    return match_percentage


def calculate_skill_match(user_skills, required_skills):
    """Calculate percentage of required skills that user has"""
    if not required_skills:
        return 0
    
    user_skills_lower = [skill.lower().strip() for skill in user_skills]
    required_skills_lower = [skill.lower().strip() for skill in required_skills]
    
    matched_skills = []
    for skill in required_skills_lower:
        if skill in user_skills_lower:
            matched_skills.append(skill)
    
    match_percentage = (len(matched_skills) / len(required_skills_lower)) * 100
    
    return round(match_percentage, 2), matched_skills


def identify_missing_skills(user_skills, required_skills):
    """Identify skills that are required but not in user's resume"""
    user_skills_lower = set(skill.lower().strip() for skill in user_skills)
    required_skills_lower = set(skill.lower().strip() for skill in required_skills)
    
    missing_skills = required_skills_lower - user_skills_lower
    
    return list(missing_skills)


def categorize_skills(skills):
    """Categorize skills into different categories"""
    categories = {
        'Programming Languages': [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 
            'swift', 'kotlin', 'go', 'rust', 'typescript', 'r', 'scala'
        ],
        'Web Development': [
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
            'django', 'flask', 'spring', 'bootstrap', 'tailwind', 'sass',
            'webpack', 'next.js', 'responsive design'
        ],
        'Databases': [
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'oracle',
            'redis', 'elasticsearch'
        ],
        'Machine Learning & AI': [
            'machine learning', 'deep learning', 'ai', 'nlp', 'computer vision',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'neural networks',
            'cnn', 'rnn', 'lstm', 'transformer'
        ],
        'Data Science': [
            'pandas', 'numpy', 'statistics', 'data visualization', 'tableau',
            'power bi', 'spark', 'hadoop', 'big data'
        ],
        'DevOps & Cloud': [
            'docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'gcp',
            'terraform', 'ansible', 'ci/cd', 'linux', 'bash'
        ],
        'Design': [
            'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
            'ux', 'ui', 'wireframing', 'prototyping'
        ],
        'Tools & Others': [
            'git', 'github', 'jira', 'agile', 'scrum', 'rest api',
            'graphql', 'testing', 'selenium'
        ]
    }
    
    categorized = {}
    skills_lower = [s.lower() for s in skills]
    
    for category, keywords in categories.items():
        matched = [skill for skill in skills_lower if skill in keywords]
        if matched:
            categorized[category] = matched
    
    return categorized


def get_learning_resources(missing_skills, job_title):
    """Get learning resources for missing skills"""
    job_data = load_job_descriptions()
    
    if job_title not in job_data:
        return {}
    
    resources = job_data[job_title].get('resources', {})
    
    relevant_resources = {}
    for skill in missing_skills:
        if skill in resources:
            relevant_resources[skill] = resources[skill]
    
    return relevant_resources


def analyze_resume_for_job(resume_data, job_title):
    """Main function to analyze resume against job requirements"""
    job_descriptions = load_job_descriptions()
    
    if job_title not in job_descriptions:
        return {
            'error': f'Job title "{job_title}" not found in database.'
        }
    
    job_data = job_descriptions[job_title]
    job_description = job_data['description']
    required_skills = job_data['required_skills']
    
    # Calculate semantic similarity
    semantic_match = calculate_semantic_similarity(
        resume_data['cleaned_text'],
        job_description
    )
    
    # Calculate skill-based match
    skill_match, matched_skills = calculate_skill_match(
        resume_data['skills'],
        required_skills
    )
    
    # Identify missing skills
    missing_skills = identify_missing_skills(
        resume_data['skills'],
        required_skills
    )
    
    # Categorize user skills
    categorized_user_skills = categorize_skills(resume_data['skills'])
    
    # Categorize missing skills
    categorized_missing_skills = categorize_skills(missing_skills)
    
    # Get learning resources
    learning_resources = get_learning_resources(missing_skills, job_title)
    
    # Calculate overall match (weighted average)
    overall_match = round((semantic_match * 0.4 + skill_match * 0.6), 2)
    
    return {
        'job_title': job_title,
        'overall_match': overall_match,
        'semantic_match': semantic_match,
        'skill_match': skill_match,
        'total_required_skills': len(required_skills),
        'matched_skills_count': len(matched_skills),
        'missing_skills_count': len(missing_skills),
        'matched_skills': sorted(matched_skills),
        'missing_skills': sorted(missing_skills),
        'user_skills': sorted(resume_data['skills']),
        'categorized_user_skills': categorized_user_skills,
        'categorized_missing_skills': categorized_missing_skills,
        'learning_resources': learning_resources,
        'job_description': job_description
    }


if __name__ == "__main__":
    # Test the matcher
    sample_resume_data = {
        'cleaned_text': 'Data Scientist with experience in Python, SQL, and machine learning.',
        'skills': ['python', 'sql', 'machine learning', 'pandas']
    }
    
    result = analyze_resume_for_job(sample_resume_data, 'Data Scientist')
    print("Overall Match:", result['overall_match'], "%")
    print("Missing Skills:", result['missing_skills'])