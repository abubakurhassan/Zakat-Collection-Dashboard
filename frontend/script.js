document.addEventListener("DOMContentLoaded", () => {

    const totalCollectionsEl = document.getElementById("totalCollections");
    const roiValueEl = document.getElementById("roiValue");
    const expensesValueEl = document.getElementById("expensesValue");
    const balanceValueEl = document.getElementById("balanceValue");
    const beneficiaryCardsEl = document.getElementById("beneficiaryCards");
    const investmentCardsEl = document.getElementById("investmentCards");
    const statusDot = document.getElementById("statusDot");
    const statusText = document.getElementById("statusText");
    const lastUpdateEl = document.getElementById("lastUpdate");

    let collectionChart = null;

    // Icons for categories
    const beneficiaryIcons = {
        "Poor and Needy": "👥",
        "Zakat Administrators": "👔",
        "New Converts": "🌟",
        "To Free Captives": "💚",
        "The Debtors": "💸",
        "In the Cause of Allah": "🕌",
        "The Wayfarer": "🧳"
    };

    const investmentIcon = "📈";

    function createParticles() {
        for (let i = 0; i < 15; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            const size = Math.random() * 4 + 2;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDuration = (Math.random() * 10 + 15) + 's';
            particle.style.animationDelay = Math.random() * 5 + 's';
            
            document.body.appendChild(particle);
        }
    }

    createParticles();

    function formatCurrency(value) {
        return Number(value).toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    function updateTimestamp() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit'
        });
        lastUpdateEl.textContent = timeStr;
    }

    function initCollectionChart() {
        const ctx = document.getElementById('collectionChart').getContext('2d');
        
        collectionChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Daily Collections',
                    data: [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgba(59, 130, 246, 0.5)',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return 'MVR ' + formatCurrency(context.parsed.y);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.5)',
                            callback: function(value) {
                                return 'MVR ' + value.toLocaleString();
                            }
                        }
                    },
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                        ticks: { color: 'rgba(255, 255, 255, 0.5)' }
                    }
                }
            }
        });
    }

    function updateCollectionChart(chartData) {
        if (!collectionChart) initCollectionChart();
        collectionChart.data.labels = chartData.labels;
        collectionChart.data.datasets[0].data = chartData.values;
        collectionChart.update();
    }

    function updateBeneficiaryCards(categories) {
        if (!categories || categories.length === 0) {
            beneficiaryCardsEl.innerHTML = '<div style="text-align: center; opacity: 0.5;">No data</div>';
            return;
        }
        
        beneficiaryCardsEl.innerHTML = categories.map(cat => {
            const icon = beneficiaryIcons[cat.name] || "📊";
            return `
                <div class="expense-card">
                    <div class="expense-icon">${icon}</div>
                    <div class="expense-name">${cat.name}</div>
                    <div class="expense-amount">
                        <span class="expense-currency">MVR</span>${formatCurrency(cat.amount)}
                    </div>
                </div>
            `;
        }).join('');
    }

    function updateInvestmentCard(investment) {
        if (!investment) {
            investmentCardsEl.innerHTML = '<div style="text-align: center; opacity: 0.5;">No data</div>';
            return;
        }
        
        investmentCardsEl.innerHTML = `
            <div class="expense-card">
                <div class="expense-icon">${investmentIcon}</div>
                <div class="expense-name">${investment.name}</div>
                <div class="expense-amount">
                    <span class="expense-currency">MVR</span>${formatCurrency(investment.amount)}
                </div>
            </div>
        `;
    }

    async function loadDashboardData() {
        try {
            totalCollectionsEl.classList.add("loading");
            roiValueEl.classList.add("loading");
            expensesValueEl.classList.add("loading");
            balanceValueEl.classList.add("loading");
            
            const API_URL = "https://supercordial-cary-peerlessly.ngrok-free.dev";
            const res = await fetch(`${API_URL}/dashboard`, {
                headers: {
                    "ngrok-skip-browser-warning": "true"
                }
            });
            
            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`);
            }

            const data = await res.json();
            
            if (data.error) throw new Error(data.error);
            
            // Update main values
            totalCollectionsEl.innerHTML = `<span class="main-currency">MVR</span>${formatCurrency(data.total_collections)}`;
            roiValueEl.innerHTML = `<span class="card-currency">MVR</span>${formatCurrency(data.roi)}`;
            expensesValueEl.innerHTML = `<span class="card-currency">MVR</span>${formatCurrency(data.total_expenses)}`;
            balanceValueEl.innerHTML = `<span class="card-currency">MVR</span>${formatCurrency(data.account_balance)}`;
            
            // Update beneficiary cards
            if (data.beneficiary_distribution) {
                updateBeneficiaryCards(data.beneficiary_distribution);
            }
            
            // Update investment card
            if (data.investments) {
                updateInvestmentCard(data.investments);
            }
            
            // Update chart
            if (data.chart) {
                updateCollectionChart(data.chart);
            }
            
            totalCollectionsEl.classList.remove("loading");
            roiValueEl.classList.remove("loading");
            expensesValueEl.classList.remove("loading");
            balanceValueEl.classList.remove("loading");
            
            statusDot.classList.remove("error");
            statusText.textContent = "Live";
            updateTimestamp();
            
        } catch (e) {
            console.error("Error loading dashboard:", e);
            
            totalCollectionsEl.innerHTML = "Error";
            roiValueEl.innerHTML = "Error";
            expensesValueEl.innerHTML = "Error";
            balanceValueEl.innerHTML = "Error";
            
            totalCollectionsEl.classList.remove("loading");
            roiValueEl.classList.remove("loading");
            expensesValueEl.classList.remove("loading");
            balanceValueEl.classList.remove("loading");
            
            statusDot.classList.add("error");
            statusText.textContent = "Offline";
            lastUpdateEl.textContent = "Error";
        }
    }

    // Initialize
    initCollectionChart();
    loadDashboardData();
    setInterval(loadDashboardData, 60000);

    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) loadDashboardData();
    });

});