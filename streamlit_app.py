import streamlit as st
import os
from resume_parser import parse_resume
from job_matcher import analyze_resume_for_job, load_job_descriptions

st.set_page_config(page_title="Resume Analyzer", page_icon="🧾", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .score-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f8f9fa;
        text-align: center;
    }
    .skill-tag {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        background: #667eea;
        color: white;
        border-radius: 15px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🧾 Resume & Skill Gap Analyzer</h1>
    <p>Upload your resume and discover your perfect career match</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Instructions")
    st.write("1. Upload your resume (PDF/DOCX)")
    st.write("2. Select target job title")
    st.write("3. Click 'Analyze Resume'")
    st.write("4. View your results!")
    
    st.divider()
    st.info("💡 Tip: Make sure your resume includes technical skills and experience")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload Resume", type=['pdf', 'docx'])

with col2:
    job_titles = list(load_job_descriptions().keys())
    selected_job = st.selectbox("Select Job Title", options=job_titles)

if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
    if uploaded_file is None:
        st.error("⚠️ Please upload a resume file")
    elif not selected_job:
        st.error("⚠️ Please select a job title")
    else:
        with st.spinner("🔄 Analyzing your resume..."):
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Parse resume
            resume_data = parse_resume(temp_path)
            
            # Clean up temp file
            os.remove(temp_path)
            
            if 'error' in resume_data:
                st.error(f"❌ {resume_data['error']}")
            else:
                # Analyze
                results = analyze_resume_for_job(resume_data, selected_job)
                
                if 'error' in results:
                    st.error(f"❌ {results['error']}")
                else:
                    st.success("✅ Analysis Complete!")
                    
                    # Display results
                    st.divider()
                    st.header(f"📊 Results for {selected_job}")
                    
                    # Score cards
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Overall Match", f"{results['overall_match']}%")
                    with col2:
                        st.metric("Semantic Match", f"{results['semantic_match']}%")
                    with col3:
                        st.metric("Skill Match", f"{results['skill_match']}%")
                    with col4:
                        st.metric("Skills Found", 
                                f"{results['matched_skills_count']}/{results['total_required_skills']}")
                    
                    # Progress bars
                    st.subheader("📈 Match Breakdown")
                    st.progress(results['overall_match']/100)
                    
                    # Skills comparison
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("✅ Your Skills")
                        if results['categorized_user_skills']:
                            for category, skills in results['categorized_user_skills'].items():
                                st.write(f"**{category}**")
                                for skill in skills:
                                    st.markdown(f'<span class="skill-tag">{skill}</span>', 
                                              unsafe_allow_html=True)
                        else:
                            st.info("No skills detected")
                    
                    with col2:
                        st.subheader("⚠️ Missing Skills")
                        if results['categorized_missing_skills']:
                            for category, skills in results['categorized_missing_skills'].items():
                                st.write(f"**{category}**")
                                for skill in skills:
                                    st.markdown(f'<span class="skill-tag">{skill}</span>', 
                                              unsafe_allow_html=True)
                        else:
                            st.success("🎉 You have all required skills!")
                    
                    # Learning resources
                    if results['learning_resources']:
                        st.divider()
                        st.subheader("📚 Recommended Learning Resources")
                        
                        cols = st.columns(3)
                        for idx, (skill, url) in enumerate(results['learning_resources'].items()):
                            with cols[idx % 3]:
                                st.markdown(f"""
                                <div style="padding: 1rem; background: #f8f9fa; 
                                     border-radius: 10px; margin-bottom: 1rem;">
                                    <h4>{skill.title()}</h4>
                                    <a href="{url}" target="_blank">Start Learning →</a>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Job description
                    st.divider()
                    st.subheader("💼 Job Description")
                    st.info(results['job_description'])

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Built with Streamlit, spaCy, and Sentence Transformers
</div>
""", unsafe_allow_html=True)