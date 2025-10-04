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
            password='demo1234',
            first_name='demo',
            last_name='Demonstracao'
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
    
    # DESPESAS (25 registros)
    despesas = [
        {'description': 'Aluguel Residencial', 'base_amount': 1200.00, 'variation': 0},
        {'description': 'Supermercado', 'base_amount': 600.00, 'variation': 150},
        {'description': 'Transporte/Combustível', 'base_amount': 400.00, 'variation': 100},
        {'description': 'Energia Elétrica', 'base_amount': 180.00, 'variation': 50},
        {'description': 'Água e Esgoto', 'base_amount': 90.00, 'variation': 20},
        {'description': 'Internet', 'base_amount': 120.00, 'variation': 10},
        {'description': 'Plano de Saúde', 'base_amount': 350.00, 'variation': 0},
        {'description': 'Academia', 'base_amount': 100.00, 'variation': 0},
        {'description': 'Streaming (Netflix/Spotify)', 'base_amount': 60.00, 'variation': 10},
        {'description': 'Telefone Celular', 'base_amount': 80.00, 'variation': 10},
        {'description': 'Restaurante', 'base_amount': 300.00, 'variation': 100},
        {'description': 'Farmácia', 'base_amount': 120.00, 'variation': 50},
        {'description': 'Vestuário', 'base_amount': 250.00, 'variation': 100},
        {'description': 'Manutenção Carro', 'base_amount': 200.00, 'variation': 100},
        {'description': 'Presentes', 'base_amount': 150.00, 'variation': 80},
        {'description': 'Cursos', 'base_amount': 300.00, 'variation': 150},
        {'description': 'Livros', 'base_amount': 100.00, 'variation': 50},
        {'description': 'Cinema/Entretenimento', 'base_amount': 120.00, 'variation': 50},
        {'description': 'Seguro Residencial', 'base_amount': 80.00, 'variation': 10},
        {'description': 'IPTU', 'base_amount': 150.00, 'variation': 0},
        {'description': 'Material Escritório', 'base_amount': 70.00, 'variation': 30},
        {'description': 'Assinaturas Revistas', 'base_amount': 50.00, 'variation': 10},
        {'description': 'Doações', 'base_amount': 100.00, 'variation': 50},
        {'description': 'Viagem Fim de Semana', 'base_amount': 400.00, 'variation': 150},
        {'description': 'Manutenção Casa', 'base_amount': 180.00, 'variation': 80},
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
            'amount': round(amount, 2)
        })

    # Adiciona despesas
    for item in despesas:
        amount = item['base_amount'] + random.uniform(-item['variation'], item['variation'])
        sample_data.append({
            'category': 'despesa',
            'description': item['description'],
            'amount': round(amount, 2)
        })

    # Adiciona investimentos
    for item in investimentos:
        amount = item['base_amount'] + random.uniform(-item['variation'], item['variation'])
        sample_data.append({
            'category': 'investimento',
            'description': item['description'],
            'amount': round(amount, 2)
        })

    # Cria os registros com datas distribuídas nos últimos 6 meses
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
            date=transaction_date
        )
        created_count += 1

    # Cria algumas transações recorrentes (mesma descrição, meses diferentes)
    transacoes_recorrentes = [
        {'category': 'receita', 'description': 'Salário Mensal', 'amount': 4500.00},
        {'category': 'despesa', 'description': 'Aluguel Mensal', 'amount': 1200.00},
        {'category': 'despesa', 'description': 'Supermercado Mensal', 'amount': 650.00},
    ]
    
    for transacao in transacoes_recorrentes:
        for month_offset in range(6):  # Últimos 6 meses
            date_offset = timedelta(days=30 * month_offset + random.randint(1, 28))
            transaction_date = base_date - date_offset
            
            FinancialData.objects.create(
                user=user,
                category=transacao['category'],
                description=transacao['description'],
                amount=transacao['amount'] + random.uniform(-50, 50),
                date=transaction_date
            )
            created_count += 1

    print(f"✅ {created_count} registros de exemplo criados para o usuário {user.username}")
    print("📊 Estatísticas criadas:")
    
    # Mostra estatísticas
    total_receita = FinancialData.objects.filter(user=user, category='receita').aggregate(Sum('amount'))['amount__sum'] or 0
    total_despesa = FinancialData.objects.filter(user=user, category='despesa').aggregate(Sum('amount'))['amount__sum'] or 0
    total_investimento = FinancialData.objects.filter(user=user, category='investimento').aggregate(Sum('amount'))['amount__sum'] or 0
    
    print(f"   💰 Receita Total: R$ {total_receita:,.2f}")
    print(f"   💸 Despesa Total: R$ {total_despesa:,.2f}")
    print(f"   📈 Investimento Total: R$ {total_investimento:,.2f}")
    print(f"   ⚖️ Saldo: R$ {(total_receita - total_despesa):,.2f}")
    print("\n🎯 Agora acesse o dashboard para ver os gráficos com dados realistas!")

if __name__ == '__main__':
    create_sample_data()
