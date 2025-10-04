from django import forms
from .models import FinancialData

class FinancialDataForm(forms.ModelForm):
    class Meta:
        model = FinancialData
        fields = ['category', 'description', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'placeholder': 'Descrição da transação'}),
            'amount': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01'}),
        }
