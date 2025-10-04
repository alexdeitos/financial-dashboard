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
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.description} - R$ {self.amount}"

class DashboardConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=20, default='light', choices=[('light', 'Claro'), ('dark', 'Escuro')])
    currency = models.CharField(max_length=10, default='BRL')
    language = models.CharField(max_length=10, default='pt-br')
    
    def __str__(self):
        return f"Configurações do Dashboard - {self.user.username}"
