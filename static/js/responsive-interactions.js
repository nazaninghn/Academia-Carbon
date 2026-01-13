/* =========================================================
   RESPONSIVE INTERACTIONS
   Academia Carbon - Mobile & Touch Optimizations
========================================================= */

(function() {
    'use strict';

    // =========================================================
    // MOBILE DETECTION & SETUP
    // =========================================================
    
    const isMobile = window.innerWidth <= 768;
    const isTablet = window.innerWidth > 768 && window.innerWidth <= 992;
    const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    // Add device classes to body
    document.body.classList.add(
        isMobile ? 'is-mobile' : 'is-desktop',
        isTablet ? 'is-tablet' : '',
        isTouch ? 'is-touch' : 'is-mouse'
    );

    // =========================================================
    // RESPONSIVE NAVIGATION
    // =========================================================
    
    function initResponsiveNavigation() {
        const navToggle = document.querySelector('.nav-toggle-responsive');
        const navLinks = document.querySelector('.nav-links-responsive');
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
        
        // Handle navigation toggle
        if (navToggle && navLinks) {
            navToggle.addEventListener('click', function() {
                navLinks.classList.toggle('active');
                this.setAttribute('aria-expanded', 
                    navLinks.classList.contains('active') ? 'true' : 'false'
                );
            });
        }
        
        // Handle mobile menu button
        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                toggleMobileMenu();
            });
        }
        
        // Handle floating mobile menu toggle
        if (mobileMenuToggle) {
            mobileMenuToggle.addEventListener('click', function(e) {
                e.stopPropagation();
                toggleMobileMenu();
            });
        }
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (navLinks && navLinks.classList.contains('active') && 
                !e.target.closest('.nav-responsive')) {
                navLinks.classList.remove('active');
                if (navToggle) {
                    navToggle.setAttribute('aria-expanded', 'false');
                }
            }
        });
        
        // Close mobile menu on window resize
        window.addEventListener('resize', function() {
            if (window.innerWidth > 992) {
                if (navLinks) navLinks.classList.remove('active');
                if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
                closeMobileMenu();
            }
        });
    }

    // =========================================================
    // MOBILE MENU FUNCTIONALITY
    // =========================================================
    
    function toggleMobileMenu() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        const body = document.body;
        
        if (sidebar) {
            const isActive = sidebar.classList.contains('active');
            
            if (isActive) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        }
    }
    
    function openMobileMenu() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        const body = document.body;
        
        if (sidebar) {
            sidebar.classList.add('active');
            if (overlay) overlay.classList.add('active');
            body.classList.add('sidebar-open');
            
            // Update button icons
            updateMenuButtonIcons(true);
            
            // Prevent body scroll
            body.style.overflow = 'hidden';
        }
    }
    
    function closeMobileMenu() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        const body = document.body;
        
        if (sidebar) {
            sidebar.classList.remove('active');
            if (overlay) overlay.classList.remove('active');
            body.classList.remove('sidebar-open');
            
            // Update button icons
            updateMenuButtonIcons(false);
            
            // Restore body scroll
            body.style.overflow = '';
        }
    }
    
    function updateMenuButtonIcons(isOpen) {
        const menuBtns = document.querySelectorAll('.mobile-menu-btn, .mobile-menu-toggle');
        
        menuBtns.forEach(btn => {
            const icon = btn.querySelector('i');
            if (icon) {
                if (isOpen) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                } else {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }

    // =========================================================
    // RESPONSIVE TABLES
    // =========================================================
    
    function initResponsiveTables() {
        const tables = document.querySelectorAll('.table-responsive, .sources-table, .summary-table');
        
        tables.forEach(table => {
            if (!table.closest('.table-responsive-wrapper')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-responsive-wrapper';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
        });
    }

    // =========================================================
    // RESPONSIVE FORMS
    // =========================================================
    
    function initResponsiveForms() {
        // Handle form validation on mobile
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            
            inputs.forEach(input => {
                // Prevent zoom on iOS
                if (isTouch && input.type !== 'file') {
                    if (parseFloat(getComputedStyle(input).fontSize) < 16) {
                        input.style.fontSize = '16px';
                    }
                }
                
                // Add touch-friendly focus handling
                input.addEventListener('focus', function() {
                    if (isMobile) {
                        this.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'center' 
                        });
                    }
                });
            });
        });
        
        // Handle form rows on mobile
        const formRows = document.querySelectorAll('.form-row, .form-row-responsive');
        
        formRows.forEach(row => {
            if (isMobile) {
                row.style.gridTemplateColumns = '1fr';
            }
        });
    }

    // =========================================================
    // RESPONSIVE MODALS
    // =========================================================
    
    function initResponsiveModals() {
        const modals = document.querySelectorAll('.modal-responsive, .dashboard-modal');
        
        modals.forEach(modal => {
            // Close modal on overlay click
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    closeModal(modal);
                }
            });
            
            // Handle escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && modal.style.display !== 'none') {
                    closeModal(modal);
                }
            });
            
            // Prevent body scroll when modal is open
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.attributeName === 'style') {
                        const isVisible = modal.style.display !== 'none' && 
                                        modal.style.display !== '';
                        
                        if (isVisible) {
                            document.body.style.overflow = 'hidden';
                        } else {
                            document.body.style.overflow = '';
                        }
                    }
                });
            });
            
            observer.observe(modal, { attributes: true });
        });
    }
    
    function closeModal(modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }

    // =========================================================
    // RESPONSIVE CHARTS
    // =========================================================
    
    function initResponsiveCharts() {
        // Handle Chart.js responsive behavior
        if (window.Chart) {
            Chart.defaults.responsive = true;
            Chart.defaults.maintainAspectRatio = false;
            
            // Update chart options for mobile
            if (isMobile) {
                Chart.defaults.plugins.legend.labels.font = { size: 10 };
                Chart.defaults.plugins.tooltip.titleFont = { size: 12 };
                Chart.defaults.plugins.tooltip.bodyFont = { size: 11 };
            }
        }
        
        // Resize charts on window resize
        window.addEventListener('resize', debounce(function() {
            if (window.Chart) {
                Chart.helpers.each(Chart.instances, function(instance) {
                    instance.resize();
                });
            }
        }, 250));
    }

    // =========================================================
    // RESPONSIVE DROPDOWNS
    // =========================================================
    
    function initResponsiveDropdowns() {
        const dropdowns = document.querySelectorAll('.scope-dropdown');
        
        dropdowns.forEach(dropdown => {
            // Close dropdown when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.scope-dropdown-btn') && 
                    !e.target.closest('.scope-dropdown')) {
                    dropdown.style.display = 'none';
                }
            });
            
            // Handle touch events
            if (isTouch) {
                dropdown.addEventListener('touchstart', function(e) {
                    e.stopPropagation();
                });
            }
        });
    }

    // =========================================================
    // RESPONSIVE TABS
    // =========================================================
    
    function initResponsiveTabs() {
        const tabContainers = document.querySelectorAll('.scope-tabs');
        
        tabContainers.forEach(container => {
            const tabs = container.querySelectorAll('.scope-tab');
            
            // Add swipe support for mobile
            if (isTouch && isMobile) {
                let startX = 0;
                let currentTab = 0;
                
                container.addEventListener('touchstart', function(e) {
                    startX = e.touches[0].clientX;
                });
                
                container.addEventListener('touchend', function(e) {
                    const endX = e.changedTouches[0].clientX;
                    const diff = startX - endX;
                    
                    if (Math.abs(diff) > 50) { // Minimum swipe distance
                        if (diff > 0 && currentTab < tabs.length - 1) {
                            // Swipe left - next tab
                            tabs[currentTab + 1].click();
                            currentTab++;
                        } else if (diff < 0 && currentTab > 0) {
                            // Swipe right - previous tab
                            tabs[currentTab - 1].click();
                            currentTab--;
                        }
                    }
                });
                
                // Track active tab
                tabs.forEach((tab, index) => {
                    tab.addEventListener('click', function() {
                        currentTab = index;
                    });
                });
            }
        });
    }

    // =========================================================
    // RESPONSIVE TOOLTIPS
    // =========================================================
    
    function initResponsiveTooltips() {
        // Convert hover tooltips to click on touch devices
        if (isTouch) {
            const tooltipElements = document.querySelectorAll('[title], [data-tooltip]');
            
            tooltipElements.forEach(element => {
                const tooltipText = element.getAttribute('title') || 
                                 element.getAttribute('data-tooltip');
                
                if (tooltipText) {
                    element.removeAttribute('title'); // Prevent default tooltip
                    
                    element.addEventListener('click', function(e) {
                        e.preventDefault();
                        showMobileTooltip(this, tooltipText);
                    });
                }
            });
        }
    }
    
    function showMobileTooltip(element, text) {
        // Remove existing tooltips
        const existingTooltips = document.querySelectorAll('.mobile-tooltip');
        existingTooltips.forEach(tooltip => tooltip.remove());
        
        // Create new tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'mobile-tooltip';
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 10000;
            max-width: 200px;
            word-wrap: break-word;
        `;
        
        document.body.appendChild(tooltip);
        
        // Position tooltip
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.bottom + 5) + 'px';
        
        // Remove tooltip after 3 seconds
        setTimeout(() => {
            tooltip.remove();
        }, 3000);
    }

    // =========================================================
    // RESPONSIVE SCROLL HANDLING
    // =========================================================
    
    function initResponsiveScrolling() {
        // Smooth scrolling for anchor links
        const anchorLinks = document.querySelectorAll('a[href^="#"]');
        
        anchorLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    e.preventDefault();
                    
                    const offset = isMobile ? 80 : 100; // Account for fixed headers
                    const targetPosition = targetElement.offsetTop - offset;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                    
                    // Close mobile menu if open
                    closeMobileMenu();
                }
            });
        });
        
        // Handle scroll-based header changes
        let lastScrollTop = 0;
        const header = document.querySelector('.header, .top-navbar');
        
        if (header && isMobile) {
            window.addEventListener('scroll', debounce(function() {
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                
                if (scrollTop > lastScrollTop && scrollTop > 100) {
                    // Scrolling down
                    header.style.transform = 'translateY(-100%)';
                } else {
                    // Scrolling up
                    header.style.transform = 'translateY(0)';
                }
                
                lastScrollTop = scrollTop;
            }, 10));
        }
    }

    // =========================================================
    // RESPONSIVE PERFORMANCE OPTIMIZATIONS
    // =========================================================
    
    function initPerformanceOptimizations() {
        // Lazy load images
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver(function(entries) {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => imageObserver.observe(img));
        }
        
        // Reduce animations on low-end devices
        if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
            document.body.classList.add('reduce-animations');
        }
        
        // Optimize touch events
        if (isTouch) {
            // Use passive listeners for better scroll performance
            const passiveEvents = ['touchstart', 'touchmove', 'wheel'];
            
            passiveEvents.forEach(eventType => {
                document.addEventListener(eventType, function() {}, { passive: true });
            });
        }
    }

    // =========================================================
    // UTILITY FUNCTIONS
    // =========================================================
    
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
    
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // =========================================================
    // RESPONSIVE ACCESSIBILITY
    // =========================================================
    
    function initResponsiveAccessibility() {
        // Add skip links for mobile
        if (isMobile) {
            const skipLink = document.createElement('a');
            skipLink.href = '#main-content';
            skipLink.textContent = 'Skip to main content';
            skipLink.className = 'skip-link';
            skipLink.style.cssText = `
                position: absolute;
                top: -40px;
                left: 6px;
                background: #000;
                color: white;
                padding: 8px;
                text-decoration: none;
                z-index: 10000;
                border-radius: 4px;
            `;
            
            skipLink.addEventListener('focus', function() {
                this.style.top = '6px';
            });
            
            skipLink.addEventListener('blur', function() {
                this.style.top = '-40px';
            });
            
            document.body.insertBefore(skipLink, document.body.firstChild);
        }
        
        // Improve focus management
        const focusableElements = document.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        focusableElements.forEach(element => {
            element.addEventListener('focus', function() {
                this.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'nearest' 
                });
            });
        });
    }

    // =========================================================
    // INITIALIZATION
    // =========================================================
    
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }
        
        // Initialize all responsive features
        initResponsiveNavigation();
        initResponsiveTables();
        initResponsiveForms();
        initResponsiveModals();
        initResponsiveCharts();
        initResponsiveDropdowns();
        initResponsiveTabs();
        initResponsiveTooltips();
        initResponsiveScrolling();
        initPerformanceOptimizations();
        initResponsiveAccessibility();
        
        // Handle window resize
        window.addEventListener('resize', debounce(function() {
            const newIsMobile = window.innerWidth <= 768;
            const newIsTablet = window.innerWidth > 768 && window.innerWidth <= 992;
            
            // Update body classes
            document.body.classList.toggle('is-mobile', newIsMobile);
            document.body.classList.toggle('is-desktop', !newIsMobile);
            document.body.classList.toggle('is-tablet', newIsTablet);
            
            // Re-initialize components that need it
            if (newIsMobile !== isMobile) {
                initResponsiveForms();
                initResponsiveTables();
            }
        }, 250));
        
        console.log('Responsive interactions initialized');
    }
    
    // Auto-initialize
    init();
    
    // Expose global functions
    window.ResponsiveUtils = {
        toggleMobileMenu,
        openMobileMenu,
        closeMobileMenu,
        isMobile: () => window.innerWidth <= 768,
        isTablet: () => window.innerWidth > 768 && window.innerWidth <= 992,
        isTouch: () => isTouch
    };

})();