// Helper function to close mobile menu
function closeMenu() {
    const navMenu = document.getElementById('navMenu');
    const hamburger = document.querySelector('.hamburger');
    const overlay = document.getElementById('menuOverlay');

    navMenu.classList.remove('active');
    hamburger.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
}

// Toggle Mobile Menu
function toggleMenu() {
    const navMenu = document.getElementById('navMenu');
    const hamburger = document.querySelector('.hamburger');
    const overlay = document.getElementById('menuOverlay');

    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
    overlay.classList.toggle('active');

    // Prevent body scroll when menu is open
    document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
}

// Mobile Dropdown Accordion
document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggles = document.querySelectorAll('.has-dropdown > a');
    const submenuToggles = document.querySelectorAll('.has-submenu > a');

    // Check if mobile
    function isMobile() {
        return window.innerWidth <= 1024;
    }

    // Dropdown toggle for mobile
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            if (isMobile()) {
                e.preventDefault();
                const parent = this.parentElement;
                const arrow = this.querySelector('.dropdown-arrow');

                // Toggle this dropdown
                const wasOpen = parent.classList.contains('open');

                // Close all dropdowns first
                document.querySelectorAll('.has-dropdown').forEach(item => {
                    item.classList.remove('open');
                    const itemArrow = item.querySelector('.dropdown-arrow');
                    if (itemArrow) itemArrow.textContent = '▼';
                });

                // If it wasn't open, open it
                if (!wasOpen) {
                    parent.classList.add('open');
                    if (arrow) arrow.textContent = '▲';
                }
            }
        });
    });

    // Submenu toggle for mobile
    submenuToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            if (isMobile()) {
                e.preventDefault();
                const parent = this.parentElement;
                const arrow = this.querySelector('.submenu-arrow');

                // Toggle submenu
                const wasOpen = parent.classList.contains('open');
                parent.classList.toggle('open');

                // Update arrow
                if (arrow) {
                    arrow.textContent = wasOpen ? '→' : '↓';
                }
            }
        });
    });

    // Sticky header on scroll
    const header = document.querySelector('header');

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Active link highlighting
    const currentLocation = window.location.pathname;
    const menuLinks = document.querySelectorAll('.nav-menu a:not([href^="#"])');

    menuLinks.forEach(link => {
        try {
            const linkPath = new URL(link.href).pathname;
            if (linkPath === currentLocation) {
                link.classList.add('active');
            }
        } catch (e) {
            // Skip invalid URLs
        }
    });

    // Keyboard accessibility
    document.addEventListener('keydown', function(e) {
        // Close menu on Escape
        if (e.key === 'Escape') {
            const navMenu = document.getElementById('navMenu');

            if (navMenu.classList.contains('active')) {
                closeMenu();
            }

            // Close open dropdowns
            document.querySelectorAll('.has-dropdown.open, .has-submenu.open').forEach(el => {
                el.classList.remove('open');
            });
        }
    });

    // Close menu when clicking on non-dropdown links
    document.querySelectorAll('.nav-menu a:not(.dropdown-toggle):not(.has-submenu > a)').forEach(link => {
        link.addEventListener('click', () => {
            if (isMobile()) {
                closeMenu();
            }
        });
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        if (!isMobile()) {
            // Close mobile menu if window is resized to desktop
            closeMenu();

            // Close all accordion items
            document.querySelectorAll('.has-dropdown.open, .has-submenu.open').forEach(el => {
                el.classList.remove('open');
            });
        }
    });
});

// Cookie Consent Management
function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const isSecure = window.location.protocol === 'https:';
    const secureFlag = isSecure ? ';Secure' : '';
    document.cookie = name + "=" + value + ";expires=" + date.toUTCString() + ";path=/;SameSite=Lax" + secureFlag;
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length);
    }
    return null;
}

function acceptCookies() {
    setCookie('cookieConsent', 'accepted', 365);
    document.getElementById('cookieBanner').classList.remove('show');
    // Tu dodasz kod Google Analytics gdy będzie gotowy
    loadGoogleAnalytics();
}

function rejectCookies() {
    setCookie('cookieConsent', 'rejected', 365);
    document.getElementById('cookieBanner').classList.remove('show');
}

function loadGoogleAnalytics() {
    // Placeholder - dodaj tutaj kod Google Analytics gdy będziesz gotowy
    // Przykład:
    // window.dataLayer = window.dataLayer || [];
    // function gtag(){dataLayer.push(arguments);}
    // gtag('js', new Date());
    // gtag('config', 'GA_MEASUREMENT_ID');
    console.log('Google Analytics załadowany (placeholder)');
}

// Check consent on page load
document.addEventListener('DOMContentLoaded', function() {
    const consent = getCookie('cookieConsent');
    if (!consent) {
        // Show banner if no consent given
        document.getElementById('cookieBanner').classList.add('show');
    } else if (consent === 'accepted') {
        // Load analytics if previously accepted
        loadGoogleAnalytics();
    }
});

