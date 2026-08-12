from django.shortcuts import render,  redirect, get_object_or_404

from django.db.models import ProtectedError
from django.contrib import messages

from ..models import *
from ..forms import *

def home_view(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    
    # Fetch items with 5 or fewer units in stock
    low_stock_products = Product.objects.filter(stock__lte=5)
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'low_stock_count': low_stock_products.count(),
        'low_stock_products': low_stock_products,
    }
    return render(request, 'store/home.html', context)