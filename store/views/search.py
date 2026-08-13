from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product, Customer, Sale, Inventory, Category, Supplier, Employee

def search_page(request):
    entity = request.GET.get('entity', 'products')
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    supplier_id = request.GET.get('supplier', '')
    employee_id = request.GET.get('employee', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    low_stock = request.GET.get('low_stock', '')
    sort_by = request.GET.get('sort_by', '')
    sort_dir = request.GET.get('sort_dir', 'asc')

    results = None

    # Common relational dropdown data
    categories = Category.objects.all().order_by('name')
    suppliers = Supplier.objects.all().order_by('name')
    employees = Employee.objects.all().order_by('last_name', 'first_name')

    # ==================== ENTITY: PRODUCTS ====================
    if entity == 'products':
        qs = Product.objects.select_related('category', 'supplier', 'inventory')
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(barcode__icontains=query))
        if category_id:
            qs = qs.filter(category_id=category_id)
        if supplier_id:
            qs = qs.filter(supplier_id=supplier_id)

        # Dynamic Sorting
        sort_map = {'name': 'name', 'price': 'unit_price', 'expiry': 'expiry_date'}
        order_field = sort_map.get(sort_by, 'name')
        if sort_dir == 'desc':
            order_field = '-' + order_field
        results = qs.order_by(order_field)

    # ==================== ENTITY: SALES ====================
    elif entity == 'sales':
        qs = Sale.objects.select_related('employee', 'customer')
        if query:
            qs = qs.filter(
                Q(sale_id__icontains=query) |
                Q(customer__first_name__icontains=query) |
                Q(customer__last_name__icontains=query) |
                Q(employee__first_name__icontains=query)
            )
        if employee_id:
            qs = qs.filter(employee_id=employee_id)
        if date_from:
            qs = qs.filter(sale_date__date__gte=date_from)
        if date_to:
            qs = qs.filter(sale_date__date__lte=date_to)

        sort_map = {'date': 'sale_date', 'amount': 'total_amount', 'id': 'sale_id'}
        order_field = sort_map.get(sort_by, 'sale_date')
        if sort_dir == 'desc' or not sort_by:
            order_field = '-' + order_field if sort_by else '-sale_date'
        results = qs.order_by(order_field)

    # ==================== ENTITY: CUSTOMERS ====================
    elif entity == 'customers':
        qs = Customer.objects.select_related('loyalty_card')
        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query)
            )
        sort_map = {'name': 'last_name', 'email': 'email'}
        order_field = sort_map.get(sort_by, 'last_name')
        if sort_dir == 'desc':
            order_field = '-' + order_field
        results = qs.order_by(order_field)

    # ==================== ENTITY: INVENTORY ====================
    elif entity == 'inventory':
        qs = Inventory.objects.select_related('product', 'product__category', 'product__supplier')
        if query:
            qs = qs.filter(
                Q(product__name__icontains=query) |
                Q(product__barcode__icontains=query)
            )
        if category_id:
            qs = qs.filter(product__category_id=category_id)
        if low_stock == '1':
            qs = qs.filter(quantity_on_hand__lte=F('reorder_level'))

        sort_map = {'name': 'product__name', 'qty': 'quantity_on_hand', 'reorder': 'reorder_level'}
        order_field = sort_map.get(sort_by, 'product__name')
        if sort_dir == 'desc':
            order_field = '-' + order_field
        results = qs.order_by(order_field)

    context = {
        'entity': entity,
        'query': query,
        'category_id': category_id,
        'supplier_id': supplier_id,
        'employee_id': employee_id,
        'date_from': date_from,
        'date_to': date_to,
        'low_stock': low_stock,
        'sort_by': sort_by,
        'sort_dir': sort_dir,
        'categories': categories,
        'suppliers': suppliers,
        'employees': employees,
        'results': results,
        'result_count': results.count() if results is not None else 0
    }
    return render(request, 'store/search/search_page.html', context)