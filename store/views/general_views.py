from django.shortcuts import render,  redirect, get_object_or_404

from django.db.models import ProtectedError
from django.db.models import F
from django.contrib import messages

from ..models import *
from ..forms import *

from datetime import date, timedelta


def home_view(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()

    # Fetch inventory rows that are at or below their reorder threshold.
    low_stock_items = (
        Inventory.objects
        .select_related('product__category')
        .filter(quantity_on_hand__lte=F('reorder_level'))
        .order_by('quantity_on_hand', 'product__name')
    )
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'low_stock_count': low_stock_items.count(),
        'low_stock_items': low_stock_items,
    }
    return render(request, 'store/home.html', context)


def system_register(request):
    return render(request, 'store/system_register.html')




# store/views/reports.py (might move to reports.py)

# Report 1: Low-Stock & Near-Expiry Product Alert Report

def report_low_stock_and_expiry(request):
    today = date.today()
    near_expiry_threshold = today + timedelta(days=45)

    # Low-Stock Items
    low_stock_items = Inventory.objects.select_related('product', 'product__supplier').filter(
        quantity_on_hand__lte=F('reorder_level')
    ).order_by('quantity_on_hand')

    # Near-Expiry Products (expiry_date within 45 days)
    near_expiry_products = Product.objects.select_related('supplier', 'inventory').filter(
        expiry_date__isnull=False,
        expiry_date__lte=near_expiry_threshold
    ).order_by('expiry_date')

    context = {
        'low_stock_items': low_stock_items,
        'near_expiry_products': near_expiry_products,
        'today': today,
    }
    return render(request, 'store/reports/low_stock_expiry.html', context)




