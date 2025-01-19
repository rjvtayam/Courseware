// Workspace Dashboard Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Course card hover effects
    const courseCards = document.querySelectorAll('.course-card');
    courseCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Search functionality
    const searchInput = document.querySelector('#courseSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const courses = document.querySelectorAll('.course-card');
            
            courses.forEach(course => {
                const title = course.querySelector('.card-title').textContent.toLowerCase();
                const description = course.querySelector('.card-text').textContent.toLowerCase();
                const category = course.querySelector('.category-badge')?.textContent.toLowerCase() || '';
                
                if (title.includes(searchTerm) || 
                    description.includes(searchTerm) || 
                    category.includes(searchTerm)) {
                    course.style.display = '';
                } else {
                    course.style.display = 'none';
                }
            });
        });
    }

    // Category filter
    const categoryFilters = document.querySelectorAll('.category-filter');
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            const courses = document.querySelectorAll('.course-card');
            
            // Update active state
            categoryFilters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
            
            courses.forEach(course => {
                const courseCategory = course.querySelector('.category-badge')?.textContent;
                if (category === 'all' || courseCategory === category) {
                    course.style.display = '';
                } else {
                    course.style.display = 'none';
                }
            });
        });
    });

    // Course view counter
    const courseLinks = document.querySelectorAll('.course-link');
    courseLinks.forEach(link => {
        link.addEventListener('click', function() {
            const courseId = this.dataset.courseId;
            // Send view count to server
            fetch(`/api/course/${courseId}/view`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            }).catch(console.error);
        });
    });
});
