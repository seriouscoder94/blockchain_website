// Initialize Coinbase Wallet
async function initCoinbaseWallet() {
    if (typeof window.CoinbaseWalletSDK !== 'undefined') {
        const coinbaseWallet = new CoinbaseWalletSDK({
            appName: 'BlockchainFriendly',
            appLogoUrl: '/images/logo.png',
            darkMode: false
        });
        
        window.web3 = new Web3(coinbaseWallet.makeWeb3Provider());
        try {
            const accounts = await window.web3.eth.requestAccounts();
            return accounts.length > 0;
        } catch (error) {
            console.error("Coinbase Wallet connection failed:", error);
            return false;
        }
    }
    return false;
}

// Payment addresses
const PAYMENT_ADDRESSES = {
    'ETH': '0xf3cB0eF05a345f3397fE9CDCDd5Ec1d125550E1e',
    'BTC': '3FwU7EcARSFMut2AUBT1dxV4i1n7KA1QzY',
    'USDC': '0x88B98B7A482D1B83e414bbE772340e936EE9DC86'
};

// Handle crypto donations
function handleDonation(amount, currency) {
    // Show QR code and copy button immediately
    showQRCode(currency);
    showCopyAddress(currency);
    
    // Show mobile wallet options
    showMobileWalletOptions(currency, amount);
}

// Display QR code for crypto address
function showQRCode(currency) {
    const qrContainer = document.getElementById('qr-code');
    qrContainer.innerHTML = '';
    qrContainer.style.display = 'block';
    
    QRCode.toCanvas(qrContainer, PAYMENT_ADDRESSES[currency], function (error) {
        if (error) console.error(error);
    });
}

// Show copy address button
function showCopyAddress(currency) {
    const copyBtn = document.getElementById('copy-address');
    copyBtn.style.display = 'block';
    copyBtn.onclick = function() {
        navigator.clipboard.writeText(PAYMENT_ADDRESSES[currency]);
        alert('Address copied to clipboard!');
    };
}

// Show mobile wallet options
function showMobileWalletOptions(currency, amount) {
    const walletLinks = document.getElementById('wallet-links');
    if (!walletLinks) return;

    // Clear previous links
    walletLinks.innerHTML = '';

    // Add links for different wallets
    const links = {
        'ETH': [
            {name: 'MetaMask', url: `ethereum:${PAYMENT_ADDRESSES[currency]}?value=${amount}`},
            {name: 'Coinbase', url: `https://wallet.coinbase.com/send?address=${PAYMENT_ADDRESSES[currency]}&asset=ETH&amount=${amount}`},
            {name: 'Trust Wallet', url: `trust://send?address=${PAYMENT_ADDRESSES[currency]}&asset=ETH&amount=${amount}`}
        ],
        'BTC': [
            {name: 'Coinbase', url: `https://wallet.coinbase.com/send?address=${PAYMENT_ADDRESSES[currency]}&asset=BTC&amount=${amount}`},
            {name: 'Trust Wallet', url: `trust://send?address=${PAYMENT_ADDRESSES[currency]}&asset=BTC&amount=${amount}`}
        ],
        'USDC': [
            {name: 'Coinbase', url: `https://wallet.coinbase.com/send?address=${PAYMENT_ADDRESSES[currency]}&asset=USDC&amount=${amount}`},
            {name: 'MetaMask', url: `ethereum:${PAYMENT_ADDRESSES[currency]}?value=${amount}`}
        ]
    };

    links[currency].forEach(link => {
        const button = document.createElement('a');
        button.href = link.url;
        button.className = 'wallet-link';
        button.target = '_blank';
        button.textContent = `Open in ${link.name}`;
        walletLinks.appendChild(button);
    });
}
