class FinancialDashboard {
  constructor() {
    this.categoriesChart = null;
    this.timelineChart = null;
    this.init();
  }

  init() {
    this.loadChartData();
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Atualizar gráficos quando o filtro mudar
    const dateFilter = document.getElementById('date_filter');
    if (dateFilter) {
      dateFilter.addEventListener('change', () => {
        this.loadChartData();
      });
    }
  }

  async loadChartData() {
    try {
      const dateFilter = document.getElementById('date_filter')?.value || 'month';
      const response = await fetch(`/api/chart-data/?date_filter=${dateFilter}`);
      const data = await response.json();

      this.renderCategoriesChart(data.categories);
      this.renderTimelineChart(data.timeline);
    } catch (error) {
      console.error('Erro ao carregar dados do gráfico:', error);
    }
  }

  renderCategoriesChart(data) {
    const ctx = document.getElementById('categoriesChart').getContext('2d');

    if (this.categoriesChart) {
      this.categoriesChart.destroy();
    }

    const backgroundColors = [
      'rgba(40, 167, 69, 0.8)',   // Verde para receita
      'rgba(220, 53, 69, 0.8)',   // Vermelho para despesa
      'rgba(23, 162, 184, 0.8)'   // Azul para investimento
    ];

    const borderColors = [
      'rgba(40, 167, 69, 1)',
      'rgba(220, 53, 69, 1)',
      'rgba(23, 162, 184, 1)'
    ];

    this.categoriesChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: data.labels,
        datasets: [{
          data: data.data,
          backgroundColor: backgroundColors,
          borderColor: borderColors,
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const label = context.label || '';
                const value = context.parsed;
                return `${label}: R$ ${value.toFixed(2)}`;
              }
            }
          }
        }
      }
    });
  }

  renderTimelineChart(data) {
    const ctx = document.getElementById('timelineChart').getContext('2d');

    if (this.timelineChart) {
      this.timelineChart.destroy();
    }

    this.timelineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: 'Receitas',
            data: data.receitas,
            borderColor: 'rgba(40, 167, 69, 1)',
            backgroundColor: 'rgba(40, 167, 69, 0.1)',
            tension: 0.4,
            fill: true
          },
          {
            label: 'Despesas',
            data: data.despesas,
            borderColor: 'rgba(220, 53, 69, 1)',
            backgroundColor: 'rgba(220, 53, 69, 0.1)',
            tension: 0.4,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                return `${context.dataset.label}: R$ ${context.parsed.y.toFixed(2)}`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value) {
                return 'R$ ' + value.toFixed(2);
              }
            }
          }
        }
      }
    });
  }
}

// Inicializar dashboard quando a página carregar
document.addEventListener('DOMContentLoaded', function () {
  new FinancialDashboard();
});
