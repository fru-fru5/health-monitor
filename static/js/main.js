// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity .4s';
            alert.style.opacity = '0';
            setTimeout(function () { alert.remove(); }, 400);
        }, 4000);
    });

    // Health chart (patient dashboard)
    const chartCanvas = document.getElementById('healthChart');
    if (chartCanvas && typeof Chart !== 'undefined') {
        const labels   = JSON.parse(chartCanvas.dataset.labels   || '[]');
        const bpSys    = JSON.parse(chartCanvas.dataset.bpSys    || '[]');
        const heartRate = JSON.parse(chartCanvas.dataset.heartRate || '[]');

        new Chart(chartCanvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Systolic BP',
                        data: bpSys,
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231,76,60,.08)',
                        tension: 0.3,
                        fill: true
                    },
                    {
                        label: 'Heart Rate',
                        data: heartRate,
                        borderColor: '#2e86de',
                        backgroundColor: 'rgba(46,134,222,.08)',
                        tension: 0.3,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' }
                },
                scales: {
                    y: { beginAtZero: false, grid: { color: '#eaecf0' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
});
