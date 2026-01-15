// Global Search for Homepage

let searchIndex = null;

function tokenizeQuery(query) {
    return query
        .toLowerCase()
        .trim()
        .split(/\s+/)
        .filter(token => token.length >= 2);
}

function tokenMatchesText(token, text) {
    if (!text) return false;
    const lower = text.toLowerCase();
    if (lower.includes(token)) return true;
    const words = lower.split(/[^a-z0-9]+/);
    return words.some(word => word.startsWith(token));
}

// Load search index
async function loadSearchIndex() {
    try {
        const response = await fetch(`${window.BASE_URL || ''}/search-index.json`);
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
    const tokens = tokenizeQuery(query);
    if (tokens.length === 0) {
        return [];
    }

    const results = [];

    searchIndex.forEach(entry => {
        let score = 0;
        let matchedTokens = 0;

        const name = entry.name.toLowerCase();
        const description = entry.description.toLowerCase();
        const tags = entry.tags ? entry.tags.map(tag => tag.toLowerCase()) : [];
        const category = entry.category ? entry.category.toLowerCase() : '';
        const type = entry.type ? entry.type.toLowerCase() : '';

        tokens.forEach(token => {
            let tokenScore = 0;

            if (name === token) {
                tokenScore += 90;
            } else if (name.startsWith(token)) {
                tokenScore += 60;
            } else if (name.includes(token)) {
                tokenScore += 40;
            }

            if (tokenMatchesText(token, description)) {
                tokenScore += 20;
            }

            if (tags.some(tag => tag === token)) {
                tokenScore += 30;
            } else if (tags.some(tag => tag.startsWith(token))) {
                tokenScore += 15;
            } else if (tags.some(tag => tag.includes(token))) {
                tokenScore += 10;
            }

            if (tokenMatchesText(token, category)) {
                tokenScore += 10;
            }

            if (tokenMatchesText(token, type)) {
                tokenScore += 10;
            }

            if (tokenScore > 0) {
                score += tokenScore;
                matchedTokens += 1;
            }
        });

        if (name === searchTerm) {
            score += 50;
        }

        if (score > 0 && matchedTokens === tokens.length) {
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
        const html = results.map(result => {
            const categoryPath = result.is_boilerplate
                ? `${window.BASE_URL || ''}/boilerplates/${result.category}/index.html`
                : `${window.BASE_URL || ''}/categories/${result.category}.html`;
            return `
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
                    <a href="${categoryPath}" class="text-blue-600 hover:underline text-sm whitespace-nowrap">
                        View Category <i class="fas fa-arrow-right ml-1"></i>
                    </a>
                </div>
            </div>
        `;
        }).join('');

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
