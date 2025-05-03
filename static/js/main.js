document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const messageHistory = document.getElementById('messageHistory');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const themeToggle = document.getElementById('themeToggle');
    const typingIndicator = document.getElementById('typingIndicator');
    
    // Initialize theme
    const currentTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    // Theme toggle
    themeToggle.addEventListener('click', () => {
        const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update particles for theme
        if (window.pJSDom && window.pJSDom.length > 0) {
            window.pJSDom[0].pJS.fn.vendors.destroypJS();
            particlesJS('particles-js', {
                /* Same config as before but adjust colors */
                particles: {
                    color: { value: newTheme === 'dark' ? '#6c5ce7' : '#341f97' },
                    line_linked: { color: newTheme === 'dark' ? '#6c5ce7' : '#341f97' }
                }
            });
        }
    });
    
    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Send message function
    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message
        addMessage('user', message);
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Show typing indicator
        typingIndicator.style.display = 'flex';
        
        // Disable input during processing
        userInput.disabled = true;
        sendButton.disabled = true;
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            addMessage('adam', data.response);
        } catch (error) {
            addMessage('adam', "*dust falls* My knowledge fails me...");
        } finally {
            typingIndicator.style.display = 'none';
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }
    };
    
    // Add message to chat
    const addMessage = (sender, text) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        messageDiv.innerHTML = `
            <div class="avatar">
                <img src="/static/assets/${sender === 'user' ? 'user' : 'adam'}-avatar.png" alt="${sender}">
            </div>
            <div class="message-content">
                <div class="message-text">${text}</div>
            </div>
        `;
        
        messageHistory.appendChild(messageDiv);
        messageHistory.scrollTop = messageHistory.scrollHeight;
    };
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Initial focus
    userInput.focus();
});