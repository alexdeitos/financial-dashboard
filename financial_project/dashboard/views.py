from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import FinancialData, DashboardConfig
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    
    # Dados do usuário logado - último mês para as transações
    last_month_start = today.replace(day=1)
    # Se hoje for o primeiro dia do mês, pegue o mês anterior
    if today.day == 1:
        if today.month == 1:
            last_month_start = today.replace(year=today.year-1, month=12, day=1)
        else:
            last_month_start = today.replace(month=today.month-1, day=1)
    
    # Transações do último mês (para paginação)
    last_month_transactions = FinancialData.objects.filter(
        user=user, 
        date__gte=last_month_start
    ).order_by('-date')
    
    # Paginação
    page = request.GET.get('page', 1)
    paginator = Paginator(last_month_transactions, 10)  # 10 itens por página
    
    try:
        latest_transactions = paginator.page(page)
    except PageNotAnInteger:
        latest_transactions = paginator.page(1)
    except EmptyPage:
        latest_transactions = paginator.page(paginator.num_pages)
    
    # Estatísticas (usando o filtro selecionado pelo usuário)
    user_data = FinancialData.objects.filter(
        user=user, 
        date__gte=start_date
    )
    
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
    
    context = {
        'user_data': user_data,
        'total_receita': total_receita,
        'total_despesa': total_despesa,
        'total_investimento': total_investimento,
        'saldo': saldo,
        'categories_data': categories_data,
        'latest_transactions': latest_transactions,
        'date_filter': date_filter,
        'last_month_start': last_month_start,
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
    try:
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
        
        print(f"📊 API chamada - Usuário: {user}, Filtro: {date_filter}, Data início: {start_date}")
        
        # Dados para gráfico de categorias
        categories_data = FinancialData.objects.filter(
            user=user, 
            date__gte=start_date
        ).values('category').annotate(total=Sum('amount'))
        
        categories = []
        amounts = []
        
        # Garantir que todas as categorias apareçam, mesmo com valor zero
        category_choices = dict(FinancialData.CATEGORY_CHOICES)
        for category_key, category_name in category_choices.items():
            categories.append(category_name)
            # Encontrar o total para esta categoria
            category_total = next((item['total'] for item in categories_data if item['category'] == category_key), 0)
            amounts.append(float(category_total or 0))
        
        print(f"📈 Dados categorias: {categories} - {amounts}")
        
        # Dados para gráfico de timeline - Versão corrigida
        timeline_data = FinancialData.objects.filter(
            user=user,
            date__gte=start_date
        ).values('date').annotate(
            receita=Sum('amount', filter=Q(category='receita')),
            despesa=Sum('amount', filter=Q(category='despesa'))
        ).order_by('date')
        
        dates = []
        receitas = []
        despesas = []
        
        for item in timeline_data:
            dates.append(item['date'].strftime('%Y-%m-%d'))
            receitas.append(float(item['receita'] or 0))
            despesas.append(float(item['despesa'] or 0))
        
        print(f"📅 Dados timeline: {len(dates)} datas")
        
        response_data = {
            'categories': {
                'labels': categories,
                'data': amounts
            },
            'timeline': {
                'labels': dates,
                'receitas': receitas,
                'despesas': despesas
            }
        }
        
        return JsonResponse(response_data)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Erro na API: {str(e)}")
        print(f"📋 Detalhes: {error_details}")
        
        return JsonResponse({
            'error': str(e),
            'categories': {'labels': [], 'data': []},
            'timeline': {'labels': [], 'receitas': [], 'despesas': []}
        }, status=500)
