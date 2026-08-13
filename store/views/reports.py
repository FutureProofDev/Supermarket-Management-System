from datetime import timedelta

from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date

from ..models import Sale, SaleItem


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
