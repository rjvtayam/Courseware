class CourseView {
    constructor(courseId) {
        this.courseId = courseId;
        this.initializeSortable();
        this.setupEventListeners();
    }

    initializeSortable() {
        const videosContent = document.getElementById('videos-content');
        const materialsContent = document.getElementById('materials-content');

        if (videosContent) {
            new Sortable(videosContent, {
                animation: 150,
                onEnd: () => this.updateContentOrder('videos-content')
            });
        }

        if (materialsContent) {
            new Sortable(materialsContent, {
                animation: 150,
                onEnd: () => this.updateContentOrder('materials-content')
            });
        }
    }

    setupEventListeners() {
        // Close modal when clicking outside
        document.addEventListener('click', (e) => {
            const modal = document.getElementById('editModal');
            if (e.target === modal) {
                this.hideEditModal();
            }
        });
    }

    async markContentViewed(contentId) {
        try {
            await fetch(`/course/${this.courseId}/content/${contentId}/progress`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'action=view'
            });
        } catch (error) {
            console.error('Error marking content as viewed:', error);
        }
    }

    async markContentCompleted(contentId) {
        try {
            const response = await fetch(`/course/${this.courseId}/content/${contentId}/progress`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'action=complete'
            });

            const data = await response.json();
            if (data.progress) {
                this.updateProgressUI(data.progress, contentId);
            }
        } catch (error) {
            console.error('Error marking content as completed:', error);
        }
    }

    updateProgressUI(progress, contentId) {
        // Update progress bar
        const progressBar = document.querySelector('.progress-bar');
        const progressText = document.querySelector('.progress-text');
        if (progressBar && progressText) {
            progressBar.style.width = `${progress}%`;
            progressText.textContent = `${progress.toFixed(1)}%`;
        }

        // Update completion badge
        const contentElement = document.querySelector(`[data-content-id="${contentId}"]`);
        if (contentElement && !contentElement.querySelector('.completion-badge')) {
            const badge = document.createElement('span');
            badge.className = 'completion-badge';
            badge.textContent = 'Completed';
            contentElement.querySelector('.content-header').appendChild(badge);
        }
    }

    showEditModal(contentId) {
        const content = document.querySelector(`[data-content-id="${contentId}"]`);
        const title = content.querySelector('h4').textContent;
        const description = content.querySelector('p').textContent;

        document.getElementById('edit_title').value = title;
        document.getElementById('edit_description').value = description;
        document.getElementById('editForm').action = `/course/${this.courseId}/content/${contentId}/edit`;

        document.getElementById('editModal').classList.remove('hidden');
    }

    hideEditModal() {
        document.getElementById('editModal').classList.add('hidden');
    }

    async updateContentOrder(containerId) {
        const container = document.getElementById(containerId);
        const items = container.querySelectorAll('[data-content-id]');
        const order = Array.from(items).map(item => item.dataset.contentId);

        try {
            await fetch(`/course/${this.courseId}/content/reorder`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ order })
            });
        } catch (error) {
            console.error('Error updating content order:', error);
        }
    }
}

// Initialize progress bars
document.addEventListener('DOMContentLoaded', function() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const progress = bar.getAttribute('data-progress');
        bar.style.setProperty('--progress', progress);
    });
});

// Initialize CourseView when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const courseIdMeta = document.querySelector('meta[name="course-id"]');
    if (courseIdMeta) {
        const courseId = courseIdMeta.getAttribute('content');
        window.courseView = new CourseView(courseId);
    }
});
