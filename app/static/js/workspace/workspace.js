// Workspace Dashboard Functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeSearch();
    initializeFilters();
    initializeInteractions();
    initializeStats();
});

// Initialize Animations
function initializeAnimations() {
    // Animate header elements on load
    const header = document.querySelector('.workspace-header');
    if (header) {
        header.style.opacity = '0';
        header.style.transform = 'translateY(-20px)';
        
        requestAnimationFrame(() => {
            header.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            header.style.opacity = '1';
            header.style.transform = 'translateY(0)';
        });
    }

    // Animate course cards on scroll
    const courseCards = document.querySelectorAll('.course-card');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                cardObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    courseCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.5s ease ${index * 0.1}s, transform 0.5s ease ${index * 0.1}s`;
        cardObserver.observe(card);
    });
}

// Initialize Search Functionality
function initializeSearch() {
    const searchInput = document.getElementById('courseSearch');
    const categoryFilter = document.getElementById('categoryFilter');
    const courseItems = document.querySelectorAll('.course-item');
    let searchTimeout;

    function filterCourses() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedCategory = categoryFilter.value.toLowerCase();
        let visibleCount = 0;

        courseItems.forEach(item => {
            const title = item.querySelector('.card-title').textContent.toLowerCase();
            const description = item.querySelector('.card-text').textContent.toLowerCase();
            const category = item.querySelector('.category-badge').textContent.toLowerCase();

            const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
            const matchesCategory = !selectedCategory || category.includes(selectedCategory);
            const shouldShow = matchesSearch && matchesCategory;

            if (shouldShow) {
                item.style.display = 'block';
                item.style.opacity = '1';
                item.style.transform = 'scale(1)';
                visibleCount++;
            } else {
                item.style.opacity = '0';
                item.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    if (item.style.opacity === '0') {
                        item.style.display = 'none';
                    }
                }, 300);
            }
        });

        // Show empty state if no results
        const emptyState = document.querySelector('.empty-state');
        if (emptyState) {
            if (visibleCount === 0) {
                emptyState.style.display = 'block';
                emptyState.style.opacity = '1';
            } else {
                emptyState.style.opacity = '0';
                setTimeout(() => {
                    emptyState.style.display = 'none';
                }, 300);
            }
        }
    }

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(filterCourses, 300);
        });
    }

    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterCourses);
    }
}

// Initialize Filter Functionality
function initializeFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            // Remove ripple after animation
            setTimeout(() => ripple.remove(), 1000);
        });
    });
}

// Initialize Interactive Elements
function initializeInteractions() {
    // Course card hover effects
    const courseCards = document.querySelectorAll('.course-card');
    
    courseCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
        });
        
        // Add click ripple effect
        card.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            ripple.classList.add('card-ripple');
            ripple.style.left = `${e.clientX - rect.left}px`;
            ripple.style.top = `${e.clientY - rect.top}px`;
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 1000);
        });
    });

    // Button hover effects
    const buttons = document.querySelectorAll('.btn-action');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Initialize Statistics
function initializeStats() {
    // Animate statistics on scroll
    const stats = document.querySelectorAll('.course-stats span');
    
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };

    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const countElement = entry.target;
                const targetCount = parseInt(countElement.dataset.count || '0');
                animateCount(countElement, targetCount);
                statsObserver.unobserve(countElement);
            }
        });
    }, observerOptions);

    stats.forEach(stat => {
        statsObserver.observe(stat);
    });
}

function animateCount(element, target) {
    let current = 0;
    const duration = 1000; // ms
    const step = target / (duration / 16); // 60fps
    
    function updateCount() {
        current = Math.min(current + step, target);
        element.textContent = Math.round(current);
        
        if (current < target) {
            requestAnimationFrame(updateCount);
        }
    }
    
    requestAnimationFrame(updateCount);
}
