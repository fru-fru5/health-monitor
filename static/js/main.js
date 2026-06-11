document.addEventListener('DOMContentLoaded', function () {

    // Close sidebar on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && document.body.classList.contains('sidebar-open')) {
            document.body.classList.remove('sidebar-open');
        }
    });

    // Sidebar toggle (mobile)
    var toggle   = document.querySelector('.sidebar-toggle');
    var overlay  = document.querySelector('.sidebar-overlay');

    function openSidebar() {
        document.body.classList.add('sidebar-open');
    }
    function closeSidebar() {
        document.body.classList.remove('sidebar-open');
    }

    if (toggle) toggle.addEventListener('click', function () {
        document.body.classList.contains('sidebar-open') ? closeSidebar() : openSidebar();
    });
    if (overlay) overlay.addEventListener('click', closeSidebar);

    document.querySelectorAll('.nav-link').forEach(function (link) {
        link.addEventListener('click', closeSidebar);
    });

    // Auto-dismiss flash messages after 4 seconds
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity .4s';
            alert.style.opacity = '0';
            setTimeout(function () { alert.remove(); }, 400);
        }, 4000);
    });

});
