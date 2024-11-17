# inventory/forms.py

from django import forms
from .models import Items, Categories, Suppliers


class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['itm_name', 'itm_ean', 'itm_catid', 'itm_uniid', 'itm_supid', 'itm_price', 'itm_minquantity',
                  'itm_isactive']
        labels = {
            'itm_name': 'Nazwa produktu',
            'itm_ean': 'Kod EAN',
            'itm_catid': 'Kategoria',
            'itm_uniid': 'Jednostka miary',
            'itm_supid': 'Dostawca',
            'itm_price': 'Cena',
            'itm_minquantity': 'Minimalna ilość',
            'itm_isactive': 'Aktywny',
        }
        widgets = {
            'itm_name': forms.TextInput(attrs={'class': 'form-control'}),
            'itm_ean': forms.TextInput(attrs={'class': 'form-control'}),
            'itm_catid': forms.Select(attrs={'class': 'form-select'}),
            'itm_uniid': forms.Select(attrs={'class': 'form-select'}),
            'itm_supid': forms.Select(attrs={'class': 'form-select'}),
            'itm_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'itm_minquantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'itm_isactive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductFilterForm(forms.Form):
    name = forms.CharField(required=False, label="Nazwa produktu", widget=forms.TextInput(attrs={'class': 'form-control'}))
    ean = forms.CharField(required=False, label="Kod EAN", widget=forms.TextInput(attrs={'class': 'form-control'}))
    min_price = forms.DecimalField(required=False, label="Cena minimalna", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_price = forms.DecimalField(required=False, label="Cena maksymalna", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), required=False, label="Kategoria", widget=forms.Select(attrs={'class': 'form-select'}))
    is_active = forms.ChoiceField(choices=[('', 'Wszystkie'), (1, 'Aktywny'), (0, 'Nieaktywny')], required=False, label="Status", widget=forms.Select(attrs={'class': 'form-select'}))