document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('resume');
    const fileNameSpan = document.getElementById('fileName');
    const errorMessage = document.getElementById('errorMessage');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');

    // Handle file selection
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            fileNameSpan.textContent = file.name;
            fileNameSpan.style.display = 'block';
            hideError();
        } else {
            fileNameSpan.textContent = '';
            fileNameSpan.style.display = 'none';
        }
    });

    // Handle form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        hideError();
        
        const file = fileInput.files[0];
        const jobTitle = document.getElementById('job_title').value;

        // Validate inputs
        if (!file) {
            showError('Please select a resume file');
            return;
        }

        if (!jobTitle) {
            showError('Please select a job title');
            return;
        }

        // Check file size (16MB max)
        if (file.size > 16 * 1024 * 1024) {
            showError('File size must be less than 16MB');
            return;
        }

        // Check file type
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!validTypes.includes(file.type) && !file.name.match(/\.(pdf|docx)$/i)) {
            showError('Please upload a PDF or DOCX file');
            return;
        }

        // Prepare form data
        const formData = new FormData();
        formData.append('resume', file);
        formData.append('job_title', jobTitle);

        // Show loading state
        setLoadingState(true);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                // Store results in sessionStorage
                sessionStorage.setItem('analysisResults', JSON.stringify(data));
                
                // Redirect to results page
                window.location.href = '/results';
            } else {
                showError(data.error || 'An error occurred during analysis');
                setLoadingState(false);
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Failed to connect to server. Please try again.');
            setLoadingState(false);
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideError() {
        errorMessage.style.display = 'none';
        errorMessage.textContent = '';
    }

    function setLoadingState(loading) {
        if (loading) {
            analyzeBtn.disabled = true;
            btnText.style.display = 'none';
            btnLoader.style.display = 'inline-flex';
        } else {
            analyzeBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
        }
    }

    // Add drag and drop functionality
    const fileLabel = document.querySelector('.file-label');

    fileLabel.addEventListener('dragover', function(e) {
        e.preventDefault();
        fileLabel.style.borderColor = '#764ba2';
        fileLabel.style.background = '#f0f0f0';
    });

    fileLabel.addEventListener('dragleave', function(e) {
        e.preventDefault();
        fileLabel.style.borderColor = '#667eea';
        fileLabel.style.background = 'white';
    });

    fileLabel.addEventListener('drop', function(e) {
        e.preventDefault();
        fileLabel.style.borderColor = '#667eea';
        fileLabel.style.background = 'white';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    });
});