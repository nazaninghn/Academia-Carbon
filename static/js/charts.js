// Chart configurations
const chartColors = {
    primary: 'rgba(102, 126, 234, 0.8)',
    secondary: 'rgba(118, 75, 162, 0.8)',
    success: 'rgba(40, 167, 69, 0.8)',
    danger: 'rgba(220, 53, 69, 0.8)',
    warning: 'rgba(255, 193, 7, 0.8)',
    info: 'rgba(23, 162, 184, 0.8)',
};

const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
        legend: {
            display: true,
            position: 'top',
            labels: {
                color: 'rgba(255, 255, 255, 0.8)',
                padding: 15,
                font: {
                    size: 13
                }
            }
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            grid: {
                color: 'rgba(255, 255, 255, 0.1)',
                drawBorder: false
            },
            ticks: {
                color: 'rgba(255, 255, 255, 0.7)'
            }
        },
        x: {
            grid: {
                color: 'rgba(255, 255, 255, 0.1)',
                drawBorder: false
            },
            ticks: {
                color: 'rgba(255, 255, 255, 0.7)'
            }
        }
    }
};

let co2Chart, ghgChart, totalChart, globalChart;

// Load global data on page load
document.addEventListener('DOMContentLoaded', function() {
    loadGlobalData();
});

// Country selector
document.getElementById('countrySelect').addEventListener('change', function() {
    const countryCode = this.value;
    if (countryCode) {
        loadCountryData(countryCode);
    } else {
        document.getElementById('countryData').style.display = 'none';
    }
});

function loadGlobalData() {
    fetch(window.location.pathname + 'api/global/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('globalChart').getContext('2d');
            
            if (globalChart) {
                globalChart.destroy();
            }
            
            globalChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.years,
                    datasets: [{
                        label: translations.globalEmissions,
                        data: data.emissions,
                        borderColor: 'rgba(74, 222, 128, 1)',
                        backgroundColor: 'rgba(74, 222, 128, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 6,
                        pointBackgroundColor: 'rgba(74, 222, 128, 1)',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointHoverRadius: 8
                    }]
                },
                options: chartOptions
            });
        })
        .catch(error => console.error('Error loading global data:', error));
}

function loadCountryData(countryCode) {
    // This function is now in dashboard.js
    // Keep this for compatibility
}
