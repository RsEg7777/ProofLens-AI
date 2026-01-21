/**
 * ULTIMATE INTERACTIONS - ProofLens AI
 * Universal JavaScript for maximum visual experience
 */

(function() {
    'use strict';

    // ============================================
    // INITIALIZATION
    // ============================================
    
    function initializeUltimateExperience() {
        initCustomCursor();
        initNavbar();
        initSmoothScroll();
        initParallax();
        initAOS();
        initNumberCounters();
        initFormAnimations();
        initTooltips();
        initMagneticButtons();
        initPageTransitions();
    }

    // ============================================
    // CUSTOM CURSOR
    // ============================================
    
    function initCustomCursor() {
        const cursor = document.querySelector('.ultimate-cursor');
        const cursorFollower = document.querySelector('.ultimate-cursor-follower');
        
        if (!cursor || !cursorFollower) return;

        document.addEventListener('mousemove', (e) => {
            cursor.style.transform = `translate(${e.clientX - 10}px, ${e.clientY - 10}px)`;
            setTimeout(() => {
                cursorFollower.style.transform = `translate(${e.clientX - 20}px, ${e.clientY - 20}px)`;
            }, 100);
        });

        // Magnetic effect on interactive elements
        const interactiveElements = document.querySelectorAll(
            '.ultimate-btn, a, button, input, textarea, .ultimate-card'
        );

        interactiveElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursor.style.transform += ' scale(1.5)';
                cursorFollower.style.transform += ' scale(1.5)';
            });

            el.addEventListener('mouseleave', () => {
                cursor.style.transform = cursor.style.transform.replace(' scale(1.5)', '');
                cursorFollower.style.transform = cursorFollower.style.transform.replace(' scale(1.5)', '');
            });
        });
    }

    // ============================================
    // NAVBAR
    // ============================================
    
    function initNavbar() {
        const nav = document.querySelector('.ultimate-nav');
        if (!nav) return;

        let lastScroll = 0;

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;

            if (currentScroll > 100) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }

            // Hide on scroll down, show on scroll up
            if (currentScroll > lastScroll && currentScroll > 500) {
                nav.style.transform = 'translateY(-100%)';
            } else {
                nav.style.transform = 'translateY(0)';
            }

            lastScroll = currentScroll;
        });
    }

    // ============================================
    // SMOOTH SCROLL
    // ============================================
    
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                
                if (target) {
                    const navHeight = document.querySelector('.ultimate-nav')?.offsetHeight || 0;
                    const targetPosition = target.offsetTop - navHeight;

                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // ============================================
    // PARALLAX EFFECTS
    // ============================================
    
    function initParallax() {
        const parallaxElements = document.querySelectorAll('.float-element, .gradient-orb');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            
            parallaxElements.forEach((el, index) => {
                const speed = (index + 1) * 0.05;
                el.style.transform += ` translateY(${scrolled * speed}px)`;
            });
        });
    }

    // ============================================
    // AOS (Animate On Scroll) INIT
    // ============================================
    
    function initAOS() {
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 1000,
                once: true,
                offset: 100,
                easing: 'ease-out-cubic'
            });
        }
    }

    // ============================================
    // NUMBER COUNTERS
    // ============================================
    
    function initNumberCounters() {
        const animateNumber = (element, target, suffix = '') => {
            const duration = 2000;
            const start = 0;
            const increment = target / (duration / 16);
            let current = start;

            const timer = setInterval(() => {
                current += increment;
                
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                
                if (suffix.includes('%')) {
                    element.textContent = current.toFixed(1) + '%';
                } else if (suffix.includes('M+')) {
                    element.textContent = (current / 1000000).toFixed(1) + 'M+';
                } else if (suffix.includes('K+')) {
                    element.textContent = (current / 1000).toFixed(0) + 'K+';
                } else {
                    element.textContent = Math.floor(current) + suffix;
                }
            }, 16);
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const statNumbers = entry.target.querySelectorAll('[data-count]');
                    
                    statNumbers.forEach(stat => {
                        const target = parseFloat(stat.getAttribute('data-count'));
                        const suffix = stat.getAttribute('data-suffix') || '';
                        
                        if (suffix.includes('M+')) {
                            animateNumber(stat, target * 1000000, suffix);
                        } else if (suffix.includes('K+')) {
                            animateNumber(stat, target * 1000, suffix);
                        } else {
                            animateNumber(stat, target, suffix);
                        }
                    });
                    
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('.stats, .stats-grid, .ultimate-card').forEach(el => {
            observer.observe(el);
        });
    }

    // ============================================
    // FORM ANIMATIONS
    // ============================================
    
    function initFormAnimations() {
        // Floating labels
        const inputs = document.querySelectorAll('.ultimate-input, input, textarea');
        
        inputs.forEach(input => {
            // Add focus effects
            input.addEventListener('focus', function() {
                this.parentElement?.classList.add('focused');
            });

            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.parentElement?.classList.remove('focused');
                }
            });

            // Character counter for textareas
            if (input.tagName === 'TEXTAREA' && input.hasAttribute('data-max-length')) {
                const maxLength = parseInt(input.getAttribute('data-max-length'));
                const counter = document.createElement('div');
                counter.className = 'char-counter';
                counter.style.cssText = 'text-align: right; font-size: 12px; color: var(--text-muted); margin-top: 4px;';
                input.parentElement.appendChild(counter);

                input.addEventListener('input', function() {
                    const length = this.value.length;
                    counter.textContent = `${length} / ${maxLength}`;
                    
                    if (length > maxLength) {
                        counter.style.color = 'var(--error)';
                    } else {
                        counter.style.color = 'var(--text-muted)';
                    }
                });
            }
        });

        // File input enhancements
        const fileInputs = document.querySelectorAll('input[type="file"]');
        
        fileInputs.forEach(input => {
            const wrapper = document.createElement('div');
            wrapper.className = 'ultimate-file-input';
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);

            const label = document.createElement('label');
            label.className = 'ultimate-btn ultimate-btn-secondary';
            label.innerHTML = '<i class="fas fa-upload"></i> Choose File';
            label.style.cursor = 'pointer';
            wrapper.appendChild(label);

            const fileName = document.createElement('span');
            fileName.className = 'file-name';
            fileName.style.marginLeft = '16px';
            fileName.style.color = 'var(--text-secondary)';
            wrapper.appendChild(fileName);

            input.style.display = 'none';
            
            label.addEventListener('click', () => input.click());

            input.addEventListener('change', function() {
                if (this.files.length > 0) {
                    fileName.textContent = this.files[0].name;
                } else {
                    fileName.textContent = '';
                }
            });
        });
    }

    // ============================================
    // TOOLTIPS
    // ============================================
    
    function initTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        
        tooltipElements.forEach(el => {
            el.classList.add('ultimate-tooltip');
        });
    }

    // ============================================
    // MAGNETIC BUTTONS
    // ============================================
    
    function initMagneticButtons() {
        const buttons = document.querySelectorAll('.ultimate-btn, .magnetic');
        
        buttons.forEach(button => {
            button.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                
                this.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
            });

            button.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });
    }

    // ============================================
    // PAGE TRANSITIONS
    // ============================================
    
    function initPageTransitions() {
        // Fade in on page load
        document.body.style.opacity = '0';
        
        window.addEventListener('load', () => {
            document.body.style.transition = 'opacity 0.5s ease';
            document.body.style.opacity = '1';
        });

        // Add loading indicator for navigation
        const links = document.querySelectorAll('a:not([href^="#"]):not([target="_blank"])');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                if (this.href && !this.href.startsWith('javascript:')) {
                    document.body.style.opacity = '0';
                }
            });
        });
    }

    // ============================================
    // UTILITY FUNCTIONS
    // ============================================
    
    // Show/Hide Loading
    window.showUltimateLoading = function(text = 'Loading...') {
        const loader = document.createElement('div');
        loader.id = 'ultimate-loader';
        loader.className = 'ultimate-modal active';
        loader.innerHTML = `
            <div class="ultimate-modal-content" style="text-align: center;">
                <div class="ultimate-loader" style="margin: 0 auto 20px;"></div>
                <p style="color: var(--text-primary); font-size: 18px;">${text}</p>
            </div>
        `;
        document.body.appendChild(loader);
    };

    window.hideUltimateLoading = function() {
        const loader = document.getElementById('ultimate-loader');
        if (loader) {
            loader.remove();
        }
    };

    // Show Toast Notification
    window.showUltimateToast = function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `ultimate-toast ultimate-toast-${type}`;
        toast.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            padding: 20px 30px;
            background: var(--dark-2);
            border: 1px solid var(--border-medium);
            border-radius: var(--radius-lg);
            color: var(--text-primary);
            box-shadow: var(--shadow-xl);
            z-index: 10000;
            animation: slideInRight 0.5s ease-out;
            max-width: 400px;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.5s ease-out';
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    };

    // Copy to Clipboard
    window.ultimateCopyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(() => {
            showUltimateToast('Copied to clipboard!', 'success');
        }).catch(() => {
            showUltimateToast('Failed to copy', 'error');
        });
    };

    // ============================================
    // EXECUTE ON DOM READY
    // ============================================
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeUltimateExperience);
    } else {
        initializeUltimateExperience();
    }

})();

// ============================================
// ADDITIONAL ANIMATIONS
// ============================================

// Slide in animations
const slideInKeyframes = `
    @keyframes slideInRight {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;

const style = document.createElement('style');
style.textContent = slideInKeyframes;
document.head.appendChild(style);
