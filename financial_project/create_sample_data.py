import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_project.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import FinancialData
from django.db.models import Sum

def create_sample_data():
    # Cria ou pega o usuário demo
    try:
        user = User.objects.get(username='demo')
        print("✅ Usuário demo encontrado")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='demo', 
            email='demo@example.com', 
            password='demo123',
            first_name='Usuário',
            last_name='Demo'
        )
        print("✅ Usuário demo criado")

    # Limpa dados existentes do usuário demo
    FinancialData.objects.filter(user=user).delete()
    print("🧹 Dados antigos do usuário demo removidos")

    # Dados de exemplo mais extensos e variados
    sample_data = []
    
    # RECEITAS (20 registros)
    receitas = [
        {'description': 'Salário Empresa ABC', 'base_amount': 4500.00, 'variation': 200},
        {'description': 'Freelance Design', 'base_amount': 1200.00, 'variation': 300},
        {'description': 'Consultoria TI', 'base_amount': 2000.00, 'variation': 500},
        {'description': 'Venda Produtos', 'base_amount': 800.00, 'variation': 200},
        {'description': 'Aluguel Apartamento', 'base_amount': 1500.00, 'variation': 0},
        {'description': 'Dividendos Ações', 'base_amount': 300.00, 'variation': 100},
        {'description': 'Bônus Performance', 'base_amount': 800.00, 'variation': 200},
        {'description': 'Reembolso IR', 'base_amount': 600.00, 'variation': 150},
        {'description': 'Trabalho Extra', 'base_amount': 700.00, 'variation': 200},
        {'description': 'Royalties', 'base_amount': 400.00, 'variation': 100},
        {'description': 'Aula Particular', 'base_amount': 500.00, 'variation': 150},
        {'description': 'Venda Usados', 'base_amount': 250.00, 'variation': 100},
        {'description': 'Prêmio', 'base_amount': 300.00, 'variation': 100},
        {'description': 'Freelance Redação', 'base_amount': 600.00, 'variation': 150},
        {'description': 'Consultoria Marketing', 'base_amount': 900.00, 'variation': 200},
        {'description': 'Salário Extra', 'base_amount': 1000.00, 'variation': 200},
        {'description': 'Venda Artesanato', 'base_amount': 350.00, 'variation': 100},
        {'description': 'Serviço Manutenção', 'base_amount': 450.00, 'variation': 100},
        {'description': 'Tradução', 'base_amount': 550.00, 'variation': 150},
        {'description': 'Design Site', 'base_amount': 1200.00, 'variation': 300},
    ]
    
    # DESPESAS FIXAS (não recorrentes)
    despesas_nao_recorrentes = [
        {'description': 'Restaurante', 'base_amount': 300.00, 'variation': 100},
        {'description': 'Farmácia', 'base_amount': 120.00, 'variation': 50},
        {'description': 'Vestuário', 'base_amount': 250.00, 'variation': 100},
        {'description': 'Manutenção Carro', 'base_amount': 200.00, 'variation': 100},
        {'description': 'Presentes', 'base_amount': 150.00, 'variation': 80},
        {'description': 'Cursos', 'base_amount': 300.00, 'variation': 150},
        {'description': 'Livros', 'base_amount': 100.00, 'variation': 50},
        {'description': 'Cinema/Entretenimento', 'base_amount': 120.00, 'variation': 50},
        {'description': 'Material Escritório', 'base_amount': 70.00, 'variation': 30},
        {'description': 'Assinaturas Revistas', 'base_amount': 50.00, 'variation': 10},
        {'description': 'Doações', 'base_amount': 100.00, 'variation': 50},
        {'description': 'Viagem Fim de Semana', 'base_amount': 400.00, 'variation': 150},
        {'description': 'Manutenção Casa', 'base_amount': 180.00, 'variation': 80},
    ]
    
    # DESPESAS RECORRENTES (com dia fixo do mês)
    despesas_recorrentes = [
        {'description': 'Aluguel Residencial', 'base_amount': 1200.00, 'variation': 0, 'day': 5},
        {'description': 'Supermercado', 'base_amount': 600.00, 'variation': 150, 'day': 10},
        {'description': 'Transporte/Combustível', 'base_amount': 400.00, 'variation': 100, 'day': 15},
        {'description': 'Energia Elétrica', 'base_amount': 180.00, 'variation': 50, 'day': 12},
        {'description': 'Água e Esgoto', 'base_amount': 90.00, 'variation': 20, 'day': 8},
        {'description': 'Internet', 'base_amount': 120.00, 'variation': 10, 'day': 3},
        {'description': 'Plano de Saúde', 'base_amount': 350.00, 'variation': 0, 'day': 1},
        {'description': 'Academia', 'base_amount': 100.00, 'variation': 0, 'day': 25},
        {'description': 'Streaming (Netflix/Spotify)', 'base_amount': 60.00, 'variation': 10, 'day': 20},
        {'description': 'Telefone Celular', 'base_amount': 80.00, 'variation': 10, 'day': 18},
        {'description': 'Seguro Residencial', 'base_amount': 80.00, 'variation': 10, 'day': 7},
        {'description': 'IPTU', 'base_amount': 150.00, 'variation': 0, 'day': 28},
    ]
    
    # INVESTIMENTOS (10 registros)
    investimentos = [
        {'description': 'Ações PETR4', 'base_amount': 800.00, 'variation': 200},
        {'description': 'Tesouro Direto', 'base_amount': 500.00, 'variation': 100},
        {'description': 'Fundo Imobiliário', 'base_amount': 600.00, 'variation': 150},
        {'description': 'CDB Banco', 'base_amount': 400.00, 'variation': 100},
        {'description': 'Ações VALE3', 'base_amount': 700.00, 'variation': 150},
        {'description': 'Fundo de Ações', 'base_amount': 550.00, 'variation': 120},
        {'description': 'LCI/LCA', 'base_amount': 450.00, 'variation': 100},
        {'description': 'Ações ITUB4', 'base_amount': 650.00, 'variation': 150},
        {'description': 'Fundo Multimercado', 'base_amount': 350.00, 'variation': 80},
        {'description': 'Debêntures', 'base_amount': 480.00, 'variation': 100},
    ]

    # Adiciona receitas
    for item in receitas:
        amount = item['base_amount'] + random.uniform(-item['variation'], item['variation'])
        sample_data.append({
            'category': 'receita',
            'description': item['description'],
            'amount': round(amount, 2),
            'is_recurring': False
        })

    # Adiciona despesas não recorrentes
    for item in despesas_nao_recorrentes:
        amount = item['base_amount'] + random.uniform(-item['variation'], item['variation'])
        sample_data.append({
            'category': 'despesa',
            'description': item['description'],
            'amount': round(amount, 2),
            'is_recurring': False
        })

    # Adiciona investimentos
    for item in investimentos:
        amount = item['base_amount'] + random.uniform(-item['variation'], item['variation'])
        sample_data.append({
            'category': 'investimento',
            'description': item['description'],
            'amount': round(amount, 2),
            'is_recurring': False
        })

    # Cria os registros não recorrentes com datas distribuídas nos últimos 6 meses
    base_date = datetime.now().date()
    created_count = 0
    
    for data in sample_data:
        # Distribui as datas nos últimos 180 dias
        date_offset = timedelta(days=random.randint(0, 180))
        transaction_date = base_date - date_offset
        
        FinancialData.objects.create(
            user=user,
            category=data['category'],
            description=data['description'],
            amount=data['amount'],
            date=transaction_date,
            is_recurring=data['is_recurring']
        )
        created_count += 1

    # Cria despesas recorrentes para os últimos 6 meses
    for despesa in despesas_recorrentes:
        for month_offset in range(6):  # Últimos 6 meses
            # Calcula a data base para o mês
            month_date = base_date.replace(day=1) - timedelta(days=30 * month_offset)
            
            # Ajusta o dia do mês (garante que não passe do último dia do mês)
            try:
                transaction_date = month_date.replace(day=despesa['day'])
            except ValueError:
                # Se o dia não existe no mês (ex: 31 em fevereiro), usa o último dia do mês
                next_month = month_date.replace(day=28) + timedelta(days=4)
                transaction_date = next_month - timedelta(days=next_month.day)
            
            # Garante que a data não é no futuro
            if transaction_date <= base_date:
                amount = despesa['base_amount'] + random.uniform(-despesa['variation'], despesa['variation'])
                
                FinancialData.objects.create(
                    user=user,
                    category='despesa',
                    description=despesa['description'],
                    amount=round(amount, 2),
                    date=transaction_date,
                    is_recurring=True,
                    recurring_day=despesa['day']
                )
                created_count += 1

    # Cria algumas receitas recorrentes também
    receitas_recorrentes = [
        {'description': 'Salário Mensal', 'base_amount': 4500.00, 'day': 25},
    ]
    
    for receita in receitas_recorrentes:
        for month_offset in range(6):
            month_date = base_date.replace(day=1) - timedelta(days=30 * month_offset)
            
            try:
                transaction_date = month_date.replace(day=receita['day'])
            except ValueError:
                next_month = month_date.replace(day=28) + timedelta(days=4)
                transaction_date = next_month - timedelta(days=next_month.day)
            
            if transaction_date <= base_date:
                FinancialData.objects.create(
                    user=user,
                    category='receita',
                    description=receita['description'],
                    amount=receita['base_amount'],
                    date=transaction_date,
                    is_recurring=True,
                    recurring_day=receita['day']
                )
                created_count += 1

    print(f"✅ {created_count} registros de exemplo criados para o usuário demo")
    print("📊 Estatísticas criadas:")
    
    # Mostra estatísticas
    total_receita = FinancialData.objects.filter(user=user, category='receita').aggregate(Sum('amount'))['amount__sum'] or 0
    total_despesa = FinancialData.objects.filter(user=user, category='despesa').aggregate(Sum('amount'))['amount__sum'] or 0
    total_investimento = FinancialData.objects.filter(user=user, category='investimento').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Estatísticas de despesas recorrentes
    despesas_recorrentes_count = FinancialData.objects.filter(user=user, category='despesa', is_recurring=True).count()
    despesas_recorrentes_total = FinancialData.objects.filter(user=user, category='despesa', is_recurring=True).aggregate(Sum('amount'))['amount__sum'] or 0
    
    print(f"   💰 Receita Total: R$ {total_receita:,.2f}")
    print(f"   💸 Despesa Total: R$ {total_despesa:,.2f}")
    print(f"   📈 Investimento Total: R$ {total_investimento:,.2f}")
    print(f"   ⚖️ Saldo: R$ {(total_receita - total_despesa):,.2f}")
    print(f"   🔄 Despesas Recorrentes: {despesas_recorrentes_count} registros (R$ {despesas_recorrentes_total:,.2f})")
    
    print("\n📅 Despesas recorrentes configuradas:")
    for despesa in despesas_recorrentes:
        print(f"   📌 {despesa['description']} - Dia {despesa['day']} - R$ {despesa['base_amount']:,.2f}")
    
    print("\n🎯 Agora acesse o dashboard para ver os gráficos com dados realistas!")

if __name__ == '__main__':
    create_sample_data()
