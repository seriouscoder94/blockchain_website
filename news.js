// News API Configuration
const NEWS_API_KEY = 'c333855c293224de4b44b3dc5d37a945d161603986be391689ffb533afccf865'; 
const NEWS_API_URL = 'https://min-api.cryptocompare.com/data/v2/news/?lang=EN';

let currentPage = 1;
const newsPerPage = 12;
let currentCategory = 'all';
let allNews = [];

// Fetch news from the API
async function fetchNews() {
    try {
        const response = await fetch(`${NEWS_API_URL}&api_key=${NEWS_API_KEY}`);
        const data = await response.json();
        allNews = data.Data;
        displayNews(filterNewsByCategory(currentCategory));
    } catch (error) {
        console.error('Error fetching news:', error);
        document.getElementById('newsGrid').innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-circle"></i>
                <p>Failed to load news. Please try again later.</p>
            </div>
        `;
    }
}

// Filter news by category
function filterNewsByCategory(category) {
    if (category === 'all') return allNews;
    
    return allNews.filter(news => {
        const categories = news.categories.toLowerCase();
        const tags = (news.tags || '').toLowerCase();
        
        // Check both categories and tags for matches
        switch(category.toLowerCase()) {
            case 'defi':
                return categories.includes('defi') || 
                       categories.includes('decentralized finance') ||
                       tags.includes('defi') ||
                       tags.includes('decentralized finance');
            case 'nfts':
                return categories.includes('nft') ||
                       categories.includes('nfts') ||
                       tags.includes('nft') ||
                       tags.includes('nfts');
            default:
                return categories.includes(category.toLowerCase());
        }
    });
}

// Display news in the grid
function displayNews(newsArray) {
    const newsGrid = document.getElementById('newsGrid');
    const startIndex = (currentPage - 1) * newsPerPage;
    const endIndex = startIndex + newsPerPage;
    const newsToShow = newsArray.slice(startIndex, endIndex);

    if (currentPage === 1) {
        newsGrid.innerHTML = '';
    }

    newsToShow.forEach(news => {
        const newsCard = createNewsCard(news);
        newsGrid.appendChild(newsCard);
    });

    // Show/hide load more button
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (endIndex >= newsArray.length) {
        loadMoreBtn.style.display = 'none';
    } else {
        loadMoreBtn.style.display = 'inline-flex';
    }
}

// Create a news card element
function createNewsCard(news) {
    const card = document.createElement('article');
    card.className = 'news-card';
    
    // Format the published date
    const publishedDate = new Date(news.published_on * 1000);
    const formattedDate = publishedDate.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });

    card.innerHTML = `
        <img src="${news.imageurl}" alt="${news.title}" class="news-image" onerror="this.src='images/news-placeholder.jpg'">
        <div class="news-content">
            <span class="news-category">${news.categories}</span>
            <h3 class="news-title">${news.title}</h3>
            <p class="news-excerpt">${news.body.slice(0, 150)}...</p>
            <div class="news-meta">
                <div class="news-source">
                    <img src="${news.source_info.img}" alt="${news.source_info.name}" class="source-logo">
                    <span>${news.source_info.name}</span>
                </div>
                <span>${formattedDate}</span>
            </div>
        </div>
    `;

    // Add click event to open the full article
    card.addEventListener('click', () => {
        window.open(news.url, '_blank');
    });

    return card;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initial news load
    fetchNews();

    // Category buttons
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active button
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Update category and refresh news
            currentCategory = button.dataset.category;
            currentPage = 1;
            displayNews(filterNewsByCategory(currentCategory));
        });
    });

    // Load more button
    document.getElementById('loadMoreBtn').addEventListener('click', () => {
        currentPage++;
        displayNews(filterNewsByCategory(currentCategory));
    });
});

// Auto-refresh news every 5 minutes
setInterval(fetchNews, 300000);
