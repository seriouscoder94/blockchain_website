// CryptoCompare API Configuration
const PRICE_API_KEY = 'c333855c293224de4b44b3dc5d37a945d161603986be391689ffb533afccf865';
const TOP_COINS = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'ADA', 'DOGE', 'TRX', 'LINK', 'DOT'];
let currentTimeframe = '24h';

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', () => {
    initializeDashboard();
    // Update prices every 30 seconds
    setInterval(updatePrices, 30000);

    // Add event listeners to timeframe buttons
    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            currentTimeframe = button.dataset.timeframe;
            updatePrices();
        });
    });
});

async function initializeDashboard() {
    try {
        await updatePrices();
    } catch (error) {
        console.error('Error initializing dashboard:', error);
    }
}

async function updatePrices() {
    try {
        const priceData = await fetchPriceData();
        displayPrices(priceData);
    } catch (error) {
        console.error('Error updating prices:', error);
    }
}

async function fetchPriceData() {
    const response = await fetch(`https://min-api.cryptocompare.com/data/pricemultifull?fsyms=${TOP_COINS.join(',')}&tsyms=USD&api_key=${PRICE_API_KEY}`);
    const data = await response.json();
    return data.RAW;
}

function displayPrices(priceData) {
    const priceGrid = document.querySelector('.price-grid');
    priceGrid.innerHTML = '';

    TOP_COINS.forEach(coin => {
        if (priceData[coin] && priceData[coin].USD) {
            const coinData = priceData[coin].USD;
            const card = createPriceCard(coin, coinData);
            priceGrid.appendChild(card);
        }
    });
}

function createPriceCard(coin, data) {
    const card = document.createElement('div');
    card.className = 'price-card';
    
    const priceChange = data.CHANGEPCT24HOUR;
    const changeClass = priceChange >= 0 ? 'positive' : 'negative';
    const changeIcon = priceChange >= 0 ? '↑' : '↓';

    card.innerHTML = `
        <div class="coin-header">
            <img src="https://www.cryptocompare.com${data.IMAGEURL}" alt="${coin}" class="coin-icon">
            <h3>${coin}/USD</h3>
        </div>
        <div class="price-info">
            <p class="current-price">$${data.PRICE.toFixed(2)}</p>
            <p class="price-change ${changeClass}">
                ${changeIcon} ${Math.abs(priceChange).toFixed(2)}%
            </p>
        </div>
        <div class="price-details">
            <div class="detail">
                <span>24h High</span>
                <span>$${data.HIGH24HOUR.toFixed(2)}</span>
            </div>
            <div class="detail">
                <span>24h Low</span>
                <span>$${data.LOW24HOUR.toFixed(2)}</span>
            </div>
            <div class="detail">
                <span>Volume 24h</span>
                <span>$${(data.VOLUME24HOUR).toFixed(0)}</span>
            </div>
            <div class="detail">
                <span>Market Cap</span>
                <span>$${(data.MKTCAP).toFixed(0)}</span>
            </div>
        </div>
    `;

    return card;
}
