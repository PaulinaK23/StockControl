from django.urls import path
from inventory import views



urlpatterns = [
    # Strona główna
    path('', views.dashboard, name='dashboard'),

    # Produkty
    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('items/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('items/filter/', views.ajax_filter_items, name='ajax_filter_items'),
    path('items/export/', views.export_items_to_excel, name='export_items_to_excel'),

    # Dostawcy
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/<int:supplier_id>/edit/', views.edit_supplier, name='edit_supplier'),
    path('suppliers/<int:supplier_id>/delete/', views.delete_supplier, name='delete_supplier'),
    path('suppliers/export/', views.export_suppliers_to_excel, name='export_suppliers_to_excel'),

    # Stany magazynowe
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/add/', views.add_stock, name='add_stock'),
    path('stocks/<int:stock_id>/edit/', views.edit_stock, name='edit_stock'),
    path('stocks/<int:stock_id>/delete/', views.delete_stock, name='delete_stock'),
    path('stocks/export/', views.export_stocks_to_excel, name='export_stocks_to_excel'),

    #Zamówienia
    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.add_order, name='add_order'),
    path('orders/<int:order_id>/edit/', views.edit_order, name='edit_order'),
    path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('orders/export/', views.export_orders_to_excel, name='export_orders_to_excel'),


]
