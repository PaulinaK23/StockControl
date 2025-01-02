# inventory/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Items, Categories, Suppliers, Stock, Orders, OrderItems, Attachments


class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['itm_name', 'itm_ean', 'itm_catid', 'itm_supid', 'itm_price',
                  'itm_isactive','itm_minquantity', 'itm_uniid',]
        labels = {
            'itm_name': 'Nazwa produktu',
            'itm_ean': 'Kod EAN',
            'itm_catid': 'Kategoria',
            'itm_supid': 'Dostawca',
            'itm_price': 'Cena',
            'itm_isactive': 'Aktywny',
            'itm_minquantity': 'Ilość minimalna',
            'itm_uniid': 'Jednostka miary',
        }
        widgets = {
            'itm_name': forms.TextInput(attrs={'class': 'form-control'}),
            'itm_ean': forms.TextInput(attrs={'class': 'form-control'}),
            'itm_catid': forms.Select(attrs={'class': 'form-select'}),
            'itm_supid': forms.Select(attrs={'class': 'form-select'}),
            'itm_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'itm_isactive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'itm_minquantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'itm_uniid': forms.Select(attrs={'class': 'form-select'}),
        }


class ProductFilterForm(forms.Form):
    name = forms.CharField(required=False, label="Nazwa produktu", widget=forms.TextInput(attrs={'class': 'form-control'}))
    ean = forms.CharField(required=False, label="Kod EAN", widget=forms.TextInput(attrs={'class': 'form-control'}))
    min_price = forms.DecimalField(required=False, label="Cena minimalna", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_price = forms.DecimalField(required=False, label="Cena maksymalna", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), required=False, label="Kategoria", widget=forms.Select(attrs={'class': 'form-select'}))
    is_active = forms.ChoiceField(choices=[('', 'Wszystkie'), (1, 'Aktywny'), (0, 'Nieaktywny')], required=False, label="Status", widget=forms.Select(attrs={'class': 'form-select'}))


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['stk_itmid', 'stk_whsid', 'stk_qty']
        labels = {
            'stk_itmid': 'Produkt',
            'stk_whsid': 'Magazyn',
            'stk_qty': 'Ilość',
        }
        widgets = {
            'stk_itmid': forms.Select(attrs={'class': 'form-control'}),
            'stk_whsid': forms.Select(attrs={'class': 'form-control'}),
            'stk_qty': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # Wszystkie pola wymagane
    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = ['sup_name', 'sup_taxid', 'sup_email', 'sup_phone', 'sup_paymentterms', 'sup_address']
        labels = {
            'sup_name': 'Nazwa dostawcy',
            'sup_taxid': 'NIP',
            'sup_email': 'Email',
            'sup_phone': 'Telefon',
            'sup_paymentterms': 'Warunki płatności',
            'sup_address': 'Adres',
        }
        widgets = {
            'sup_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sup_taxid': forms.TextInput(attrs={'class': 'form-control'}),
            'sup_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'sup_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'sup_paymentterms': forms.TextInput(attrs={'class': 'form-control'}),
            'sup_address': forms.Textarea(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['ord_date', 'ord_statusid', 'ord_whsid', 'ord_supid', 'ord_number']
        widgets = {
            'ord_date': forms.DateInput(
                format='%Y-%m-%d',  # Format daty zgodny z bazą danych
                attrs={
                    'class': 'form-control',
                    'type': 'date',  # HTML5 input typu 'date'
                }
            ),
            'ord_statusid': forms.Select(attrs={'class': 'form-select'}),
            'ord_whsid': forms.Select(attrs={'class': 'form-select'}),
            'ord_supid': forms.Select(attrs={'class': 'form-select'}),
            'ord_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Jeśli instancja istnieje, ustaw datę w polu w odpowiednim formacie
        if self.instance and self.instance.pk:
            if self.instance.ord_date:
                self.fields['ord_date'].initial = self.instance.ord_date.strftime('%Y-%m-%d')


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItems
        exclude = ['oit_id']
        fields = ['oit_itmid', 'oit_quantity', 'oit_price']
        labels = {
            'oit_itmid': 'Produkt',
            'oit_quantity': 'Ilość',
            'oit_price': 'Cena jednostkowa',
        }
        widgets = {
            'oit_itmid': forms.Select(attrs={'class': 'form-select'}),
            'oit_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'oit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Dodaj ukryte pole DELETE
            self.fields['DELETE'] = forms.BooleanField(
                required=False,
                widget=forms.HiddenInput()
            )

OrderItemFormSet = inlineformset_factory(
    Orders,
    OrderItems,
    form=OrderItemForm,
    extra=0,
    can_delete=True
)
