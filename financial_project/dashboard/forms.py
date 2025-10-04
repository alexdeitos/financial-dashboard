from django import forms

class FinancialDataForm(forms.ModelForm):
    class Meta:
        model = FinancialData
        fields = '__all__'
    
    def clean_recurring_day(self):
        day = self.cleaned_data.get('recurring_day')
        if day and (day < 1 or day > 31):
            raise forms.ValidationError("O dia recorrente deve estar entre 1 e 31.")
        return day

@admin.register(FinancialData)
class FinancialDataAdmin(admin.ModelAdmin):
    form = FinancialDataForm
    list_display = ('user', 'category', 'description', 'amount', 'date', 'is_recurring', 'recurring_day')
    list_filter = ('category', 'date', 'user', 'is_recurring')
    search_fields = ('description', 'user__username')
    date_hierarchy = 'date'
    ordering = ('-date',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'category', 'description', 'amount', 'date')
        }),
        ('Configurações Recorrentes', {
            'fields': ('is_recurring', 'recurring_day'),
            'classes': ('collapse',),
        }),
    )
