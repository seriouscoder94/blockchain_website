// Reddit Community Integration
async function updateRedditStats() {
    try {
        const response = await fetch('https://www.reddit.com/r/BlockchainFriendly/about.json', {
            headers: {
                'Accept': 'application/json'
            }
        });
        const data = await response.json();
        
        // Update member count
        const memberCount = document.getElementById('reddit-members');
        if (memberCount && data.data) {
            memberCount.textContent = new Intl.NumberFormat().format(data.data.subscribers || 0);
        }
        
        // Update online count
        const onlineCount = document.getElementById('reddit-online');
        if (onlineCount && data.data) {
            onlineCount.textContent = new Intl.NumberFormat().format(data.data.active_user_count || 0);
        }
    } catch (error) {
        // Handle silently
    }
}

// Fetch Reddit posts
async function fetchRedditPosts(sortBy = 'hot') {
    const postsContainer = document.getElementById('reddit-posts');
    if (!postsContainer) return;

    postsContainer.innerHTML = '<div class="loading-spinner">Loading posts...</div>';

    try {
        const response = await fetch(`https://www.reddit.com/r/BlockchainFriendly/${sortBy}.json`, {
            headers: {
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        postsContainer.innerHTML = ''; // Clear loading message
        
        if (!data.data || !data.data.children || data.data.children.length === 0) {
            postsContainer.innerHTML = '<div class="no-posts">No posts available at the moment. Check back soon!</div>';
            return;
        }
        
        data.data.children.forEach(post => {
            if (post.data) {
                const postElement = createPostElement(post.data);
                postsContainer.appendChild(postElement);
            }
        });
    } catch (error) {
        postsContainer.innerHTML = '<div class="no-posts">Loading posts...</div>';
    }
}

// Create post element
function createPostElement(postData) {
    const postDiv = document.createElement('div');
    postDiv.className = 'reddit-post';
    
    // Format timestamp
    const timestamp = new Date(postData.created_utc * 1000);
    const timeAgo = formatTimeAgo(timestamp);
    
    // Handle possible undefined values
    const title = postData.title || 'Untitled';
    const author = postData.author || '[deleted]';
    const ups = postData.ups || 0;
    const numComments = postData.num_comments || 0;
    const selftext = postData.selftext || '';
    
    postDiv.innerHTML = `
        <div class="post-header">
            <span class="post-author">Posted by u/${author} ${timeAgo}</span>
        </div>
        <a href="https://reddit.com${postData.permalink}" target="_blank" class="post-title">
            ${escapeHtml(title)}
        </a>
        ${selftext ? `
        <div class="post-content">
            ${escapeHtml(truncateText(selftext, 300))}
        </div>
        ` : ''}
        <div class="post-footer">
            <span class="post-votes">
                <i class="fas fa-arrow-up"></i> ${formatNumber(ups)}
            </span>
            <span class="post-comments">
                <i class="fas fa-comment"></i> ${formatNumber(numComments)}
            </span>
        </div>
    `;
    
    return postDiv;
}

// Helper function to escape HTML and prevent XSS
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Helper functions
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

function formatNumber(num) {
    if (!num) return '0';
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };
    
    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval === 1 ? '' : 's'} ago`;
        }
    }
    
    return 'just now';
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    updateRedditStats();
    fetchRedditPosts('hot');
    
    const sortSelect = document.getElementById('post-sort');
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            fetchRedditPosts(e.target.value);
        });
    }
});

// Update stats periodically
setInterval(updateRedditStats, 300000);
