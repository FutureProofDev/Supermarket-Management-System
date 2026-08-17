# store/admin.py

from django.contrib import admin
from .models import (
    Supplier, Category, Employee, Customer, Discount,
    Product, PurchaseOrder, PurchaseOrderItem, Inventory,
    Sale, SaleItem, LoyaltyCard
)

#  

class SaleItemInline(admin.TabularInline):
    """Allows viewing and editing SaleItems directly inside the Sale page."""
    model = SaleItem
    extra = 0
    

class PurchaseOrderItemInline(admin.TabularInline):
    """Allows viewing PurchaseOrderItems directly inside the PurchaseOrder page."""
    model = PurchaseOrderItem
    extra = 0

class InventoryInline(admin.StackedInline):
    """Displays Inventory stock status directly on the Product admin page."""
    model = Inventory
    can_delete = False

#  MODEL ADMINS 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'supplier', 'unit_price', 'barcode', 'expiry_date')

    
    list_filter = ('category', 'supplier')

   
    search_fields = ('name', 'barcode', 'category__name', 'supplier__name')
    inlines = [InventoryInline]

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_id', 'sale_date', 'employee', 'customer', 'total_amount')
    list_filter = ('sale_date', 'employee')
    search_fields = ('sale_id', 'customer__first_name', 'customer__last_name')

    inlines = [SaleItemInline]

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_id', 'supplier', 'order_date', 'status')
    list_filter = ('status', 'supplier')
    inlines = [PurchaseOrderItemInline]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'phone', 'email', 'get_loyalty_points')
    search_fields = ('first_name', 'last_name', 'phone')

    def get_loyalty_points(self, obj):

        return obj.loyalty_card.points_balance if hasattr(obj, 'loyalty_card') else "No Card"
    get_loyalty_points.short_description = "Loyalty Points"



admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Employee)
admin.site.register(Discount)
admin.site.register(Inventory)
admin.site.register(SaleItem)
admin.site.register(PurchaseOrderItem)
admin.site.register(LoyaltyCard)