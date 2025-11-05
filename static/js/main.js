// Main JavaScript for Ultimate Agent Directory

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Add external link icons
    document.querySelectorAll('a[target="_blank"]').forEach(link => {
        if (!link.querySelector('.fa-external-link-alt')) {
            // Link already has icon or doesn't need one
        }
    });

    // Animate stats on scroll (if IntersectionObserver is supported)
    if ('IntersectionObserver' in window) {
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('stat-counter');
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.stat-counter, [class*="font-bold text-"]').forEach(stat => {
            statsObserver.observe(stat);
        });
    }

    // Copy to clipboard functionality for code snippets (if any)
    document.querySelectorAll('pre code').forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-btn absolute top-2 right-2 bg-gray-700 text-white px-3 py-1 rounded text-sm hover:bg-gray-600';
        button.textContent = 'Copy';

        button.addEventListener('click', function() {
            const code = block.textContent;
            navigator.clipboard.writeText(code).then(() => {
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            });
        });

        const pre = block.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(button);
    });

    // Add loading animation for images
    document.querySelectorAll('img').forEach(img => {
        if (!img.complete) {
            img.classList.add('opacity-0');
            img.addEventListener('load', function() {
                this.classList.remove('opacity-0');
                this.classList.add('transition-opacity', 'duration-300');
            });
        }
    });

    // Log page view (optional analytics hook)
    console.log('Page loaded:', window.location.pathname);
});

// Utility Functions

/**
 * Debounce function to limit rate of function calls
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Format number with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Highlight search terms in text
 */
function highlightText(text, searchTerm) {
    if (!searchTerm) return escapeHtml(text);

    const escaped = escapeHtml(text);
    const regex = new RegExp(`(${escapeHtml(searchTerm)})`, 'gi');
    return escaped.replace(regex, '<span class="search-highlight">$1</span>');
}

// Export utilities for use in other scripts
window.Utils = {
    debounce,
    formatNumber,
    escapeHtml,
    highlightText
};
