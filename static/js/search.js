// Global Search for Homepage

let searchIndex = null;

// Load search index
async function loadSearchIndex() {
    try {
        const response = await fetch('/search-index.json');
        searchIndex = await response.json();
        console.log('Search index loaded:', searchIndex.length, 'entries');
    } catch (error) {
        console.error('Failed to load search index:', error);
        searchIndex = [];
    }
}

// Perform search
function performSearch(query) {
    if (!searchIndex || searchIndex.length === 0) {
        return [];
    }

    if (!query || query.trim().length < 2) {
        return [];
    }

    const searchTerm = query.toLowerCase().trim();
    const results = [];

    searchIndex.forEach(entry => {
        let score = 0;

        // Exact name match (highest priority)
        if (entry.name.toLowerCase() === searchTerm) {
            score += 100;
        }
        // Name contains search term
        else if (entry.name.toLowerCase().includes(searchTerm)) {
            score += 50;
        }

        // Description contains search term
        if (entry.description.toLowerCase().includes(searchTerm)) {
            score += 20;
        }

        // Tag match
        if (entry.tags && entry.tags.some(tag => tag.toLowerCase().includes(searchTerm))) {
            score += 30;
        }

        // Category match
        if (entry.category && entry.category.toLowerCase().includes(searchTerm)) {
            score += 10;
        }

        // Type match
        if (entry.type && entry.type.toLowerCase().includes(searchTerm)) {
            score += 10;
        }

        if (score > 0) {
            results.push({ ...entry, score });
        }
    });

    // Sort by score (descending) and return top 10
    return results.sort((a, b) => b.score - a.score).slice(0, 10);
}

// Display search results
function displaySearchResults(results, query) {
    const searchResults = document.getElementById('search-results');
    const resultsContainer = searchResults.querySelector('div');

    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="text-center py-8 text-gray-500">
                <i class="fas fa-search text-4xl mb-3 opacity-50"></i>
                <p>No results found for "<strong>${window.Utils.escapeHtml(query)}</strong>"</p>
                <p class="text-sm mt-2">Try different keywords or browse categories below</p>
            </div>
        `;
    } else {
        const html = results.map(result => `
            <div class="border-b border-gray-200 last:border-0 py-3">
                <div class="flex items-start justify-between gap-4">
                    <div class="flex-grow">
                        <h4 class="font-bold text-gray-900 mb-1">
                            <a href="${result.url}" target="_blank" class="hover:text-blue-600">
                                ${window.Utils.highlightText(result.name, query)}
                            </a>
                        </h4>
                        <p class="text-sm text-gray-600 mb-2">${window.Utils.escapeHtml(result.description.substring(0, 150))}${result.description.length > 150 ? '...' : ''}</p>
                        <div class="flex flex-wrap gap-2 text-xs">
                            <span class="bg-blue-100 text-blue-700 px-2 py-1 rounded">
                                ${result.category_title || result.category}
                            </span>
                            ${result.type ? `<span class="bg-gray-100 text-gray-700 px-2 py-1 rounded">${result.type}</span>` : ''}
                            ${result.github_stars ? `<span class="bg-yellow-100 text-yellow-700 px-2 py-1 rounded"><i class="fas fa-star mr-1"></i>${result.github_stars}</span>` : ''}
                        </div>
                    </div>
                    <a href="${window.BASE_URL || ''}/categories/${result.category}.html" class="text-blue-600 hover:underline text-sm whitespace-nowrap">
                        View Category <i class="fas fa-arrow-right ml-1"></i>
                    </a>
                </div>
            </div>
        `).join('');

        resultsContainer.innerHTML = `
            <div class="mb-3 text-sm text-gray-600">
                Found <strong>${results.length}</strong> result${results.length !== 1 ? 's' : ''} for "<strong>${window.Utils.escapeHtml(query)}</strong>"
            </div>
            ${html}
        `;
    }

    searchResults.classList.remove('hidden');
}

// Hide search results
function hideSearchResults() {
    const searchResults = document.getElementById('search-results');
    searchResults.classList.add('hidden');
}

// Initialize search
document.addEventListener('DOMContentLoaded', async function() {
    const searchInput = document.getElementById('global-search');

    if (!searchInput) return;

    // Load search index
    await loadSearchIndex();

    // Search input handler with debounce
    const debouncedSearch = window.Utils.debounce((query) => {
        if (query.trim().length < 2) {
            hideSearchResults();
            return;
        }

        const results = performSearch(query);
        displaySearchResults(results, query);
    }, 300);

    searchInput.addEventListener('input', function(e) {
        debouncedSearch(e.target.value);
    });

    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !document.getElementById('search-results').contains(e.target)) {
            hideSearchResults();
        }
    });

    // Show results again when focusing on input with existing query
    searchInput.addEventListener('focus', function() {
        if (this.value.trim().length >= 2) {
            const results = performSearch(this.value);
            displaySearchResults(results, this.value);
        }
    });

    // Clear search on Escape key
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            this.value = '';
            hideSearchResults();
            this.blur();
        }
    });
});
