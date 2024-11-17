from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Categories, Items, Stock, Suppliers, Units, Warehouses

admin.site.register(Categories)
admin.site.register(Items)
admin.site.register(Stock)
admin.site.register(Suppliers)
admin.site.register(Units)
admin.site.register(Warehouses)
