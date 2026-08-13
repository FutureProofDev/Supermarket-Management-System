# store/views/reports.py

from django.shortcuts import render
from django.db.models import Sum, Count, F, Q, ExpressionWrapper, DecimalField, Avg
from django.utils import timezone
from datetime import date, timedelta
from store.models import Product, Sale, SaleItem, Inventory, Customer, Supplier


def reports_hub(request):
    """
    Central hub page providing quick navigation cards to all system reports.
    """
    return render(request, 'store/reports/reports_hub.html')

# ---------------------------------------------------------------------
# Report 1: Low-Stock & Near-Expiry Product Alert Report
# Maps to Q6 & Q10 in advanced_scripts.sql
# ---------------------------------------------------------------------
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


# ---------------------------------------------------------------------
# Report 2: Sales & Revenue Analytics Report
# Maps to Q4 & Q8 in advanced_scripts.sql
# ---------------------------------------------------------------------
def report_sales_analytics(request):
    # Total Revenue & Transaction Count
    totals = Sale.objects.aggregate(
        grand_total=Sum('total_amount'),
        total_sales=Count('sale_id')
    )

    # Top 5 Customers by Lifetime Spend
    top_customers = Customer.objects.annotate(
        num_purchases=Count('sales'),
        lifetime_spend=Sum('sales__total_amount')
    ).filter(lifetime_spend__isnull=False).order_by('-lifetime_spend')[:5]

    # Revenue by Product Category
    category_revenue = SaleItem.objects.values(
        category_name=F('product__category__name')
    ).annotate(
        total_revenue=Sum('line_total'),
        units_sold=Sum('quantity')
    ).order_by('-total_revenue')

    context = {
        'grand_total': totals['grand_total'] or 0,
        'total_sales': totals['total_sales'] or 0,
        'top_customers': top_customers,
        'category_revenue': category_revenue,
    }
    return render(request, 'store/reports/sales_analytics.html', context)