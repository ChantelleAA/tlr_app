// Create this file: static/js/activity_tracker.js

class ActivityTracker {
    constructor() {
        this.startTime = Date.now();
        this.scrollDepth = 0;
        this.maxScrollDepth = 0;
        this.setupEventListeners();
        this.trackPageView();
    }

    setupEventListeners() {
        // Track scroll depth
        window.addEventListener('scroll', this.trackScroll.bind(this));
        
        // Track clicks on important elements
        document.addEventListener('click', this.trackClick.bind(this));
        
        // Track form submissions
        document.addEventListener('submit', this.trackFormSubmit.bind(this));
        
        // Track page unload (time spent)
        window.addEventListener('beforeunload', this.trackPageExit.bind(this));
        
        // Track search input changes (with debouncing)
        const searchInputs = document.querySelectorAll('input[type="search"], input[name*="search"], input[id*="search"]');
        searchInputs.forEach(input => {
            input.addEventListener('input', this.debounce(this.trackSearchInput.bind(this), 1000));
        });
    }

    trackScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        
        this.scrollDepth = Math.round(scrollPercent);
        this.maxScrollDepth = Math.max(this.maxScrollDepth, this.scrollDepth);
    }

    trackClick(event) {
        const target = event.target;
        let elementDescription = '';
        
        // Identify the clicked element
        if (target.tagName === 'BUTTON') {
            elementDescription = `Button: ${target.textContent.trim() || target.value || target.id}`;
        } else if (target.tagName === 'A') {
            elementDescription = `Link: ${target.textContent.trim() || target.href}`;
        } else if (target.type === 'submit') {
            elementDescription = `Submit: ${target.value || target.textContent.trim()}`;
        } else if (target.classList.contains('btn') || target.role === 'button') {
            elementDescription = `Element: ${target.textContent.trim() || target.className}`;
        }

        if (elementDescription) {
            this.sendActivity('button_click', {
                element: elementDescription,
                scroll_depth: this.maxScrollDepth
            });
        }
    }

    trackFormSubmit(event) {
        const form = event.target;
        const formData = new FormData(form);
        const formInfo = {
            form_id: form.id || form.className || 'unknown',
            form_action: form.action || window.location.href,
            field_count: formData.entries ? Array.from(formData.entries()).length : 0
        };

        this.sendActivity('form_submitted', formInfo);
    }

    trackSearchInput(event) {
        const query = event.target.value.trim();
        if (query.length > 2) {  // Only track meaningful queries
            this.sendActivity('search_input', {
                query: query,
                partial: true
            });
        }
    }

    trackPageView() {
        const pageInfo = {
            page_title: document.title,
            page_url: window.location.href,
            referrer: document.referrer,
            screen_resolution: `${screen.width}x${screen.height}`,
            viewport: `${window.innerWidth}x${window.innerHeight}`
        };

        this.sendActivity('page_view', pageInfo);
    }

    trackPageExit() {
        const timeSpent = Math.round((Date.now() - this.startTime) / 1000);
        
        this.sendActivity('session_end', {
            time_on_page: timeSpent,
            max_scroll_depth: this.maxScrollDepth
        }, true); // Sync request for page unload
    }

    sendActivity(action, data = {}, sync = false) {
        const payload = {
            action: action,
            timestamp: new Date().toISOString(),
            url: window.location.href,
            ...data
        };

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify(payload)
        };

        if (sync) {
            // Use sendBeacon for page unload
            if (navigator.sendBeacon) {
                navigator.sendBeacon('/api/activity/', JSON.stringify(payload));
            }
        } else {
            // Regular async request
            fetch('/api/activity/', options).catch(console.error);
        }
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    debounce(func, wait) {
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
}

// Initialize tracking when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.startsWith('/admin/')) {
        return; // Don't track admin pages
    }
    
    window.activityTracker = new ActivityTracker();
});

// Track AJAX requests for search and filtering
if (window.fetch) {
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        const url = args[0];
        const options = args[1] || {};
        
        // Track important AJAX calls
        if (typeof url === 'string' && 
            (url.includes('/suggest/') || url.includes('/search/') || url.includes('/filter/'))) {
            
            const startTime = Date.now();
            
            return originalFetch.apply(this, args)
                .then(response => {
                    const responseTime = Date.now() - startTime;
                    
                    if (window.activityTracker) {
                        window.activityTracker.sendActivity('ajax_request', {
                            url: url,
                            method: options.method || 'GET',
                            response_time: responseTime,
                            status: response.status
                        });
                    }
                    
                    return response;
                })
                .catch(error => {
                    if (window.activityTracker) {
                        window.activityTracker.sendActivity('ajax_error', {
                            url: url,
                            error: error.message
                        });
                    }
                    throw error;
                });
        }
        
        return originalFetch.apply(this, args);
    };
}