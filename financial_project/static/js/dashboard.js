class FinancialDashboard {
  constructor() {
    this.categoriesChart = null;
    this.timelineChart = null;
    this.init();
  }

  init() {
    console.log('📊 Inicializando Financial Dashboard...');
    this.loadChartData();
    this.setupEventListeners();
  }

  setupEventListeners() {
    const dateFilter = document.getElementById('date_filter');
    if (dateFilter) {
      dateFilter.addEventListener('change', () => {
        console.log('🔄 Filtro alterado, recarregando gráficos...');
        this.loadChartData();
      });
    }
  }

  async loadChartData() {
    try {
      const dateFilter = document.getElementById('date_filter')?.value || 'month';
      console.log(`📋 Carregando dados para filtro: ${dateFilter}`);

      const response = await fetch(`/api/chart-data/?date_filter=${dateFilter}`);

      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Dados recebidos:', data);

      this.renderCategoriesChart(data.categories);
      this.renderTimelineChart(data.timeline);
    } catch (error) {
      console.error('❌ Erro ao carregar dados do gráfico:', error);
      this.showError('Erro ao carregar gráficos. Verifique o console para detalhes.');
    }
  }

  renderCategoriesChart(data) {
    const ctx = document.getElementById('categoriesChart');

    if (!ctx) {
      console.error('❌ Elemento categoriesChart não encontrado');
      return;
    }

    if (this.categoriesChart) {
      this.categoriesChart.destroy();
    }

    // Verificar se há dados para mostrar
    const hasData = data.data && data.data.some(value => value > 0);

    if (!hasData) {
      this.showNoDataMessage(ctx, 'categoriesChart');
      return;
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

    try {
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
          maintainAspectRatio: false,
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
      console.log('✅ Gráfico de categorias renderizado com sucesso');
    } catch (error) {
      console.error('❌ Erro ao renderizar gráfico de categorias:', error);
    }
  }

  renderTimelineChart(data) {
    const ctx = document.getElementById('timelineChart');

    if (!ctx) {
      console.error('❌ Elemento timelineChart não encontrado');
      return;
    }

    if (this.timelineChart) {
      this.timelineChart.destroy();
    }

    // Verificar se há dados para mostrar
    const hasData = (data.receitas && data.receitas.some(value => value > 0)) ||
      (data.despesas && data.despesas.some(value => value > 0));

    if (!hasData) {
      this.showNoDataMessage(ctx, 'timelineChart');
      return;
    }

    try {
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
          maintainAspectRatio: false,
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
      console.log('✅ Gráfico de timeline renderizado com sucesso');
    } catch (error) {
      console.error('❌ Erro ao renderizar gráfico de timeline:', error);
    }
  }

  showNoDataMessage(ctx, chartType) {
    const parent = ctx.parentNode;
    parent.innerHTML = `
      <div class="alert alert-info text-center">
        <i class="fas fa-info-circle"></i>
        Nenhum dado disponível para o período selecionado.
      </div>
    `;
    console.log(`ℹ️ Sem dados para ${chartType}`);
  }

  showError(message) {
    // Você pode implementar uma notificação de erro aqui
    console.error('💥 Erro:', message);
  }
}

// Inicializar dashboard quando a página carregar
document.addEventListener('DOMContentLoaded', function () {
  console.log('🚀 DOM carregado, iniciando dashboard...');
  new FinancialDashboard();
});
