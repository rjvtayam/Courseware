// Login page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth hover effects for buttons
    const buttons = document.querySelectorAll('.oauth-btn');
    buttons.forEach(button => {
        button.addEventListener('mouseover', function() {
            this.style.transform = 'translateY(-2px)';
        });
        button.addEventListener('mouseout', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Get role selection elements
    const roleStudent = document.getElementById('roleStudent');
    const roleTeacher = document.getElementById('roleTeacher');
    const googleBtn = document.querySelector('.google-btn');
    const githubBtn = document.querySelector('.github-btn');

    // Function to update OAuth URLs with role parameter
    function updateOAuthUrls() {
        const role = document.querySelector('input[name="role"]:checked').value;
        
        // Update Google OAuth URL
        const googleUrl = new URL(googleBtn.href);
        googleUrl.searchParams.set('role', role);
        googleBtn.href = googleUrl.toString();
        
        // Update GitHub OAuth URL
        const githubUrl = new URL(githubBtn.href);
        githubUrl.searchParams.set('role', role);
        githubBtn.href = githubUrl.toString();
    }

    // Add event listeners for role changes
    roleStudent.addEventListener('change', updateOAuthUrls);
    roleTeacher.addEventListener('change', updateOAuthUrls);

    // Initialize URLs with default role (student)
    updateOAuthUrls();
});
