from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import json

from resume_parser import parse_resume
from job_matcher import analyze_resume_for_job, load_job_descriptions

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    job_titles = list(load_job_descriptions().keys())
    return render_template('index.html', job_titles=job_titles)


@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['resume']
        job_title = request.form.get('job_title')

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF or DOCX'}), 400

        if not job_title:
            return jsonify({'error': 'Please select a job title'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        resume_data = parse_resume(filepath)

        if 'error' in resume_data:
            os.remove(filepath)
            return jsonify({'error': resume_data['error']}), 400

        analysis_result = analyze_resume_for_job(resume_data, job_title)

        if 'error' in analysis_result:
            os.remove(filepath)
            return jsonify({'error': analysis_result['error']}), 400

        os.remove(filepath)

        analysis_result['email'] = resume_data.get('email')
        analysis_result['phone'] = resume_data.get('phone')

        return jsonify(analysis_result), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/api/jobs')
def get_jobs():
    job_descriptions = load_job_descriptions()
    return jsonify({'jobs': list(job_descriptions.keys())})


@app.route('/api/job/<job_title>')
def get_job_details(job_title):
    job_descriptions = load_job_descriptions()

    if job_title not in job_descriptions:
        return jsonify({'error': 'Job not found'}), 404

    return jsonify(job_descriptions[job_title])


@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


@app.errorhandler(404)
def not_found(e):
    return render_template('index.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting Resume Analyzer...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
