from django.contrib import admin
from .models import FinancialData, DashboardConfig

@admin.register(FinancialData)
class FinancialDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'description', 'amount', 'date', 'is_recurring', 'recurring_day')
    list_filter = ('category', 'date', 'user', 'is_recurring')
    search_fields = ('description', 'user__username')
    date_hierarchy = 'date'
    ordering = ('-date',)

@admin.register(DashboardConfig)
class DashboardConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'currency', 'language')
    list_filter = ('theme', 'currency')
    search_fields = ('user__username',)
