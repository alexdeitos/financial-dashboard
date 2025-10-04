from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FinancialData(models.Model):
    CATEGORY_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
        ('investimento', 'Investimento'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Novo campo para indicar se é recorrente
    is_recurring = models.BooleanField(default=False)
    recurring_day = models.IntegerField(null=True, blank=True, help_text="Dia do mês para despesas recorrentes (1-31)")
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        recurrente = " 🔄" if self.is_recurring else ""
        return f"{self.user.username} - {self.description} - R$ {self.amount}{recurrente}"

class DashboardConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=20, default='light', choices=[('light', 'Claro'), ('dark', 'Escuro')])
    currency = models.CharField(max_length=10, default='BRL')
    language = models.CharField(max_length=10, default='pt-br')
    
    def __str__(self):
        return f"Configurações do Dashboard - {self.user.username}"
