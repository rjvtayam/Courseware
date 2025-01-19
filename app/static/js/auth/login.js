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
});
