// Dashboard specific functionality
let currentCountryData = null;

// Load top emitters chart on page load
document.addEventListener('DOMContentLoaded', function() {
    loadTopEmitters();
});

// Update country selector handler
document.getElementById('countrySelect').addEventListener('change', function() {
    const countryCode = this.value;
    if (countryCode) {
        loadCountryData(countryCode);
    } else {
        document.getElementById('countryData').style.display = 'none';
    }
});

// Override loadCountryData to include table
function loadCountryData(countryCode) {
    fetch(window.location.pathname + `api/country/${countryCode}/`)
        .then(response => response.json())
        .then(data => {
            currentCountryData = data;
            document.getElementById('countryData').style.display = 'block';
            
            // Update charts
            updateCO2Chart(data);
            updateGHGChart(data);
            updateTotalChart(data);
            updateDataTable(data);
        })
        .catch(error => console.error('Error loading country data:', error));
}

function updateCO2Chart(data) {
    const ctx = document.getElementById('co2Chart').getContext('2d');
    if (window.co2Chart) window.co2Chart.destroy();
    
    window.co2Chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.years,
            datasets: [{
                label: translations.co2,
                data: data.co2,
                backgroundColor: 'rgba(239, 68, 68, 0.8)',
                borderColor: 'rgba(239, 68, 68, 1)',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            ...chartOptions,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function updateGHGChart(data) {
    const ctx = document.getElementById('ghgChart').getContext('2d');
    if (window.ghgChart) window.ghgChart.destroy();
    
    const latestIndex = data.years.length - 1;
    
    window.ghgChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [translations.co2, translations.methane, translations.nitrousOxide],
            datasets: [{
                data: [
                    data.co2[latestIndex],
                    data.methane[latestIndex],
                    data.nitrous_oxide[latestIndex]
                ],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(251, 191, 36, 0.8)',
                    'rgba(59, 130, 246, 0.8)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
}

function updateTotalChart(data) {
    const ctx = document.getElementById('totalChart').getContext('2d');
    if (window.totalChart) window.totalChart.destroy();
    
    window.totalChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.years,
            datasets: [{
                label: translations.totalEmissions,
                data: data.total,
                borderColor: 'rgba(74, 222, 128, 1)',
                backgroundColor: 'rgba(74, 222, 128, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointBackgroundColor: 'rgba(74, 222, 128, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: chartOptions
    });
}

function updateDataTable(data) {
    const tbody = document.getElementById('dataTableBody');
    tbody.innerHTML = '';
    
    data.years.forEach((year, index) => {
        const trend = index > 0 ? 
            (data.total[index] > data.total[index - 1] ? 'up' : 'down') : 'neutral';
        
        const trendBadge = trend === 'up' ? 
            '<span class="badge badge-danger">↑ Increase</span>' :
            trend === 'down' ?
            '<span class="badge badge-success">↓ Decrease</span>' :
            '<span class="badge badge-warning">—</span>';
        
        const row = `
            <tr>
                <td><strong>${year}</strong></td>
                <td>${data.co2[index].toFixed(1)} Mt</td>
                <td>${data.methane[index].toFixed(1)} Mt</td>
                <td>${data.nitrous_oxide[index].toFixed(1)} Mt</td>
                <td><strong>${data.total[index].toFixed(1)} Mt</strong></td>
                <td>${trendBadge}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

function loadTopEmitters() {
    // Get all countries and their latest emissions
    fetch(window.location.pathname + 'api/top-emitters/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('topEmittersChart').getContext('2d');
            
            if (window.topEmittersChart) {
                window.topEmittersChart.destroy();
            }
            
            window.topEmittersChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.countries,
                    datasets: [{
                        label: translations.totalEmissions,
                        data: data.emissions,
                        backgroundColor: 'rgba(74, 222, 128, 0.8)',
                        borderColor: 'rgba(74, 222, 128, 1)',
                        borderWidth: 2,
                        borderRadius: 8
                    }]
                },
                options: {
                    indexAxis: 'y',
                    ...chartOptions,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading top emitters:', error));
}
