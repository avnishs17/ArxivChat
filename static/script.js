// Enhanced ArxivChat JavaScript - Production Ready with Markdown Support

let selectedPaper = null;
let searchHistory = JSON.parse(localStorage.getItem('arxivChat_searchHistory')) || [];
let bookmarkedPapers = JSON.parse(localStorage.getItem('arxivChat_bookmarks')) || [];
let currentConversation = [];

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadSearchHistory();
    loadBookmarks();
    
    // Configure marked for better markdown rendering
    if (typeof marked !== 'undefined') {
        marked.setOptions({
            breaks: true,        // Enable line breaks
            gfm: true,          // GitHub flavored markdown
            sanitize: false,    // Allow HTML (we'll sanitize manually if needed)
            smartLists: true,   // Better list handling
            smartypants: true   // Smart quotes and dashes
        });
    }
    
    // Close panels when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.side-panel') && !e.target.closest('.header-actions')) {
            closePanels();
        }
    });
});

// Search functionality
async function searchPapers() {
    const query = document.getElementById('searchQuery').value.trim();
    const limit = parseInt(document.getElementById('limitSelect').value) || 10;
    
    if (!query) {
        showToast('Please enter a search query', 'warning');
        return;
    }

    const resultsDiv = document.getElementById('searchResults');
    const searchBtn = document.getElementById('searchBtn');
    
    // Update UI state
    resultsDiv.innerHTML = '<div class="loading">Searching papers...</div>';
    searchBtn.disabled = true;
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';

    try {
        const response = await fetch(`/api/papers?q=${encodeURIComponent(query)}&limit=${limit}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();

        if (data.papers && data.papers.length > 0) {
            displayPapers(data.papers);
            addToSearchHistory(query, data.papers.length);
            showToast(`Found ${data.papers.length} papers`, 'success');
        } else {
            resultsDiv.innerHTML = '<div class="error">No papers found. Try a different search term.</div>';
            showToast('No papers found', 'warning');
        }
    } catch (error) {
        console.error('Search error:', error);
        resultsDiv.innerHTML = '<div class="error">Error searching papers. Please try again.</div>';
        showToast('Search failed. Please try again.', 'error');
    } finally {
        // Reset button state
        searchBtn.disabled = false;
        searchBtn.innerHTML = '<i class="fas fa-search"></i> Search';
    }
}

function displayPapers(papers) {
    const resultsDiv = document.getElementById('searchResults');
    resultsDiv.innerHTML = papers.map((paper, index) => {
        const isBookmarked = bookmarkedPapers.some(b => b.id === paper.id);
        const publishedDate = new Date(paper.published).toLocaleDateString();
        
        return `
            <div class="paper-card" onclick="selectPaper(${index})">
                <div class="paper-card-header">
                    <div class="paper-title">${escapeHtml(paper.title)}</div>
                    <button class="paper-bookmark ${isBookmarked ? 'bookmarked' : ''}" 
                            onclick="toggleBookmark(event, ${index})" 
                            title="${isBookmarked ? 'Remove bookmark' : 'Bookmark paper'}">
                        <i class="fas fa-bookmark"></i>
                    </button>
                </div>
                <div class="paper-authors">Authors: ${paper.authors.join(', ')}</div>
                <div class="paper-abstract">${escapeHtml(paper.abstract.substring(0, 300))}...</div>
                <div class="paper-meta">
                    <span><i class="fas fa-calendar"></i> ${publishedDate}</span>
                    <span><i class="fas fa-tags"></i> ${paper.categories.slice(0, 3).join(', ')}</span>
                </div>
            </div>
        `;
    }).join('');
    
    // Store papers globally for selection
    window.currentPapers = papers;
}

function selectPaper(paperIndex) {
    try {
        if (window.currentPapers && window.currentPapers[paperIndex]) {
            selectedPaper = window.currentPapers[paperIndex];
            currentConversation = []; // Reset conversation
            showChatSection();
            showToast('Paper selected for chat', 'success');
        }
    } catch (error) {
        console.error('Error selecting paper:', error);
        showToast('Error selecting paper', 'error');
    }
}

function showChatSection() {
    const chatSection = document.querySelector('.chat-section');
    const paperInfo = document.getElementById('selectedPaper');
    
    paperInfo.innerHTML = `
        <h3>${escapeHtml(selectedPaper.title)}</h3>
        <p><strong>Authors:</strong> ${selectedPaper.authors.join(', ')}</p>
        <p><strong>Published:</strong> ${new Date(selectedPaper.published).toLocaleDateString()}</p>
        <p><strong>Abstract:</strong> ${escapeHtml(selectedPaper.abstract.substring(0, 300))}...</p>
        <p><strong>Categories:</strong> ${selectedPaper.categories.join(', ')}</p>
    `;
    
    chatSection.style.display = 'block';
    document.getElementById('chatMessages').innerHTML = '';
    
    // Add welcome message with enhanced formatting
    addMessage('assistant', `**Welcome!** I'm ready to help you understand this paper: **"${selectedPaper.title}"**\n\nFeel free to ask me about:\n- 🔬 **Methodology**: How the research was conducted\n- 📊 **Results**: Key findings and conclusions\n- 🧠 **Concepts**: Technical terms and theories\n- 🌐 **Context**: How this fits in the broader field\n- 💡 **Implications**: Real-world applications and impact`);
    
    // Scroll to chat section
    chatSection.scrollIntoView({ behavior: 'smooth' });
}

// Enhanced chat functionality with markdown support
async function sendMessage() {
    const input = document.getElementById('chatQuery');
    const message = input.value.trim();
    
    if (!message || !selectedPaper) {
        showToast('Please enter a message', 'warning');
        return;
    }

    const messagesDiv = document.getElementById('chatMessages');
    const sendBtn = document.getElementById('sendBtn');
    
    // Add user message
    addMessage('user', message);
    currentConversation.push({ role: 'user', content: message, timestamp: new Date() });
    input.value = '';

    // Update button state
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

    // Add loading message
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message loading';
    loadingDiv.textContent = '🤔 AI is analyzing the paper and formulating a comprehensive response...';
    messagesDiv.appendChild(loadingDiv);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                paper_id: selectedPaper.id,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        messagesDiv.removeChild(loadingDiv);
        
        if (data.response) {
            addMessage('assistant', data.response);
            currentConversation.push({ role: 'assistant', content: data.response, timestamp: new Date() });
            showToast('Response generated successfully', 'success');
        } else {
            addMessage('assistant', 'Sorry, I could not generate a response.');
            showToast('No response generated', 'warning');
        }
    } catch (error) {
        console.error('Chat error:', error);
        messagesDiv.removeChild(loadingDiv);
        addMessage('assistant', '❌ **Error**: Could not get response from AI. Please try again.\n\n*This might be due to network issues or API limits.*');
        showToast('Chat failed. Please try again.', 'error');
    } finally {
        // Reset button state
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
    }
}

// Enhanced message rendering with markdown support
function addMessage(role, content) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    // Render markdown if marked library is available
    if (typeof marked !== 'undefined' && role === 'assistant') {
        try {
            // Convert markdown to HTML
            const htmlContent = marked.parse(content);
            messageDiv.innerHTML = htmlContent;
        } catch (error) {
            console.warn('Markdown parsing failed:', error);
            messageDiv.textContent = content;
        }
    } else {
        // For user messages or when markdown isn't available, use plain text
        messageDiv.textContent = content;
    }
    
    // Add timestamp for better UX
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = new Date().toLocaleTimeString();
    messageDiv.appendChild(timestamp);
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Bookmark functionality
function toggleBookmark(event, paperIndex) {
    event.stopPropagation(); // Prevent paper selection
    
    const paper = window.currentPapers[paperIndex];
    const existingIndex = bookmarkedPapers.findIndex(b => b.id === paper.id);
    
    if (existingIndex >= 0) {
        // Remove bookmark
        bookmarkedPapers.splice(existingIndex, 1);
        event.target.closest('.paper-bookmark').classList.remove('bookmarked');
        showToast('Bookmark removed', 'success');
    } else {
        // Add bookmark
        bookmarkedPapers.push({
            ...paper,
            bookmarkedAt: new Date().toISOString()
        });
        event.target.closest('.paper-bookmark').classList.add('bookmarked');
        showToast('Paper bookmarked', 'success');
    }
    
    localStorage.setItem('arxivChat_bookmarks', JSON.stringify(bookmarkedPapers));
    loadBookmarks();
}

// Search history functionality
function addToSearchHistory(query, resultCount) {
    const historyItem = {
        query,
        resultCount,
        timestamp: new Date().toISOString()
    };
    
    // Remove duplicate if exists
    searchHistory = searchHistory.filter(item => item.query !== query);
    
    // Add to beginning
    searchHistory.unshift(historyItem);
    
    // Keep only last 50 searches
    searchHistory = searchHistory.slice(0, 50);
    
    localStorage.setItem('arxivChat_searchHistory', JSON.stringify(searchHistory));
    loadSearchHistory();
}

function loadSearchHistory() {
    const historyList = document.getElementById('historyList');
    
    if (searchHistory.length === 0) {
        historyList.innerHTML = '<p>No search history yet</p>';
        return;
    }
    
    historyList.innerHTML = searchHistory.map(item => `
        <div class="history-item" onclick="repeatSearch('${escapeHtml(item.query)}')">
            <div><strong>${escapeHtml(item.query)}</strong></div>
            <div>${item.resultCount} results</div>
            <time>${new Date(item.timestamp).toLocaleString()}</time>
        </div>
    `).join('');
}

function loadBookmarks() {
    const bookmarksList = document.getElementById('bookmarksList');
    
    if (bookmarkedPapers.length === 0) {
        bookmarksList.innerHTML = '<p>No bookmarked papers yet</p>';
        return;
    }
    
    bookmarksList.innerHTML = bookmarkedPapers.map((paper, index) => `
        <div class="bookmark-item" onclick="selectBookmarkedPaper(${index})">
            <div><strong>${escapeHtml(paper.title.substring(0, 80))}...</strong></div>
            <div class="date">Bookmarked: ${new Date(paper.bookmarkedAt).toLocaleDateString()}</div>
        </div>
    `).join('');
}

function repeatSearch(query) {
    document.getElementById('searchQuery').value = query;
    closePanels();
    searchPapers();
}

function selectBookmarkedPaper(index) {
    selectedPaper = bookmarkedPapers[index];
    currentConversation = [];
    showChatSection();
    closePanels();
    showToast('Bookmarked paper selected', 'success');
}

// Panel management
function toggleHistory() {
    const panel = document.getElementById('historyPanel');
    const bookmarksPanel = document.getElementById('bookmarksPanel');
    
    bookmarksPanel.classList.remove('active');
    panel.classList.toggle('active');
}

function toggleBookmarks() {
    const panel = document.getElementById('bookmarksPanel');
    const historyPanel = document.getElementById('historyPanel');
    
    historyPanel.classList.remove('active');
    panel.classList.toggle('active');
}

function closePanels() {
    document.getElementById('historyPanel').classList.remove('active');
    document.getElementById('bookmarksPanel').classList.remove('active');
}

// Export functionality
function exportConversation() {
    if (currentConversation.length === 0) {
        showToast('No conversation to export', 'warning');
        return;
    }
    
    const exportData = {
        paper: {
            title: selectedPaper.title,
            authors: selectedPaper.authors,
            abstract: selectedPaper.abstract,
            published: selectedPaper.published
        },
        conversation: currentConversation,
        exportedAt: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `arxivchat_${selectedPaper.id}_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    showToast('Conversation exported', 'success');
}

// Clear functions
function clearChat() {
    if (currentConversation.length === 0) {
        showToast('No conversation to clear', 'warning');
        return;
    }
    
    if (confirm('Clear current conversation?')) {
        document.getElementById('chatMessages').innerHTML = '';
        currentConversation = [];
        showToast('Conversation cleared', 'success');
    }
}

function clearHistory() {
    if (searchHistory.length === 0) {
        showToast('No history to clear', 'warning');
        return;
    }
    
    if (confirm('Clear all search history?')) {
        searchHistory = [];
        localStorage.removeItem('arxivChat_searchHistory');
        loadSearchHistory();
        showToast('Search history cleared', 'success');
    }
}

function clearBookmarks() {
    if (bookmarkedPapers.length === 0) {
        showToast('No bookmarks to clear', 'warning');
        return;
    }
    
    if (confirm('Clear all bookmarks?')) {
        bookmarkedPapers = [];
        localStorage.removeItem('arxivChat_bookmarks');
        loadBookmarks();
        showToast('Bookmarks cleared', 'success');
    }
}

// Toast notifications
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event listeners
document.getElementById('searchQuery').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchPapers();
    }
});

document.getElementById('chatQuery').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Handle escape key to close panels
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closePanels();
    }
});

// Handle click outside to close panels
document.addEventListener('click', function(e) {
    const historyPanel = document.getElementById('historyPanel');
    const bookmarksPanel = document.getElementById('bookmarksPanel');
    
    // Check if click is outside both panels and not on trigger buttons
    if (!historyPanel.contains(e.target) && 
        !bookmarksPanel.contains(e.target) &&
        !e.target.closest('button[onclick*="toggleHistory"]') &&
        !e.target.closest('button[onclick*="toggleBookmarks"]')) {
        closePanels();
    }
});
