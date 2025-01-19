// Welcome Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Animate stats when they come into view
    const stats = document.querySelectorAll('.stat-number');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateStats(entry.target);
            }
        });
    }, { threshold: 0.5 });

    stats.forEach(stat => observer.observe(stat));

    // Animate features on scroll
    const features = document.querySelectorAll('.feature-card');
    features.forEach((feature, index) => {
        feature.style.opacity = '0';
        feature.style.transform = 'translateY(20px)';
        setTimeout(() => {
            feature.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            feature.style.opacity = '1';
            feature.style.transform = 'translateY(0)';
        }, 200 * index);
    });
});

function animateStats(element) {
    const finalValue = parseInt(element.textContent);
    let startValue = 0;
    const duration = 2000;
    const increment = finalValue / (duration / 16);
    
    function updateValue() {
        startValue += increment;
        if (startValue < finalValue) {
            element.textContent = Math.floor(startValue) + '+';
            requestAnimationFrame(updateValue);
        } else {
            element.textContent = finalValue + '+';
        }
    }
    
    updateValue();
}
