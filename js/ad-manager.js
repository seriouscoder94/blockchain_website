// Ad Manager Configuration
const AD_SLOTS = {
    'sidebar': {
        'adSlot': '',  // Paste your sidebar ad unit ID here
        'format': 'auto',
        'style': 'display:block'
    },
    'inContent': {
        'adSlot': '',  // Paste your in-content ad unit ID here
        'format': 'auto',
        'style': 'display:block'
    },
    'footer': {
        'adSlot': '',  // Paste your footer ad unit ID here
        'format': 'auto',
        'style': 'display:block'
    }
};

// Initialize ads
function initAds() {
    // Show ad slots again
    const adSlots = document.querySelectorAll('.ad-slot');
    adSlots.forEach(slot => {
        slot.style.display = 'block';
    });
}

// Place ads in designated slots
function placeAds() {
    const adSlots = document.querySelectorAll('.ad-slot');
    adSlots.forEach(slot => {
        const slotType = slot.getAttribute('data-ad-type');
        if (AD_SLOTS[slotType]) {
            slot.innerHTML = `
                <ins class="adsbygoogle"
                    style="display:block"
                    data-ad-client="pub-9345743366640756"
                    data-ad-slot="${AD_SLOTS[slotType].adSlot}"
                    data-ad-format="${AD_SLOTS[slotType].format}"
                    data-full-width-responsive="true">
                </ins>
            `;
            (adsbygoogle = window.adsbygoogle || []).push({});
        }
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initAds();
    placeAds();
});
