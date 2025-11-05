// Category Page - Filtering and Sorting

let allCards = [];
let activeFilters = {
    search: '',
    type: '',
    pricing: '',
    tags: [],
    sort: 'name'
};

// Initialize category page
document.addEventListener('DOMContentLoaded', function() {
    allCards = Array.from(document.querySelectorAll('.agent-card'));

    initializeSearch();
    initializeFilters();
    initializeSorting();
    initializeTags();

    // Initial render
    applyFiltersAndSort();
});

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('category-search');
    if (!searchInput) return;

    const debouncedSearch = window.Utils.debounce((query) => {
        activeFilters.search = query.toLowerCase();
        applyFiltersAndSort();
    }, 300);

    searchInput.addEventListener('input', function(e) {
        debouncedSearch(e.target.value);
    });

    // Clear on Escape
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            this.value = '';
            activeFilters.search = '';
            applyFiltersAndSort();
        }
    });
}

// Type and Pricing filters
function initializeFilters() {
    const typeFilter = document.getElementById('filter-type');
    const pricingFilter = document.getElementById('filter-pricing');

    if (typeFilter) {
        typeFilter.addEventListener('change', function() {
            activeFilters.type = this.value;
            applyFiltersAndSort();
        });
    }

    if (pricingFilter) {
        pricingFilter.addEventListener('change', function() {
            activeFilters.pricing = this.value;
            applyFiltersAndSort();
        });
    }
}

// Tag filtering
function initializeTags() {
    const tagButtons = document.querySelectorAll('.tag-btn');

    tagButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const tag = this.dataset.tag;

            if (activeFilters.tags.includes(tag)) {
                // Remove tag
                activeFilters.tags = activeFilters.tags.filter(t => t !== tag);
                this.classList.remove('active');
            } else {
                // Add tag
                activeFilters.tags.push(tag);
                this.classList.add('active');
            }

            applyFiltersAndSort();
        });
    });
}

// Sorting functionality
function initializeSorting() {
    const sortButtons = document.querySelectorAll('.sort-btn');

    sortButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const sortBy = this.dataset.sort;

            // Update active state
            sortButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            activeFilters.sort = sortBy;
            applyFiltersAndSort();
        });
    });
}

// Check if card matches filters
function cardMatchesFilters(card) {
    // Search filter
    if (activeFilters.search) {
        const name = card.dataset.name || '';
        const description = card.dataset.description || '';
        const searchText = `${name} ${description}`.toLowerCase();

        if (!searchText.includes(activeFilters.search)) {
            return false;
        }
    }

    // Type filter
    if (activeFilters.type && card.dataset.type !== activeFilters.type) {
        return false;
    }

    // Pricing filter
    if (activeFilters.pricing && card.dataset.pricing !== activeFilters.pricing) {
        return false;
    }

    // Tag filter
    if (activeFilters.tags.length > 0) {
        const cardTags = card.dataset.tags ? card.dataset.tags.split(',') : [];
        const hasMatchingTag = activeFilters.tags.some(tag => cardTags.includes(tag));

        if (!hasMatchingTag) {
            return false;
        }
    }

    return true;
}

// Sort cards
function sortCards(cards) {
    const sorted = [...cards];

    switch (activeFilters.sort) {
        case 'name':
            sorted.sort((a, b) => {
                const nameA = a.dataset.name || '';
                const nameB = b.dataset.name || '';
                return nameA.localeCompare(nameB);
            });
            break;

        case 'stars':
            sorted.sort((a, b) => {
                const starsA = parseInt(a.dataset.stars) || 0;
                const starsB = parseInt(b.dataset.stars) || 0;
                return starsB - starsA; // Descending
            });
            break;

        case 'date':
            sorted.sort((a, b) => {
                const dateA = a.dataset.date || '';
                const dateB = b.dataset.date || '';
                return dateB.localeCompare(dateA); // Newest first
            });
            break;
    }

    return sorted;
}

// Apply all filters and sorting
function applyFiltersAndSort() {
    const container = document.getElementById('agents-container');
    const noResults = document.getElementById('no-results');
    const visibleCount = document.getElementById('visible-count');

    // Filter cards
    const visibleCards = allCards.filter(card => cardMatchesFilters(card));

    // Sort cards
    const sortedCards = sortCards(visibleCards);

    // Hide all cards first
    allCards.forEach(card => {
        card.classList.add('hidden');
    });

    // Show and reorder visible cards
    if (sortedCards.length > 0) {
        sortedCards.forEach(card => {
            card.classList.remove('hidden');
            container.appendChild(card); // Reorder in DOM
        });

        noResults.classList.add('hidden');
        visibleCount.textContent = sortedCards.length;
    } else {
        noResults.classList.remove('hidden');
        visibleCount.textContent = '0';
    }

    // Scroll to top of results
    if (window.scrollY > 200) {
        window.scrollTo({
            top: 200,
            behavior: 'smooth'
        });
    }
}

// Export for external use
window.CategoryFilter = {
    applyFiltersAndSort,
    resetFilters: function() {
        activeFilters = {
            search: '',
            type: '',
            pricing: '',
            tags: [],
            sort: 'name'
        };

        // Reset UI
        document.getElementById('category-search').value = '';
        document.getElementById('filter-type').value = '';
        document.getElementById('filter-pricing').value = '';
        document.querySelectorAll('.tag-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.sort-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector('.sort-btn[data-sort="name"]').classList.add('active');

        applyFiltersAndSort();
    }
};

// Add reset filters button functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add a reset button if it doesn't exist
    const filterSection = document.querySelector('#category-search')?.closest('section');
    if (filterSection && !document.getElementById('reset-filters')) {
        const resetBtn = document.createElement('button');
        resetBtn.id = 'reset-filters';
        resetBtn.className = 'mt-4 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg text-sm font-semibold transition';
        resetBtn.innerHTML = '<i class="fas fa-redo mr-2"></i>Reset All Filters';
        resetBtn.addEventListener('click', window.CategoryFilter.resetFilters);

        const sortSection = filterSection.querySelector('.flex.items-center.gap-4');
        if (sortSection) {
            sortSection.appendChild(resetBtn);
        }
    }
});
