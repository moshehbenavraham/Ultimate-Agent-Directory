// Shared filter utilities for category and boilerplate pages

(function() {
    function normalizeQuery(query) {
        return (query || '').toLowerCase().trim();
    }

    function tokenize(query) {
        return normalizeQuery(query)
            .split(/\s+/)
            .filter(token => token.length >= 2);
    }

    function textMatchesTokens(text, tokens) {
        if (!tokens || tokens.length === 0) return true;
        const lower = (text || '').toLowerCase();
        if (!lower) return false;
        const words = lower.split(/[^a-z0-9]+/);
        return tokens.every(token => {
            if (lower.includes(token)) return true;
            return words.some(word => word.startsWith(token));
        });
    }

    function initSearchInput(inputId, onChange) {
        const searchInput = document.getElementById(inputId);
        if (!searchInput) return null;

        const debouncedSearch = window.Utils.debounce((query) => {
            onChange(query);
        }, 300);

        searchInput.addEventListener('input', function(e) {
            debouncedSearch(e.target.value || '');
        });

        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                this.value = '';
                onChange('');
            }
        });

        return searchInput;
    }

    function initSelectFilter(selectId, onChange) {
        const filter = document.getElementById(selectId);
        if (!filter) return null;
        filter.addEventListener('change', function() {
            onChange(this.value);
        });
        return filter;
    }

    function initTagButtons(selector, onToggle) {
        const tagButtons = document.querySelectorAll(selector);
        tagButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                onToggle(this.dataset.tag, this);
            });
        });
        return tagButtons;
    }

    function initSortButtons(selector, onChange) {
        const sortButtons = Array.from(document.querySelectorAll(selector));
        sortButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                sortButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                onChange(this.dataset.sort);
            });
        });
        return sortButtons;
    }

    window.FilterUtils = {
        normalizeQuery,
        tokenize,
        textMatchesTokens,
        initSearchInput,
        initSelectFilter,
        initTagButtons,
        initSortButtons
    };
})();
