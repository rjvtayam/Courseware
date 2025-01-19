// Resources Page Interactions and Animations
document.addEventListener('DOMContentLoaded', function() {
    // Initialize loading animation
    const loadingAnimation = document.createElement('div');
    loadingAnimation.className = 'loading-animation';
    loadingAnimation.innerHTML = '<div class="loading-bar"></div>';
    document.body.appendChild(loadingAnimation);

    // Remove loading animation after page load
    window.addEventListener('load', function() {
        setTimeout(() => {
            loadingAnimation.style.opacity = '0';
            setTimeout(() => {
                loadingAnimation.remove();
            }, 400);
        }, 500);
    });

    // Animate resource cards on scroll
    const cards = document.querySelectorAll('.resource-card');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const cardObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach(card => {
        cardObserver.observe(card);
    });

    // Smooth hover effect for cards
    cards.forEach(card => {
        card.addEventListener('mousemove', handleCardHover);
        card.addEventListener('mouseleave', resetCard);
    });

    function handleCardHover(e) {
        const card = this;
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 20;
        const rotateY = -(x - centerX) / 20;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
    }

    function resetCard() {
        this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
    }

    // Add click animation for buttons
    const buttons = document.querySelectorAll('.btn-visit');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const circle = document.createElement('div');
            const diameter = Math.max(button.clientWidth, button.clientHeight);
            const radius = diameter / 2;

            circle.style.width = circle.style.height = `${diameter}px`;
            circle.style.left = `${e.clientX - button.offsetLeft - radius}px`;
            circle.style.top = `${e.clientY - button.offsetTop - radius}px`;
            circle.classList.add('ripple');

            const ripple = button.getElementsByClassName('ripple')[0];
            if (ripple) {
                ripple.remove();
            }

            button.appendChild(circle);
        });
    });

    // Add hover effect for tags
    const tags = document.querySelectorAll('.resource-tag');
    tags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(2deg)';
        });
        tag.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    });

    // Add parallax effect to header
    const header = document.querySelector('.resource-header');
    if (header) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            header.style.backgroundPositionY = scrolled * 0.5 + 'px';
        });
    }

    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Add search functionality
    const searchInput = document.querySelector('.resource-search');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.resource-card');

            cards.forEach(card => {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const description = card.querySelector('.card-text').textContent.toLowerCase();
                const tags = Array.from(card.querySelectorAll('.resource-tag'))
                    .map(tag => tag.textContent.toLowerCase());

                const matches = title.includes(searchTerm) || 
                              description.includes(searchTerm) || 
                              tags.some(tag => tag.includes(searchTerm));

                card.style.display = matches ? 'block' : 'none';
                if (matches) {
                    card.classList.add('animate');
                }
            });
        });
    }

    // Resource Management
    function saveResource(name, type = 'resource') {
        // Get storage key based on type
        const storageKey = `saved${type.charAt(0).toUpperCase() + type.slice(1)}s`;
        
        // Get saved items
        let savedItems = JSON.parse(localStorage.getItem(storageKey) || '[]');
        
        if (!savedItems.includes(name)) {
            // Add to saved items
            savedItems.push(name);
            localStorage.setItem(storageKey, JSON.stringify(savedItems));
            showToast(`${name} saved to bookmarks!`);
            
            // Update UI
            const bookmarkBtn = document.querySelector(`[data-resource="${name}"]`);
            if (bookmarkBtn) {
                bookmarkBtn.classList.add('active');
            }
        } else {
            // Remove from saved items
            savedItems = savedItems.filter(item => item !== name);
            localStorage.setItem(storageKey, JSON.stringify(savedItems));
            showToast(`${name} removed from bookmarks!`);
            
            // Update UI
            const bookmarkBtn = document.querySelector(`[data-resource="${name}"]`);
            if (bookmarkBtn) {
                bookmarkBtn.classList.remove('active');
            }
        }
    }

    // Toast Notifications
    function showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast-message';
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Initialize Resource Cards
    function initializeResourceCards() {
        // Add click handlers for bookmark buttons
        document.querySelectorAll('.btn-save').forEach(btn => {
            const name = btn.dataset.resource;
            const type = btn.dataset.type;
            
            // Check if already saved
            const storageKey = `saved${type.charAt(0).toUpperCase() + type.slice(1)}s`;
            const savedItems = JSON.parse(localStorage.getItem(storageKey) || '[]');
            if (savedItems.includes(name)) {
                btn.classList.add('active');
            }
            
            // Add click handler
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                saveResource(name, type);
            });
        });

        // Add hover effect for resource cards
        document.querySelectorAll('.resource-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px)';
                card.style.boxShadow = '0 15px 30px rgba(0,0,0,0.12)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = 'none';
            });
        });
    }

    // Initialize when DOM is loaded
    initializeResourceCards();
});
