// Feedback Form Functionality
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('feedback-form');
    const studentSelect = document.getElementById('student-select');
    const gradeInput = document.getElementById('grade');
    const feedbackTextarea = document.getElementById('feedback');
    const submitButton = document.querySelector('button[type="submit"]');

    // Initialize character counter
    updateFeedbackLength();
    feedbackTextarea.addEventListener('input', updateFeedbackLength);

    // Form validation
    form.addEventListener('submit', submitFeedback);
    gradeInput.addEventListener('input', () => validateGrade(gradeInput.value));
    feedbackTextarea.addEventListener('input', () => validateFeedback(feedbackTextarea.value));

    // Student selection
    studentSelect.addEventListener('change', function() {
        if (this.value) {
            loadStudentFeedback(this.value);
        } else {
            resetForm();
        }
    });
});

function updateFeedbackLength() {
    const feedback = document.getElementById('feedback');
    const counter = document.getElementById('char-counter');
    const maxLength = 1000;
    const currentLength = feedback.value.length;
    
    counter.textContent = `${currentLength}/${maxLength} characters`;
    counter.style.color = currentLength > maxLength ? '#dc2626' : '#6b7280';
}

function validateGrade(grade) {
    const gradeNum = parseFloat(grade);
    const errorElement = document.getElementById('grade-error');
    
    if (isNaN(gradeNum) || gradeNum < 0 || gradeNum > 100) {
        showError('grade-error', 'Grade must be between 0 and 100');
        return false;
    }
    
    hideError('grade-error');
    return true;
}

function validateFeedback(feedback) {
    const errorElement = document.getElementById('feedback-error');
    
    if (!feedback.trim()) {
        showError('feedback-error', 'Feedback cannot be empty');
        return false;
    }
    
    if (feedback.length > 1000) {
        showError('feedback-error', 'Feedback cannot exceed 1000 characters');
        return false;
    }
    
    hideError('feedback-error');
    return true;
}

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.classList.remove('hidden');
}

function hideError(elementId) {
    const errorElement = document.getElementById(elementId);
    errorElement.classList.add('hidden');
}

async function loadStudentFeedback(studentId) {
    if (!studentId) return;
    
    const form = document.getElementById('feedback-form');
    form.classList.add('loading');
    
    try {
        const response = await fetch(`/api/feedback/${studentId}`);
        if (!response.ok) throw new Error('Failed to load feedback');
        
        const data = await response.json();
        
        // Populate form with existing feedback
        document.getElementById('student-id').value = studentId;
        document.getElementById('grade').value = data.grade || '';
        document.getElementById('feedback').value = data.feedback || '';
        
        // Update character counter
        updateFeedbackLength();
        
    } catch (error) {
        console.error('Error loading feedback:', error);
        showError('form-error', 'Failed to load student feedback');
    } finally {
        form.classList.remove('loading');
    }
}

async function submitFeedback(event) {
    event.preventDefault();
    
    const form = event.target;
    const studentId = document.getElementById('student-id').value;
    const grade = document.getElementById('grade').value;
    const feedback = document.getElementById('feedback').value;
    
    // Validate form
    if (!validateGrade(grade) || !validateFeedback(feedback)) {
        return;
    }
    
    // Disable form during submission
    form.classList.add('loading');
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    
    try {
        const response = await fetch('/api/feedback/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            },
            body: JSON.stringify({
                student_id: studentId,
                grade: parseFloat(grade),
                feedback: feedback
            })
        });
        
        if (!response.ok) throw new Error('Failed to submit feedback');
        
        // Show success message
        const successMessage = document.createElement('div');
        successMessage.className = 'success-message';
        successMessage.innerHTML = '<i class="fas fa-check-circle"></i> Feedback submitted successfully!';
        
        form.insertBefore(successMessage, form.firstChild);
        
        // Remove success message after 3 seconds
        setTimeout(() => {
            successMessage.remove();
        }, 3000);
        
    } catch (error) {
        console.error('Error submitting feedback:', error);
        showError('form-error', 'Failed to submit feedback. Please try again.');
    } finally {
        form.classList.remove('loading');
        submitButton.disabled = false;
    }
}

function resetForm() {
    const form = document.getElementById('feedback-form');
    form.reset();
    document.getElementById('student-id').value = '';
    updateFeedbackLength();
    
    // Hide all error messages
    document.querySelectorAll('.error-message').forEach(el => {
        el.classList.add('hidden');
    });
}
