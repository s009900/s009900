// Only run this script on GitHub Pages
if (window.location.hostname === 's009900.github.io') {
    document.addEventListener('DOMContentLoaded', function() {
        // Find the details element and remove the 'open' attribute
        const details = document.querySelector('details');
        if (details) {
            details.removeAttribute('open');
        }
    });
}
