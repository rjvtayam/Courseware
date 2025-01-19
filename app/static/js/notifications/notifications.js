const initNotifications = () => {
    const notificationButton = document.getElementById('notification-button');
    const notificationPanel = document.getElementById('notification-panel');
    
    const fetchNotifications = async () => {
        const response = await fetch('/notifications');
        const notifications = await response.json();
        updateNotificationBadge(notifications.length);
        return notifications;
    };

    const markAsRead = async (id) => {
        await fetch(`/notifications/mark-read/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
    };

    // Update notification count every minute
    setInterval(fetchNotifications, 60000);
};