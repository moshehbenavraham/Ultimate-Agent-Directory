// Boilerplate Page - Filtering, Sorting, and Search

let allBoilerplates = [];
let activeFilters = {
    search: '',
    ecosystem: '',
    pricing: '',
    tags: [],
    sort: 'stars'
};

// Initialize boilerplate page
document.addEventListener('DOMContentLoaded', function() {
    allBoilerplates = Array.from(document.querySelectorAll('.boilerplate-card'));

    if (allBoilerplates.length === 0) return;

    initializeFromURL();
    initializeSearch();
    initializeFilters();
    initializeTags();
    initializeSorting();

    // Initial render
    applyFiltersAndSort();
});

// Read initial state from URL query parameters
function initializeFromURL() {
    const params = new URLSearchParams(window.location.search);

    if (params.has('search')) {
        activeFilters.search = params.get('search').toLowerCase();
        const searchInput = document.getElementById('boilerplate-search');
        if (searchInput) searchInput.value = params.get('search');
    }

    if (params.has('ecosystem')) {
        activeFilters.ecosystem = params.get('ecosystem');
        const ecosystemFilter = document.getElementById('filter-ecosystem');
        if (ecosystemFilter) ecosystemFilter.value = activeFilters.ecosystem;
    }

    if (params.has('pricing')) {
        activeFilters.pricing = params.get('pricing');
        const pricingFilter = document.getElementById('filter-pricing');
        if (pricingFilter) pricingFilter.value = activeFilters.pricing;
    }

    if (params.has('tags')) {
        activeFilters.tags = params.get('tags').split(',').filter(t => t);
        activeFilters.tags.forEach(tag => {
            const tagBtn = document.querySelector(`.tag-btn[data-tag="${tag}"]`);
            if (tagBtn) tagBtn.classList.add('active');
        });
    }

    if (params.has('sort')) {
        activeFilters.sort = params.get('sort');
        const sortBtn = document.querySelector(`.sort-btn[data-sort="${activeFilters.sort}"]`);
        if (sortBtn) {
            document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
            sortBtn.classList.add('active');
        }
    }
}

// Update URL with current filter state
function updateURL() {
    const params = new URLSearchParams();

    if (activeFilters.search) params.set('search', activeFilters.search);
    if (activeFilters.ecosystem) params.set('ecosystem', activeFilters.ecosystem);
    if (activeFilters.pricing) params.set('pricing', activeFilters.pricing);
    if (activeFilters.tags.length > 0) params.set('tags', activeFilters.tags.join(','));
    if (activeFilters.sort !== 'stars') params.set('sort', activeFilters.sort);

    const newURL = params.toString()
        ? `${window.location.pathname}?${params.toString()}`
        : window.location.pathname;

    window.history.replaceState({}, '', newURL);
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('boilerplate-search');
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

// Ecosystem and Pricing filters
function initializeFilters() {
    const ecosystemFilter = document.getElementById('filter-ecosystem');
    const pricingFilter = document.getElementById('filter-pricing');

    if (ecosystemFilter) {
        ecosystemFilter.addEventListener('change', function() {
            activeFilters.ecosystem = this.value;
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

    // Ecosystem filter
    if (activeFilters.ecosystem && card.dataset.ecosystem !== activeFilters.ecosystem) {
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
    const container = document.getElementById('boilerplates-container');
    const noResults = document.getElementById('no-results');
    const visibleCount = document.getElementById('visible-count');

    if (!container) return;

    // Filter cards
    const visibleCards = allBoilerplates.filter(card => cardMatchesFilters(card));

    // Sort cards
    const sortedCards = sortCards(visibleCards);

    // Hide all cards first
    allBoilerplates.forEach(card => {
        card.classList.add('hidden');
    });

    // Show and reorder visible cards
    if (sortedCards.length > 0) {
        sortedCards.forEach(card => {
            card.classList.remove('hidden');
            container.appendChild(card); // Reorder in DOM
        });

        if (noResults) noResults.classList.add('hidden');
        if (visibleCount) visibleCount.textContent = sortedCards.length;
    } else {
        if (noResults) noResults.classList.remove('hidden');
        if (visibleCount) visibleCount.textContent = '0';
    }

    // Update URL with current state
    updateURL();
}

// Export for external use
window.BoilerplateFilter = {
    applyFiltersAndSort,
    resetFilters: function() {
        activeFilters = {
            search: '',
            ecosystem: '',
            pricing: '',
            tags: [],
            sort: 'stars'
        };

        // Reset UI
        const searchInput = document.getElementById('boilerplate-search');
        if (searchInput) searchInput.value = '';

        const ecosystemFilter = document.getElementById('filter-ecosystem');
        if (ecosystemFilter) ecosystemFilter.value = '';

        const pricingFilter = document.getElementById('filter-pricing');
        if (pricingFilter) pricingFilter.value = '';

        document.querySelectorAll('.tag-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.sort-btn').forEach(btn => btn.classList.remove('active'));

        const defaultSortBtn = document.querySelector('.sort-btn[data-sort="stars"]');
        if (defaultSortBtn) defaultSortBtn.classList.add('active');

        applyFiltersAndSort();
    }
};

// Add reset filters button functionality
document.addEventListener('DOMContentLoaded', function() {
    const resetBtn = document.getElementById('reset-filters');
    if (resetBtn) {
        resetBtn.addEventListener('click', window.BoilerplateFilter.resetFilters);
    }
});
