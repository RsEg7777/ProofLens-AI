/**
 * ProofLens AI - Theme Toggle System
 * Handles dark/light theme switching with localStorage persistence
 */

class ThemeManager {
    constructor() {
        this.themeKey = 'prooflens-theme';
        this.currentTheme = this.getStoredTheme() || 'light';
        this.init();
    }

    init() {
        // Apply stored theme on load
        this.applyTheme(this.currentTheme);
        
        // Create theme toggle button if it doesn't exist
        this.createToggleButton();
        
        // Listen for system theme changes
        this.watchSystemTheme();
    }

    getStoredTheme() {
        try {
            return localStorage.getItem(this.themeKey);
        } catch (e) {
            console.warn('localStorage not available:', e);
            return null;
        }
    }

    setStoredTheme(theme) {
        try {
            localStorage.setItem(this.themeKey, theme);
        } catch (e) {
            console.warn('localStorage not available:', e);
        }
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        this.setStoredTheme(theme);
        this.updateToggleButton();
        
        // Dispatch custom event for other components to listen
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }

    createToggleButton() {
        // Check if button already exists
        if (document.querySelector('.theme-toggle')) {
            this.toggleButton = document.querySelector('.theme-toggle');
            this.toggleButton.addEventListener('click', () => this.toggleTheme());
            this.updateToggleButton();
            return;
        }

        // Create toggle button
        this.toggleButton = document.createElement('button');
        this.toggleButton.className = 'theme-toggle';
        this.toggleButton.setAttribute('aria-label', 'Toggle theme');
        this.toggleButton.innerHTML = '<span class="theme-toggle-icon">🌙</span>';
        
        // Add click event
        this.toggleButton.addEventListener('click', () => this.toggleTheme());
        
        // Add to DOM
        document.body.appendChild(this.toggleButton);
        
        // Update icon based on current theme
        this.updateToggleButton();
    }

    updateToggleButton() {
        if (!this.toggleButton) return;
        
        const icon = this.toggleButton.querySelector('.theme-toggle-icon');
        if (icon) {
            icon.textContent = this.currentTheme === 'light' ? '🌙' : '☀️';
        }
    }

    watchSystemTheme() {
        // Listen for system theme preference changes
        if (window.matchMedia) {
            const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            darkModeQuery.addEventListener('change', (e) => {
                // Only auto-switch if user hasn't manually set a preference
                if (!this.getStoredTheme()) {
                    this.applyTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }

    // Public method to get current theme
    getCurrentTheme() {
        return this.currentTheme;
    }

    // Public method to set theme programmatically
    setTheme(theme) {
        if (theme === 'light' || theme === 'dark') {
            this.applyTheme(theme);
        }
    }
}

// Initialize theme manager when DOM is ready
let themeManager;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        themeManager = new ThemeManager();
    });
} else {
    themeManager = new ThemeManager();
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}

// Make available globally
window.ThemeManager = ThemeManager;
window.themeManager = themeManager;
