
from django.shortcuts import render, redirect, get_object_or_404
from .models import Items
from .forms import ItemForm, ProductFilterForm


def home(request):
    return render(request, 'inventory/home.html')


def item_list(request):
    items = Items.objects.all()

    return render(request, 'inventory/item_list.html', {'items': items})


def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')  # Po zapisaniu przekierowujemy na listę produktów
    else:
        form = ItemForm()
    return render(request, 'inventory/add_item.html', {'form': form})


def edit_item(request, item_id):
    item = get_object_or_404(Items, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')  # Przekierowanie po zapisaniu
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/edit_item.html', {'form': form})


def delete_item(request, item_id):
    # Znajdź produkt na podstawie jego ID
    item = get_object_or_404(Items, itm_id=item_id)

    # Usuń produkt
    item.delete()

    # Po usunięciu, przekieruj użytkownika z powrotem do listy produktów
    return redirect('item_list')

def ajax_filter_items(request):
    items = Items.objects.all()

    # Pobieranie wartości filtrów z zapytania GET
    name = request.GET.get('name')
    ean = request.GET.get('ean')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filtracja na podstawie wartości z formularza
    if name:
        items = items.filter(itm_name__icontains=name)
    if ean:
        items = items.filter(itm_ean__icontains=ean)
    if min_price:
        items = items.filter(itm_price__gte=min_price)
    if max_price:
        items = items.filter(itm_price__lte=max_price)

    return render(request, 'inventory/item_list_table.html', {'items': items})
