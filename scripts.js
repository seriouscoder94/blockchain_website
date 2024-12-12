// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    const mobileMenuOverlay = document.querySelector('.mobile-menu-overlay');
    const body = document.body;

    function toggleMobileMenu() {
        mobileNavToggle.classList.toggle('active');
        navLinks.classList.toggle('active');
        body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
    }

    if (mobileNavToggle && navLinks && mobileMenuOverlay) {
        mobileNavToggle.addEventListener('click', function(e) {
            e.preventDefault();
            toggleMobileMenu();
        });

        mobileMenuOverlay.addEventListener('click', function(e) {
            e.preventDefault();
            if (navLinks.classList.contains('active')) {
                toggleMobileMenu();
            }
        });

        // Close menu when clicking a link
        const navLinksItems = navLinks.querySelectorAll('a');
        navLinksItems.forEach(link => {
            link.addEventListener('click', () => {
                if (navLinks.classList.contains('active')) {
                    toggleMobileMenu();
                }
            });
        });

        // Close menu when pressing Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                toggleMobileMenu();
            }
        });
    }
});
