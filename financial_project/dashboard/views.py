from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import FinancialData, DashboardConfig
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    user = request.user
    
    # Filtros de data
    date_filter = request.GET.get('date_filter', 'month')
    today = timezone.now().date()
    
    if date_filter == 'week':
        start_date = today - timedelta(days=7)
    elif date_filter == 'month':
        start_date = today.replace(day=1)
    elif date_filter == 'year':
        start_date = today.replace(month=1, day=1)
    else:
        start_date = today - timedelta(days=30)
    
    # Dados do usuário logado
    user_data = FinancialData.objects.filter(
        user=user, 
        date__gte=start_date
    )
    
    # Estatísticas
    total_receita = user_data.filter(category='receita').aggregate(Sum('amount'))['amount__sum'] or 0
    total_despesa = user_data.filter(category='despesa').aggregate(Sum('amount'))['amount__sum'] or 0
    total_investimento = user_data.filter(category='investimento').aggregate(Sum('amount'))['amount__sum'] or 0
    saldo = total_receita - total_despesa
    
    # Dados para gráficos
    categories_data = {
        'Receita': float(total_receita),
        'Despesa': float(total_despesa),
        'Investimento': float(total_investimento),
    }
    
    # Últimas transações
    latest_transactions = user_data.order_by('-date')[:10]
    
    context = {
        'user_data': user_data,
        'total_receita': total_receita,
        'total_despesa': total_despesa,
        'total_investimento': total_investimento,
        'saldo': saldo,
        'categories_data': categories_data,
        'latest_transactions': latest_transactions,
        'date_filter': date_filter,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@staff_member_required
def admin_dashboard(request):
    # Dashboard administrativo
    all_users = User.objects.all()
    selected_user_id = request.GET.get('user_id')
    
    if selected_user_id:
        selected_user = get_object_or_404(User, id=selected_user_id)
        user_data = FinancialData.objects.filter(user=selected_user)
    else:
        selected_user = None
        user_data = FinancialData.objects.all()
    
    # Estatísticas gerais
    total_users = User.objects.count()
    total_transactions = FinancialData.objects.count()
    total_amount = FinancialData.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Estatísticas por categoria
    receita_total = FinancialData.objects.filter(category='receita').aggregate(Sum('amount'))['amount__sum'] or 0
    despesa_total = FinancialData.objects.filter(category='despesa').aggregate(Sum('amount'))['amount__sum'] or 0
    investimento_total = FinancialData.objects.filter(category='investimento').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'all_users': all_users,
        'selected_user': selected_user,
        'user_data': user_data,
        'total_users': total_users,
        'total_transactions': total_transactions,
        'total_amount': total_amount,
        'receita_total': receita_total,
        'despesa_total': despesa_total,
        'investimento_total': investimento_total,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def api_chart_data(request):
    user = request.user
    date_filter = request.GET.get('date_filter', 'month')
    today = timezone.now().date()
    
    if date_filter == 'week':
        start_date = today - timedelta(days=7)
    elif date_filter == 'month':
        start_date = today.replace(day=1)
    elif date_filter == 'year':
        start_date = today.replace(month=1, day=1)
    else:
        start_date = today - timedelta(days=30)
    
    # Dados para gráfico de categorias
    categories_data = FinancialData.objects.filter(
        user=user, 
        date__gte=start_date
    ).values('category').annotate(total=Sum('amount'))
    
    categories = []
    amounts = []
    
    for item in categories_data:
        categories.append(dict(FinancialData.CATEGORY_CHOICES)[item['category']])
        amounts.append(float(item['total']))
    
    # Dados para gráfico de timeline
    timeline_data = FinancialData.objects.filter(
        user=user, 
        date__gte=start_date
    ).extra({'date_formatted': "TO_CHAR(date, 'YYYY-MM-DD')"}).values('date_formatted').annotate(
        receita=Sum('amount', filter=models.Q(category='receita')),
        despesa=Sum('amount', filter=models.Q(category='despesa'))
    ).order_by('date_formatted')
    
    dates = [item['date_formatted'] for item in timeline_data]
    receitas = [float(item['receita'] or 0) for item in timeline_data]
    despesas = [float(item['despesa'] or 0) for item in timeline_data]
    
    return JsonResponse({
        'categories': {
            'labels': categories,
            'data': amounts
        },
        'timeline': {
            'labels': dates,
            'receitas': receitas,
            'despesas': despesas
        }
    })
