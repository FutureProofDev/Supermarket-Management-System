from django.urls import path
from store import views



urlpatterns = urlpatterns = [
    # Server landing page (root URL)
    path('', views.home_view, name='home'),

    # Central Directory
    path('register/', views.system_register, name='system_register'),

    # Reports URLs
    path('reports/', views.reports_view, name='reports_view'),
    path('reports/daily-sales/', views.daily_sales_report, name='daily_sales_report'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/new/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),

    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/new/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    # Customer URLs
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/new/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    # Discount URLs
    path('discounts/', views.discount_list, name='discount_list'),
    path('discounts/new/', views.discount_create, name='discount_create'),
    path('discounts/<int:pk>/', views.discount_detail, name='discount_detail'),
    path('discounts/<int:pk>/edit/', views.discount_update, name='discount_update'),
    path('discounts/<int:pk>/delete/', views.discount_delete, name='discount_delete'),

    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # PurchaseOrder URLs
    path('purchase-orders/', views.purchaseorder_list, name='purchaseorder_list'),
    path('purchase-orders/new/', views.purchaseorder_create, name='purchaseorder_create'),
    path('purchase-orders/<int:pk>/', views.purchaseorder_detail, name='purchaseorder_detail'),
    path('purchase-orders/<int:pk>/edit/', views.purchaseorder_update, name='purchaseorder_update'),
    path('purchase-orders/<int:pk>/delete/', views.purchaseorder_delete, name='purchaseorder_delete'),

    # Inventory URLs
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/new/', views.inventory_create, name='inventory_create'),
    path('inventory/<int:pk>/', views.inventory_detail, name='inventory_detail'),
    path('inventory/<int:pk>/edit/', views.inventory_update, name='inventory_update'),
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),

    # LoyaltyCard URLs
    path('loyalty-cards/', views.loyaltycard_list, name='loyaltycard_list'),
    path('loyalty-cards/new/', views.loyaltycard_create, name='loyaltycard_create'),
    path('loyalty-cards/<int:pk>/', views.loyaltycard_detail, name='loyaltycard_detail'),
    path('loyalty-cards/<int:pk>/edit/', views.loyaltycard_update, name='loyaltycard_update'),
    path('loyalty-cards/<int:pk>/delete/', views.loyaltycard_delete, name='loyaltycard_delete'),



    # Report URLs
    path('reports/', views.reports_hub, name='reports_hub'),
    path('reports/low-stock-expiry/', views.report_low_stock_and_expiry, name='report_low_stock_expiry'),
    path('reports/sales-analytics/', views.report_sales_analytics, name='report_sales_analytics'),
]