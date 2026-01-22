/**
 * ProofLens AI - Theme Toggle System
 * Handles light/dark/snow theme switching with localStorage persistence
 * Includes snow particle effects for the Snow theme
 */

class ThemeManager {
    constructor() {
        this.themeKey = 'prooflens-theme';
        this.themes = ['light', 'dark', 'snow'];
        this.themeIcons = {
            'light': '☀️',
            'dark': '🌙',
            'snow': '❄️'
        };
        this.themeNames = {
            'light': 'Light',
            'dark': 'Dark',
            'snow': 'Snow'
        };
        this.currentTheme = this.getStoredTheme() || 'dark';
        this.snowflakeCount = 50;
        this.snowflakes = [];
        this.init();
    }

    init() {
        // Create snow effect containers
        this.createSnowEffects();
        
        // Apply stored theme on load
        this.applyTheme(this.currentTheme);
        
        // Create theme toggle button if it doesn't exist
        this.createToggleButton();
        
        // Listen for system theme changes
        this.watchSystemTheme();
        
        // Initialize theme menu items
        this.initThemeMenuItems();
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
        if (!this.themes.includes(theme)) {
            theme = 'dark';
        }
        
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        this.setStoredTheme(theme);
        this.updateToggleButton();
        this.updateThemeMenuItems();
        
        // Handle snow effects
        if (theme === 'snow') {
            this.startSnowfall();
        } else {
            this.stopSnowfall();
        }
        
        // Dispatch custom event for other components to listen
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    toggleTheme() {
        const currentIndex = this.themes.indexOf(this.currentTheme);
        const nextIndex = (currentIndex + 1) % this.themes.length;
        this.applyTheme(this.themes[nextIndex]);
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
            icon.textContent = this.themeIcons[this.currentTheme] || '🌙';
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

    // Initialize theme menu item click handlers
    initThemeMenuItems() {
        document.addEventListener('click', (e) => {
            const themeOption = e.target.closest('[data-theme-option]');
            if (themeOption) {
                e.preventDefault();
                const theme = themeOption.getAttribute('data-theme-option');
                if (theme && this.themes.includes(theme)) {
                    this.applyTheme(theme);
                }
            }
        });
    }

    // Update theme menu items to show active state
    updateThemeMenuItems() {
        const themeOptions = document.querySelectorAll('[data-theme-option]');
        themeOptions.forEach(option => {
            const theme = option.getAttribute('data-theme-option');
            if (theme === this.currentTheme) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    }

    // Create snow effect DOM elements
    createSnowEffects() {
        // Create ice particles background
        if (!document.querySelector('.ice-particles')) {
            const iceParticles = document.createElement('div');
            iceParticles.className = 'ice-particles';
            document.body.appendChild(iceParticles);
        }

        // Create snowfall container
        if (!document.querySelector('.snowfall-container')) {
            const snowContainer = document.createElement('div');
            snowContainer.className = 'snowfall-container';
            snowContainer.id = 'snowfall-container';
            document.body.appendChild(snowContainer);
        }
    }

    // Start snowfall animation
    startSnowfall() {
        const container = document.getElementById('snowfall-container');
        if (!container) return;

        // Clear existing snowflakes
        container.innerHTML = '';
        this.snowflakes = [];

        // Create snowflakes
        for (let i = 0; i < this.snowflakeCount; i++) {
            this.createSnowflake(container, i);
        }
    }

    // Create individual snowflake
    createSnowflake(container, index) {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        
        // Random positioning and animation
        const startLeft = Math.random() * 100;
        const animationDuration = 8 + Math.random() * 12; // 8-20 seconds
        const animationDelay = Math.random() * 10; // 0-10 seconds delay
        
        snowflake.style.cssText = `
            left: ${startLeft}%;
            animation-duration: ${animationDuration}s;
            animation-delay: -${animationDelay}s;
        `;
        
        container.appendChild(snowflake);
        this.snowflakes.push(snowflake);
    }

    // Stop snowfall animation
    stopSnowfall() {
        const container = document.getElementById('snowfall-container');
        if (container) {
            container.innerHTML = '';
        }
        this.snowflakes = [];
    }

    // Public method to get current theme
    getCurrentTheme() {
        return this.currentTheme;
    }

    // Public method to get all available themes
    getAvailableThemes() {
        return this.themes.map(theme => ({
            id: theme,
            name: this.themeNames[theme],
            icon: this.themeIcons[theme]
        }));
    }

    // Public method to set theme programmatically
    setTheme(theme) {
        if (this.themes.includes(theme)) {
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
