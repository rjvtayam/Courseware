// Initialize Socket.IO connection with configuration
const socket = io({
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    timeout: 20000,
});

// Handle connection events
socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
});

socket.on('disconnect', (reason) => {
    console.log('Disconnected:', reason);
});

// Notification sound
const notificationSound = new Audio('/static/sounds/notification.mp3');

// Notification types and their icons
const NOTIFICATION_ICONS = {
    'assignment': 'fas fa-tasks',
    'feedback': 'fas fa-comment',
    'grade': 'fas fa-star',
    'course': 'fas fa-book',
    'material': 'fas fa-file-alt',
    'default': 'fas fa-bell'
};

// Handle incoming notifications
socket.on('notification', (data) => {
    // Play notification sound
    notificationSound.play().catch(e => console.log('Error playing sound:', e));
    
    // Update notification counter
    updateNotificationCounter(1);
    
    // Show notification toast
    showNotificationToast(data);
    
    // Add notification to list if notification panel is open
    if (document.querySelector('#notificationPanel').classList.contains('show')) {
        prependNotificationToList(data);
    }
});

// Show notification toast
function showNotificationToast(notification) {
    const icon = NOTIFICATION_ICONS[notification.type] || NOTIFICATION_ICONS.default;
    const toast = `
        <div class="toast notification-toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <i class="${icon} me-2"></i>
                <strong class="me-auto">New Notification</strong>
                <small>${moment(notification.created_at).fromNow()}</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${notification.message}
            </div>
        </div>
    `;
    
    const toastContainer = document.getElementById('toastContainer');
    toastContainer.insertAdjacentHTML('beforeend', toast);
    
    const toastElement = toastContainer.lastElementChild;
    const bsToast = new bootstrap.Toast(toastElement);
    bsToast.show();
    
    // Remove toast after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Update notification counter
function updateNotificationCounter(increment = 0) {
    const counter = document.getElementById('notificationCounter');
    if (counter) {
        let count = parseInt(counter.textContent) || 0;
        count += increment;
        counter.textContent = count;
        counter.style.display = count > 0 ? 'block' : 'none';
    }
}

// Load notifications
async function loadNotifications(offset = 0, limit = 20) {
    try {
        const response = await fetch(`/api/notifications?offset=${offset}&limit=${limit}`);
        const data = await response.json();
        
        if (data.notifications) {
            const notificationList = document.getElementById('notificationList');
            data.notifications.forEach(notification => {
                appendNotificationToList(notification);
            });
        }
    } catch (error) {
        console.error('Error loading notifications:', error);
    }
}

// Append notification to list
function appendNotificationToList(notification) {
    const icon = NOTIFICATION_ICONS[notification.type] || NOTIFICATION_ICONS.default;
    const notificationHtml = `
        <div class="notification-item ${notification.is_read ? 'read' : 'unread'}" 
             data-notification-id="${notification.id}">
            <div class="notification-icon">
                <i class="${icon}"></i>
            </div>
            <div class="notification-content">
                <div class="notification-message">${notification.message}</div>
                <div class="notification-time">
                    ${moment(notification.created_at).fromNow()}
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('notificationList').insertAdjacentHTML('beforeend', notificationHtml);
}

// Prepend new notification to list
function prependNotificationToList(notification) {
    const icon = NOTIFICATION_ICONS[notification.type] || NOTIFICATION_ICONS.default;
    const notificationHtml = `
        <div class="notification-item unread" data-notification-id="${notification.id}">
            <div class="notification-icon">
                <i class="${icon}"></i>
            </div>
            <div class="notification-content">
                <div class="notification-message">${notification.message}</div>
                <div class="notification-time">just now</div>
            </div>
        </div>
    `;
    
    const notificationList = document.getElementById('notificationList');
    notificationList.insertAdjacentHTML('afterbegin', notificationHtml);
}

// Mark notification as read
async function markNotificationAsRead(notificationId) {
    try {
        const response = await fetch(`/api/notifications/${notificationId}/read`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const notificationElement = document.querySelector(
                `.notification-item[data-notification-id="${notificationId}"]`
            );
            if (notificationElement) {
                notificationElement.classList.remove('unread');
                notificationElement.classList.add('read');
            }
            updateNotificationCounter(-1);
        }
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
}

// Initialize notification panel
document.addEventListener('DOMContentLoaded', () => {
    // Load initial notifications
    loadNotifications();
    
    // Handle notification click
    document.getElementById('notificationList').addEventListener('click', (event) => {
        const notificationItem = event.target.closest('.notification-item');
        if (notificationItem && !notificationItem.classList.contains('read')) {
            const notificationId = notificationItem.dataset.notificationId;
            markNotificationAsRead(notificationId);
        }
    });
});
