// Initialize Socket.IO connection
const socket = io();

// Room state
let courseId = null;
let onlineUsers = new Set();

function initRoom(id) {
    courseId = id;
    
    // Join course room
    socket.emit('join_course_room', { course_id: courseId });
    
    // Setup event listeners
    setupSocketListeners();
    setupUIListeners();
}

function setupSocketListeners() {
    // Handle user joined
    socket.on('user_joined', (data) => {
        onlineUsers.add(data.user_id);
        updateOnlineCount();
        appendSystemMessage(`${data.username} joined the room`);
    });
    
    // Handle user left
    socket.on('user_left', (data) => {
        onlineUsers.delete(data.user_id);
        updateOnlineCount();
        appendSystemMessage(`${data.username} left the room`);
    });
    
    // Handle room messages
    socket.on('room_message', (data) => {
        appendMessage(data);
    });
    
    // Handle material uploads
    socket.on('material_uploaded', (data) => {
        appendMaterial(data);
        appendSystemMessage(`New material uploaded: ${data.title}`);
    });
}

function setupUIListeners() {
    // Message form submission
    const messageForm = document.getElementById('messageForm');
    if (messageForm) {
        messageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message) {
                socket.emit('course_message', {
                    course_id: courseId,
                    message: message
                });
                input.value = '';
            }
        });
    }
    
    // File upload
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadModal = document.getElementById('uploadModal');
    const uploadForm = document.getElementById('uploadForm');
    const cancelUpload = document.getElementById('cancelUpload');
    
    if (uploadBtn && uploadModal) {
        uploadBtn.addEventListener('click', () => {
            uploadModal.classList.add('show');
        });
        
        cancelUpload.addEventListener('click', () => {
            uploadModal.classList.remove('show');
            uploadForm.reset();
        });
        
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(uploadForm);
            try {
                const response = await fetch(`/course/${courseId}/materials/upload`, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                if (data.success) {
                    uploadModal.classList.remove('show');
                    uploadForm.reset();
                } else {
                    alert(data.error || 'Upload failed');
                }
            } catch (error) {
                console.error('Upload error:', error);
                alert('Upload failed');
            }
        });
    }
}

function updateOnlineCount() {
    const counter = document.getElementById('onlineCount');
    if (counter) {
        counter.textContent = `${onlineUsers.size} online`;
    }
}

function appendMessage(data) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <span>${data.username[0].toUpperCase()}</span>
        </div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-author">${data.username}</span>
                <span class="message-time">${formatTime(data.timestamp)}</span>
            </div>
            <p class="message-text">${data.message}</p>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom(chatMessages);
}

function appendSystemMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'system-message';
    
    messageDiv.innerHTML = `
        <div class="system-message-content">
            ${message}
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom(chatMessages);
}

function appendMaterial(data) {
    const materialsList = document.getElementById('materialsList');
    const materialDiv = document.createElement('div');
    materialDiv.className = 'material-item';
    
    materialDiv.innerHTML = `
        <div class="material-content">
            <div class="material-icon">
                <i class="fas fa-file"></i>
            </div>
            <div class="material-details">
                <p class="material-title">${data.title}</p>
            </div>
        </div>
    `;
    
    materialsList.appendChild(materialDiv);
}

function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
}

// Clean up when leaving the page
window.addEventListener('beforeunload', () => {
    if (courseId) {
        socket.emit('leave_course_room', { course_id: courseId });
    }
});
