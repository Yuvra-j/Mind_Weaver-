// MindWeaver Saga - Enhanced Frontend JavaScript
// Handles API communication and user interactions with beautiful animations

class MindWeaverSaga {
    constructor() {
        this.userInput = document.getElementById('user-input');
        this.submitBtn = document.getElementById('submit-btn');
        this.storyOutput = document.getElementById('story-output');
        this.newChatBtn = document.getElementById('new-chat-btn');
        this.googleSigninBtn = document.getElementById('google-signin-btn');
        this.signinSection = document.getElementById('signin-section');
        this.userProfile = document.getElementById('user-profile');
        this.userName = document.getElementById('user-name');
        this.userEmail = document.getElementById('user-email');
        this.userAvatar = document.getElementById('user-avatar');
        this.signoutBtn = document.getElementById('signout-btn');
        this.API_URL = 'http://127.0.0.1:5000/generate-story';
        this.currentUser = null;
        this.currentChatId = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.adjustTextareaHeight();
        this.addWelcomeMessage();
    }

    setupEventListeners() {
        this.submitBtn.addEventListener('click', () => this.generateStory());
        this.newChatBtn.addEventListener('click', () => this.startNewChat());
        this.googleSigninBtn.addEventListener('click', () => this.signInWithGoogle());
        this.signoutBtn.addEventListener('click', () => this.signOut());
        
        this.userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.ctrlKey) {
                e.preventDefault();
                this.generateStory();
            }
        });

        this.userInput.addEventListener('input', () => {
            this.adjustTextareaHeight();
        });

        // Add interactive feedback
        this.userInput.addEventListener('focus', () => {
            this.userInput.classList.add('ring-2', 'ring-yellow-400', 'ring-opacity-50');
        });

        this.userInput.addEventListener('blur', () => {
            this.userInput.classList.remove('ring-2', 'ring-yellow-400', 'ring-opacity-50');
        });

        // Initialize Google Sign-In
        this.initializeGoogleSignIn();
    }

    adjustTextareaHeight() {
        this.userInput.style.height = 'auto';
        this.userInput.style.height = Math.min(this.userInput.scrollHeight, 120) + 'px';
    }

    addWelcomeMessage() {
        // Add a subtle entrance animation to the welcome message
        setTimeout(() => {
            const welcomeDiv = this.storyOutput.querySelector('div');
            if (welcomeDiv) {
                welcomeDiv.classList.add('message-slide-in');
            }
        }, 500);
    }

    // Loading state management with enhanced UI
    setLoading(isLoading) {
        this.submitBtn.disabled = isLoading;
        if (isLoading) {
            this.submitBtn.innerHTML = `
                <div class="flex items-center gap-2">
                    <div class="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
                    <span>Weaving your saga...</span>
                </div>
            `;
            this.submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
        } else {
            this.submitBtn.innerHTML = 'Ask';
            this.submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
        }
    }

    // Enhanced story display with beautiful animations
    displayStory(story) {
        const storyDiv = document.createElement('div');
        storyDiv.className = 'message-slide-in';
        
        storyDiv.innerHTML = `
            <div class="flex items-start gap-4 mb-6">
                <div class="w-10 h-10 bg-gradient-to-r from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <span class="text-black font-bold text-sm">MW</span>
                </div>
                <div class="flex-1">
                    <div class="bg-gradient-to-r from-yellow-50 to-yellow-100 rounded-2xl p-6 shadow-lg">
                        <div class="story-text text-gray-800 leading-relaxed">
                            ${story.split('\n').map(paragraph => 
                                paragraph.trim() ? `<p class="mb-4 last:mb-0">${paragraph}</p>` : ''
                            ).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Only clear the welcome message if it exists, otherwise append to existing content
        const welcomeDiv = this.storyOutput.querySelector('.text-center.text-gray-600.italic');
        if (welcomeDiv) {
            this.storyOutput.innerHTML = '';
        }
        this.storyOutput.appendChild(storyDiv);
        this.scrollToBottom();
    }

    // Enhanced error display
    displayError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message-slide-in';
        
        errorDiv.innerHTML = `
            <div class="flex items-start gap-4 mb-6">
                <div class="w-10 h-10 bg-gradient-to-r from-red-400 to-red-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                </div>
                <div class="flex-1">
                    <div class="bg-red-50 border border-red-200 rounded-2xl p-6 shadow-lg">
                        <h3 class="font-semibold text-red-800 mb-2">Oops! Something went wrong</h3>
                        <p class="text-sm text-red-700 mb-2">${message}</p>
                        <p class="text-xs text-red-600">Please try again or check if the backend is running.</p>
                    </div>
                </div>
            </div>
        `;
        
        // Only clear the welcome message if it exists, otherwise append to existing content
        const welcomeDiv = this.storyOutput.querySelector('.text-center.text-gray-600.italic');
        if (welcomeDiv) {
            this.storyOutput.innerHTML = '';
        }
        this.storyOutput.appendChild(errorDiv);
        this.scrollToBottom();
    }

    // Enhanced loading animation
    showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message-slide-in';
        
        loadingDiv.innerHTML = `
            <div class="flex items-start gap-4 mb-6">
                <div class="w-10 h-10 bg-gradient-to-r from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <span class="text-black font-bold text-sm">MW</span>
                </div>
                <div class="flex-1">
                    <div class="bg-gradient-to-r from-yellow-50 to-yellow-100 rounded-2xl p-6 shadow-lg">
                        <div class="typing-indicator">
                            <span>Weaving your saga</span>
                            <div class="flex gap-1">
                                <div class="typing-dot"></div>
                                <div class="typing-dot"></div>
                                <div class="typing-dot"></div>
                            </div>
                        </div>
                        <p class="text-sm text-gray-600 mt-2">Creating your personalized therapeutic fantasy...</p>
                    </div>
                </div>
            </div>
        `;
        
        // Only clear the welcome message if it exists, otherwise append to existing content
        const welcomeDiv = this.storyOutput.querySelector('.text-center.text-gray-600.italic');
        if (welcomeDiv) {
            this.storyOutput.innerHTML = '';
        }
        this.storyOutput.appendChild(loadingDiv);
        this.scrollToBottom();
    }

    scrollToBottom() {
        // Use setTimeout to ensure DOM updates are complete
        setTimeout(() => {
            this.storyOutput.scrollTop = this.storyOutput.scrollHeight;
        }, 100);
    }

    // Send request to backend with enhanced error handling
    async generateStory() {
        const input = this.userInput.value.trim();
        
        if (!input) {
            this.showNotification('Please enter your emotions or story choice!', 'warning');
            return;
        }

        // Add user message to chat
        this.addUserMessage(input);

        this.setLoading(true);
        this.showLoading();

        try {
            const response = await fetch(this.API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_input: input })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.error) {
                this.displayError(data.error);
            } else if (data.story) {
                this.displayStory(data.story);
                this.clearInput();
            } else {
                this.displayError('No story received from the server');
            }

        } catch (error) {
            console.error('Error generating story:', error);
            this.displayError('Failed to connect to the server. Please make sure the backend is running on http://127.0.0.1:5000');
        } finally {
            this.setLoading(false);
        }
    }

    // Clear input after successful submission
    clearInput() {
        this.userInput.value = '';
        this.adjustTextareaHeight();
    }

    // Show notification (optional enhancement)
    showNotification(message, type = 'info') {
        // Simple alert for now, could be enhanced with a toast notification
        alert(message);
    }

    // Add user message to chat
    addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message-slide-in';
        
        messageDiv.innerHTML = `
            <div class="flex items-start gap-4 mb-6 justify-end">
                <div class="flex-1 max-w-xs">
                    <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-2xl p-4 shadow-lg">
                        <p class="text-sm">${this.escapeHtml(message)}</p>
                    </div>
                </div>
                <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <span class="text-white font-bold text-xs">You</span>
                </div>
            </div>
        `;
        
        this.storyOutput.appendChild(messageDiv);
        this.scrollToBottom();
    }

    // Escape HTML to prevent XSS
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Google Sign-In Methods
    initializeGoogleSignIn() {
        // Check if user is already signed in
        this.checkAuthStatus();
    }

    async checkAuthStatus() {
        try {
            const response = await fetch('http://127.0.0.1:5000/auth/status', {
                method: 'GET',
                credentials: 'include'
            });
            
            if (response.ok) {
                const user = await response.json();
                this.setUserProfile(user);
            } else {
                this.showSignInButton();
            }
        } catch (error) {
            console.log('Not authenticated');
            this.showSignInButton();
        }
    }

    signInWithGoogle() {
        // This will be handled by the backend redirect
        window.location.href = 'http://127.0.0.1:5000/auth/google';
    }

    setUserProfile(user) {
        this.currentUser = user;
        this.userName.textContent = user.name;
        this.userEmail.textContent = user.email;
        this.userAvatar.src = user.picture;
        this.userAvatar.alt = user.name;
        
        this.signinSection.classList.add('hidden');
        this.userProfile.classList.remove('hidden');
    }

    showSignInButton() {
        this.signinSection.classList.remove('hidden');
        this.userProfile.classList.add('hidden');
        this.currentUser = null;
    }

    async signOut() {
        try {
            await fetch('http://127.0.0.1:5000/auth/logout', {
                method: 'POST',
                credentials: 'include'
            });
        } catch (error) {
            console.error('Error signing out:', error);
        }
        
        this.showSignInButton();
        this.startNewChat();
    }

    // New Chat Methods
    startNewChat() {
        this.currentChatId = null;
        this.storyOutput.innerHTML = '';
        this.addWelcomeMessage();
        this.userInput.value = '';
        this.adjustTextareaHeight();
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.mindWeaverSaga = new MindWeaverSaga();
    console.log('🌟 MindWeaver Saga initialized! Ready to create therapeutic fantasies.');
});
