/**
 * Theme Manager - Dark Mode Toggle
 * Version: 1.0
 */

(function() {
    'use strict';

    // Get saved theme or default to 'light'
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    // Apply theme immediately to prevent flash
    document.documentElement.setAttribute('data-theme', savedTheme);

    // Wait for DOM
    document.addEventListener('DOMContentLoaded', function() {
        initThemeToggle();
    });

    function initThemeToggle() {
        // Find all theme toggles on page
        const toggles = document.querySelectorAll('.theme-toggle, [data-theme-toggle]');
        
        toggles.forEach(toggle => {
            toggle.addEventListener('click', toggleTheme);
        });

        // Update toggle states
        updateToggles();
    }

    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Apply theme
        document.documentElement.setAttribute('data-theme', newTheme);
        
        // Save to localStorage
        localStorage.setItem('theme', newTheme);
        
        // Update all toggles
        updateToggles();

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('themeChange', { detail: { theme: newTheme } }));
    }

    function updateToggles() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const toggles = document.querySelectorAll('.theme-toggle, [data-theme-toggle]');
        
        toggles.forEach(toggle => {
            toggle.setAttribute('aria-checked', isDark);
            toggle.title = isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode';
        });
    }

    // Export for global use
    window.ThemeManager = {
        toggle: toggleTheme,
        setTheme: function(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            updateToggles();
        },
        getTheme: function() {
            return document.documentElement.getAttribute('data-theme');
        }
    };
})();
