document.addEventListener('DOMContentLoaded', function() {
    const courseId = window.location.pathname.split('/').pop();
    loadAnalytics(courseId);
});

function loadAnalytics(courseId) {
    fetch(`/api/analytics/course/${courseId}`)
        .then(response => response.json())
        .then(data => {
            updateCourseStats(data.course_analytics);
            updateEngagementTable(data.student_engagement);
        })
        .catch(error => console.error('Error loading analytics:', error));
}

function updateCourseStats(analytics) {
    document.getElementById('total-students').textContent = analytics.total_students;
    document.getElementById('active-students').textContent = analytics.active_students;
    document.getElementById('average-grade').textContent = 
        (analytics.average_grade * 100).toFixed(1) + '%';
    document.getElementById('completion-rate').textContent = 
        (analytics.content_completion_rate * 100).toFixed(1) + '%';
}

function updateEngagementTable(engagement) {
    const tbody = document.querySelector('#engagement-table tbody');
    tbody.innerHTML = '';
    
    engagement.forEach(student => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${student.student_name}</td>
            <td>${formatTime(student.total_time)}</td>
            <td>${formatDate(student.last_active)}</td>
            <td>
                <span class="badge bg-${getEngagementColor(student.engagement_level)}">
                    ${student.engagement_level}
                </span>
            </td>
            <td>${(student.performance * 100).toFixed(1)}%</td>
            <td>
                <button class="btn btn-sm btn-primary" 
                        onclick="showStudentDetails(${student.student_id})">
                    View Details
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function showStudentDetails(studentId) {
    const courseId = window.location.pathname.split('/').pop();
    
    fetch(`/api/analytics/student/${studentId}/course/${courseId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('modal-time-spent').textContent = 
                formatTime(data.total_time_spent);
            document.getElementById('modal-views').textContent = 
                data.material_views;
            document.getElementById('modal-assignments').textContent = 
                data.assignments_completed;
            document.getElementById('modal-grade').textContent = 
                (data.average_grade * 100).toFixed(1) + '%';
            
            new bootstrap.Modal(document.getElementById('studentDetailsModal')).show();
        })
        .catch(error => console.error('Error loading student details:', error));
}

function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    if (hours > 0) {
        return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function getEngagementColor(level) {
    switch(level) {
        case 'High': return 'success';
        case 'Medium': return 'warning';
        case 'Low': return 'danger';
        default: return 'secondary';
    }
}
