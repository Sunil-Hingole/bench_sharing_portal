document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap dropdowns
    var dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(function(dropdown) {
        new bootstrap.Dropdown(dropdown);
    });
});
