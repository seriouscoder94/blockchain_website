// Social Share Functions
function shareOnTwitter() {
    const text = "Check out BlockchainFriendly - Your simple guide to blockchain and cryptocurrency!";
    const url = window.location.href;
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
    window.open(twitterUrl, '_blank');
}

function shareOnFacebook() {
    const url = window.location.href;
    const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
    window.open(facebookUrl, '_blank');
}

function shareOnLinkedIn() {
    const url = window.location.href;
    const title = "BlockchainFriendly - Your Simple Guide to Blockchain";
    const linkedInUrl = `https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`;
    window.open(linkedInUrl, '_blank');
}

function shareOnWhatsApp() {
    const text = "Check out BlockchainFriendly - Your simple guide to blockchain and cryptocurrency!";
    const url = window.location.href;
    const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(text + ' ' + url)}`;
    window.open(whatsappUrl, '_blank');
}
