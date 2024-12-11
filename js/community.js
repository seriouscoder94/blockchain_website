// Initialize DOMPurify and marked
const purify = DOMPurify;

// Store posts in localStorage
let posts = JSON.parse(localStorage.getItem('posts')) || [];
let currentUser = {
    username: 'Anonymous User',
    karma: 0
};

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');
    initializeUI();
});

function initializeUI() {
    console.log('Initializing UI components');
    
    // Initialize posts list
    loadPosts();
    console.log('Posts loaded');
    
    // Initialize Sort Selection
    initializeSortSelection();
    console.log('Sort selection initialized');
}

function initializeSortSelection() {
    const sortSelect = document.getElementById('sort-posts');
    if (sortSelect) {
        sortSelect.onchange = function() {
            sortPosts(this.value);
        };
    }
}

function addNewPost(title, content, flair) {
    const post = {
        id: Date.now(),
        title: title,
        content: content,
        flair: flair,
        author: currentUser.username,
        timestamp: new Date().toISOString(),
        upvotes: 1,
        downvotes: 0,
        comments: [],
        userVote: 'up' // User automatically upvotes their own post
    };
    
    posts.unshift(post);
    localStorage.setItem('posts', JSON.stringify(posts));
    loadPosts();
}

function loadPosts() {
    const postsList = document.getElementById('posts-list');
    if (!postsList) return;

    postsList.innerHTML = '';
    
    if (posts.length === 0) {
        postsList.innerHTML = `
            <div class="no-posts">
                <p>No posts yet. Be the first to share something!</p>
            </div>
        `;
        return;
    }
    
    posts.forEach(post => {
        const postElement = createPostElement(post);
        postsList.appendChild(postElement);
    });
}

function createPostElement(post) {
    const div = document.createElement('div');
    div.className = 'post';
    
    const timeAgo = getTimeAgo(post.timestamp);
    const voteScore = post.upvotes - post.downvotes;
    const renderedContent = marked.parse(purify.sanitize(post.content));
    
    div.innerHTML = `
        <div class="post-header">
            <span class="post-flair ${post.flair}">${post.flair}</span>
            <span class="post-author">Posted by ${post.author}</span>
            <span class="post-time">${timeAgo}</span>
        </div>
        <h2 class="post-title">${purify.sanitize(post.title)}</h2>
        <div class="post-content">${renderedContent}</div>
        <div class="post-footer">
            <div class="vote-buttons">
                <button class="vote-button ${post.userVote === 'up' ? 'upvoted' : ''}" 
                        onclick="handleVote(${post.id}, 'up')">
                    <i class="fas fa-arrow-up"></i>
                </button>
                <span class="vote-score">${voteScore}</span>
                <button class="vote-button ${post.userVote === 'down' ? 'downvoted' : ''}"
                        onclick="handleVote(${post.id}, 'down')">
                    <i class="fas fa-arrow-down"></i>
                </button>
            </div>
            <div class="post-actions">
                <div class="post-action" onclick="showComments(${post.id})">
                    <i class="fas fa-comment"></i>
                    <span>${post.comments.length} Comments</span>
                </div>
                <div class="post-action">
                    <i class="fas fa-share"></i>
                    <span>Share</span>
                </div>
                <div class="post-action">
                    <i class="fas fa-bookmark"></i>
                    <span>Save</span>
                </div>
            </div>
        </div>
    `;
    
    return div;
}

function handleVote(postId, voteType) {
    const post = posts.find(p => p.id === postId);
    if (!post) return;

    // Remove previous vote
    if (post.userVote === 'up') post.upvotes--;
    if (post.userVote === 'down') post.downvotes--;

    // Apply new vote
    if (voteType === 'up' && post.userVote !== 'up') {
        post.upvotes++;
        post.userVote = 'up';
    } else if (voteType === 'down' && post.userVote !== 'down') {
        post.downvotes++;
        post.userVote = 'down';
    } else {
        post.userVote = null; // Remove vote if clicking same button
    }

    localStorage.setItem('posts', JSON.stringify(posts));
    loadPosts();
}

function sortPosts(sortType) {
    switch (sortType) {
        case 'hot':
            posts.sort((a, b) => {
                const scoreA = (a.upvotes - a.downvotes) / Math.pow((Date.now() - new Date(a.timestamp).getTime()) / 3600000 + 2, 1.8);
                const scoreB = (b.upvotes - b.downvotes) / Math.pow((Date.now() - new Date(b.timestamp).getTime()) / 3600000 + 2, 1.8);
                return scoreB - scoreA;
            });
            break;
        case 'new':
            posts.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            break;
        case 'top':
            posts.sort((a, b) => (b.upvotes - b.downvotes) - (a.upvotes - a.downvotes));
            break;
    }
    loadPosts();
}

function showComments(postId) {
    const post = posts.find(p => p.id === postId);
    if (post) {
        alert(`This post has ${post.comments.length} comments`);
    }
}

function getTimeAgo(timestamp) {
    const seconds = Math.floor((new Date() - new Date(timestamp)) / 1000);
    
    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };
    
    for (let [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return interval === 1 ? `1 ${unit} ago` : `${interval} ${unit}s ago`;
        }
    }
    
    return 'Just now';
}
