from django.shortcuts import render
from django.db.models import F
from django.contrib.auth.decorators import user_passes_test
from ..models import Product, Category, Supplier, Inventory
from django.db import connection
from django.utils import timezone

def home_view(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()

    current_hour = timezone.localtime().hour
    with connection.cursor() as cursor:
        cursor.execute("SELECT fn_greeting_for_hour(%s)", [current_hour])
        greeting = cursor.fetchone()[0]

    # Fetch inventory rows that are at or below their reorder threshold.
    low_stock_items = (
        Inventory.objects
        .select_related('product__category')
        .filter(quantity_on_hand__lte=F('reorder_level'))
        .order_by('quantity_on_hand', 'product__name')
    )
    print(greeting)

    context = {
        'greeting': greeting,
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'low_stock_count': low_stock_items.count(),
        'low_stock_items': low_stock_items,
    }
    return render(request, 'store/home.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='home')
def system_register(request):
    return render(request, 'store/system_register.html')