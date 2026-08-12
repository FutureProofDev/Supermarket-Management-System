from django.contrib import admin
from .models import (
    Supplier, Category, Employee, Customer, Discount,
    Product, PurchaseOrder, PurchaseOrderItem, Inventory,
    Sale, SaleItem, LoyaltyCard,
)
# Register your models here.
 
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Discount)
admin.site.register(Product)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(Inventory)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(LoyaltyCard)
