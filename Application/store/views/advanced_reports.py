from django.db import connection
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

# SQL based reports


def _dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


#  VIEW-BACKED REPORTS 

@login_required
def category_overview_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_category_overview ORDER BY category_name")
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/category_overview.html', {'results': results})


@permission_required('store.view_discount', raise_exception=True)
def active_discounts_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_active_discounts ORDER BY days_remaining")
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/active_discounts.html', {'results': results})


@permission_required('store.view_inventory', raise_exception=True)
def near_expiry_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_near_expiry_products ORDER BY days_until_expiry")
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/near_expiry.html', {'results': results})


@login_required
def unlinked_employees_view(request):
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_unlinked_employees")
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/unlinked_employees.html', {'results': results})


@permission_required('store.view_customer', raise_exception=True)
def customers_without_loyalty_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_customers_without_loyalty")
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/customers_without_loyalty.html', {'results': results})


#  ADVANCED QUERY REPORTS 

@permission_required('store.view_product', raise_exception=True)
def dead_stock_view(request):
    query = """
        SELECT p.product_id, p.name, p.unit_price, c.name AS category_name
        FROM product p
        JOIN category c ON p.category_id = c.category_id
        LEFT JOIN sale_item si ON p.product_id = si.product_id
        WHERE si.sale_item_id IS NULL
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/never_sold_products.html', {'results': results})


@permission_required('store.view_product', raise_exception=True)
def top_products_by_category_view(request):
    query = """
        SELECT category_name, product_name, total_quantity_sold, rnk
        FROM (
            SELECT
                c.name AS category_name,
                p.name AS product_name,
                SUM(si.quantity) AS total_quantity_sold,
                ROW_NUMBER() OVER (PARTITION BY c.category_id ORDER BY SUM(si.quantity) DESC) AS rnk
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            JOIN sale_item si ON p.product_id = si.product_id
            GROUP BY c.category_id, c.name, p.product_id, p.name
        ) ranked
        WHERE rnk <= 3
        ORDER BY category_name, rnk
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/top_products_by_category.html', {'results': results})


@permission_required('store.view_sale', raise_exception=True)
def weekday_sales_view(request):
    query = """
        SELECT
            DAYNAME(sale_date) AS weekday,
            COUNT(*) AS transaction_count,
            ROUND(SUM(total_amount), 2) AS total_revenue
        FROM sale
        GROUP BY DAYNAME(sale_date), DAYOFWEEK(sale_date)
        ORDER BY DAYOFWEEK(sale_date)
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/weekday_sales.html', {'results': results})


@permission_required('store.view_sale', raise_exception=True)
def repeat_customer_employee_view(request):
    query = """
        SELECT
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            COUNT(*) AS times_served
        FROM sale s
        JOIN employee e ON s.employee_id = e.employee_id
        JOIN customer c ON s.customer_id = c.customer_id
        GROUP BY e.employee_id, employee_name, c.customer_id, customer_name
        HAVING COUNT(*) > 1
        ORDER BY times_served DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/repeat_customer_employee.html', {'results': results})


#  STORED PROCEDURE REPORTS 

@permission_required('store.view_customer', raise_exception=True)
def top_customers_view(request):
    with connection.cursor() as cursor:
        cursor.callproc('sp_top_customers', [10])
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/top_customers.html', {'results': results})


@permission_required('store.view_sale', raise_exception=True)
def category_performance_view(request):
    from django.utils import timezone
    today = timezone.localdate()
    start = request.GET.get('start', today.replace(day=1).isoformat())
    end = request.GET.get('end', today.isoformat())

    with connection.cursor() as cursor:
        cursor.callproc('sp_category_performance', [start, end])
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/category_performance.html', {
        'results': results, 'start': start, 'end': end,
    })


@permission_required('store.view_supplier', raise_exception=True)
def supplier_performance_view(request):
    from django.utils import timezone
    today = timezone.localdate()
    start = request.GET.get('start', today.replace(day=1).isoformat())
    end = request.GET.get('end', today.isoformat())

    with connection.cursor() as cursor:
        cursor.callproc('sp_supplier_performance', [start, end])
        results = _dictfetchall(cursor)
    return render(request, 'store/reports/advanced/supplier_performance.html', {
        'results': results, 'start': start, 'end': end,
    })