// Fetch crypto prices
async function fetchCryptoPrices() {
    try {
        const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple,solana&vs_currencies=usd&include_24hr_change=true');
        const data = await response.json();

        // Update Bitcoin
        const bitcoinCard = document.getElementById('bitcoin');
        if (bitcoinCard) {
            const bitcoinPrice = bitcoinCard.querySelector('.price');
            const bitcoinChange = bitcoinCard.querySelector('.change');
            bitcoinPrice.textContent = `$${data.bitcoin.usd.toLocaleString()}`;
            const btcChange = data.bitcoin.usd_24h_change.toFixed(2);
            bitcoinChange.textContent = `24h: ${btcChange}%`;
            bitcoinChange.className = `change ${btcChange >= 0 ? 'positive' : 'negative'}`;
        }

        // Update Ethereum
        const ethereumCard = document.getElementById('ethereum');
        if (ethereumCard) {
            const ethereumPrice = ethereumCard.querySelector('.price');
            const ethereumChange = ethereumCard.querySelector('.change');
            ethereumPrice.textContent = `$${data.ethereum.usd.toLocaleString()}`;
            const ethChange = data.ethereum.usd_24h_change.toFixed(2);
            ethereumChange.textContent = `24h: ${ethChange}%`;
            ethereumChange.className = `change ${ethChange >= 0 ? 'positive' : 'negative'}`;
        }

        // Update XRP
        const rippleCard = document.getElementById('ripple');
        if (rippleCard) {
            const ripplePrice = rippleCard.querySelector('.price');
            const rippleChange = rippleCard.querySelector('.change');
            ripplePrice.textContent = `$${data.ripple.usd.toLocaleString()}`;
            const xrpChange = data.ripple.usd_24h_change.toFixed(2);
            rippleChange.textContent = `24h: ${xrpChange}%`;
            rippleChange.className = `change ${xrpChange >= 0 ? 'positive' : 'negative'}`;
        }

        // Update Solana
        const solanaCard = document.getElementById('solana');
        if (solanaCard) {
            const solanaPrice = solanaCard.querySelector('.price');
            const solanaChange = solanaCard.querySelector('.change');
            solanaPrice.textContent = `$${data.solana.usd.toLocaleString()}`;
            const solChange = data.solana.usd_24h_change.toFixed(2);
            solanaChange.textContent = `24h: ${solChange}%`;
            solanaChange.className = `change ${solChange >= 0 ? 'positive' : 'negative'}`;
        }

        // Update BNB
        const bnbCard = document.getElementById('binancecoin');
        if (bnbCard) {
            const bnbPrice = bnbCard.querySelector('.price');
            const bnbChange = bnbCard.querySelector('.change');
            bnbPrice.textContent = `$${data.binancecoin.usd.toLocaleString()}`;
            const bnbChange24h = data.binancecoin.usd_24h_change.toFixed(2);
            bnbChange.textContent = `24h: ${bnbChange24h}%`;
            bnbChange.className = `change ${bnbChange24h >= 0 ? 'positive' : 'negative'}`;
        }
    } catch (error) {
        console.error('Error fetching crypto prices:', error);
    }
}

// Update prices every 30 seconds
fetchCryptoPrices();
setInterval(fetchCryptoPrices, 30000);

// Floating blocks animation
const createBlock = () => {
    const block = document.createElement('div');
    block.classList.add('floating-block');
    
    // Random position
    block.style.left = Math.random() * 100 + 'vw';
    block.style.animationDuration = Math.random() * 3 + 2 + 's';
    block.style.opacity = Math.random() * 0.5 + 0.1;
    
    document.querySelector('.hero').appendChild(block);
    
    // Remove block after animation
    block.addEventListener('animationend', () => {
        block.remove();
    });
};

// Create blocks periodically
setInterval(createBlock, 500);
