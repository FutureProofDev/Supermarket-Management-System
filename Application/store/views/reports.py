# store/views/reports.py

from django.shortcuts import render
from django.db.models import Sum, Count, F, Q, ExpressionWrapper, DecimalField, Avg
from django.utils import timezone
from datetime import date, timedelta
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import permission_required, login_required

from store.models import Product, Sale, SaleItem, Inventory, Customer, Supplier


@permission_required('store.view_sale', raise_exception=True)
def daily_sales_report(request):

    requested_date = parse_date(request.GET.get('date', '') or '')
    report_date = requested_date or timezone.localdate()

    sales = (
        Sale.objects
        .filter(sale_date__date=report_date)
        .select_related('employee', 'customer')
        .order_by('sale_date')
    )

    totals = sales.aggregate(
        total_revenue=Sum('total_amount'),
        total_transactions=Count('sale_id'),
    )
    total_revenue = totals['total_revenue'] or 0
    total_transactions = totals['total_transactions'] or 0

    # Group sale_item rows for the day by product -> qty sold + revenue.
    # line_total is used (not quantity * unit_price) so this stays correct
    # even for discounted lines (loyalty / near-expiry).
    product_breakdown = (
        SaleItem.objects
        .filter(sale__sale_date__date=report_date)
        .values('product__name')
        .annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('line_total'),
        )
        .order_by('-total_revenue')
    )

    total_items_sold = sum(row['total_quantity'] for row in product_breakdown)

    context = {
        'report_date': report_date,
        'previous_date': report_date - timedelta(days=1),
        'next_date': report_date + timedelta(days=1),
        'is_today': report_date == timezone.localdate(),
        'sales': sales,
        'total_revenue': total_revenue,
        'total_transactions': total_transactions,
        'total_items_sold': total_items_sold,
        'product_breakdown': product_breakdown,
    }
    return render(request, 'store/reports/daily_sales_report.html', context)


# GENERAL REPORTS
@login_required
def reports_view(request):
    """
    Central hub page providing quick navigation cards to all system reports.
    """
    return render(request, 'store/reports/reports_view.html')


# ---------------------------------------------------------------------
# Report 1: Low-Stock & Near-Expiry Product Alert Report
# Maps to Q6 & Q10 in advanced_scripts.sql
# ---------------------------------------------------------------------
@permission_required('store.view_inventory', raise_exception=True)
def stock_alerts_report(request):
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
@permission_required('store.view_sale', raise_exception=True)
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