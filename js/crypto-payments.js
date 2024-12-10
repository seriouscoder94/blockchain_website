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

// Payment addresses - replace with your Coinbase addresses
const PAYMENT_ADDRESSES = {
    'ETH': '0xf3cB0eF05a345f3397fE9CDCDd5Ec1d125550E1e', // Replace everything after 'ETH': with your Ethereum address in quotes
    'BTC': '3FwU7EcARSFMut2AUBT1dxV4i1n7KA1QzY',   // Replace everything after 'BTC': with your Bitcoin address in quotes
    'USDC': '0x88B98B7A482D1B83e414bbE772340e936EE9DC86' // Replace everything after 'USDC': with your USDC address in quotes
}

// Handle crypto donations
async function handleDonation(amount, currency) {
    if (!await initCoinbaseWallet()) {
        window.open('https://www.coinbase.com/wallet', '_blank');
        alert('Please install Coinbase Wallet to make crypto payments!');
        return;
    }

    try {
        const accounts = await web3.eth.getAccounts();
        
        if (currency === 'ETH') {
            await web3.eth.sendTransaction({
                from: accounts[0],
                to: PAYMENT_ADDRESSES[currency],
                value: web3.utils.toWei(amount, 'ether')
            });
        } else {
            // For other currencies, show QR code and address
            showQRCode(currency);
            showCopyAddress(currency);
        }
        
    } catch (error) {
        alert('Transaction failed: ' + error.message);
    }
}

// Display QR code for crypto address
function showQRCode(currency) {
    const address = PAYMENT_ADDRESSES[currency];
    const qrContainer = document.getElementById('qr-code');
    qrContainer.innerHTML = '';
    new QRCode(qrContainer, address);
    
    // Show the address text
    const addressText = document.createElement('div');
    addressText.className = 'address-text';
    addressText.textContent = address;
    qrContainer.appendChild(addressText);
}

// Show copy address button
function showCopyAddress(currency) {
    const address = PAYMENT_ADDRESSES[currency];
    const copyBtn = document.getElementById('copy-address');
    copyBtn.style.display = 'block';
    copyBtn.onclick = () => {
        navigator.clipboard.writeText(address);
        alert('Address copied to clipboard!');
    };
}
