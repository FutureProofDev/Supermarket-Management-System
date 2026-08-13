from django.db import models
from django.utils import timezone
from datetime import timedelta




class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        db_table = 'supplier'

    def __str__(self):
        return self.name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # DDL had both `unique` on phone AND a separate idx_customer_phone index,
    # which is redundant (a unique constraint already creates an index in MySQL).
    # unique=True below covers it; no separate Meta.indexes entry needed.
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    percent_off = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'discount'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(percent_off__gte=0) & models.Q(percent_off__lte=100),
                name="discount_percent_off_range",
            ),
            models.CheckConstraint(
                condition=models.Q(end_date__gte=models.F("start_date")),
                name="discount_end_after_start",
            ),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    barcode = models.CharField(max_length=50, unique=True)
    # New field, closing the expiry-discount gap identified earlier.
    expiry_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'product'
        constraints = [
            models.CheckConstraint(condition=models.Q(unit_price__gte=0), name="product_unit_price_gte_0"),
        ]
        indexes = [
            models.Index(fields=['name'], name='idx_product_name'),
        ]

    def is_near_expiry(self):
        if not self.expiry_date:
            return False
        return self.expiry_date <= timezone.localdate() + timedelta(days=45)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Cancelled', 'Cancelled'),
    ]
    po_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        db_table = 'purchase_order'
        indexes = [
            models.Index(fields=['order_date'], name='idx_po_date'),
        ]

    def __str__(self):
        return f"PO#{self.po_id} - {self.supplier.name}"


class PurchaseOrderItem(models.Model):
    po_item_id = models.AutoField(primary_key=True)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    # Open item from earlier: went with PROTECT to match SaleItem.product's
    # reasoning -- purchasing history should survive a product deletion too.
    # Flip to CASCADE if you decide that history doesn't need to stay queryable.
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='purchase_order_items')
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'purchase_order_item'
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity__gt=0), name="po_item_quantity_gt_0"),
            models.CheckConstraint(condition=models.Q(unit_cost__gte=0), name="po_item_unit_cost_gte_0"),
        ]

    def __str__(self):
        return f"{self.product.name} x{self.quantity} (PO#{self.po_id})"


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    # Open item from earlier: went with PROTECT, not CASCADE -- deleting a
    # product shouldn't silently discard a nonzero on-hand quantity.
    product = models.OneToOneField(Product, on_delete=models.PROTECT, related_name='inventory')
    quantity_on_hand = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)

    class Meta:
        db_table = 'inventory'
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity_on_hand__gte=0), name="inventory_qty_on_hand_gte_0"),
            models.CheckConstraint(condition=models.Q(reorder_level__gte=0), name="inventory_reorder_level_gte_0"),
        ]

    def __str__(self):
        return f"{self.product.name}: {self.quantity_on_hand} on hand"


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='sales')
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, related_name='sales', blank=True, null=True
    )
    sale_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'sale'
        constraints = [
            models.CheckConstraint(condition=models.Q(total_amount__gte=0), name="sale_total_amount_gte_0"),
        ]
        indexes = [
            models.Index(fields=['sale_date'], name='idx_sale_date'),
        ]

    def __str__(self):
        return f"Sale#{self.sale_id} - {self.sale_date:%Y-%m-%d}"


class SaleItem(models.Model):
    sale_item_id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sale_items')
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, related_name='sale_items', blank=True, null=True
    )
    quantity = models.IntegerField()
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'sale_item'
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity__gt=0), name="sale_item_quantity_gt_0"),
            models.CheckConstraint(condition=models.Q(line_total__gte=0), name="sale_item_line_total_gte_0"),
        ]

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"


class LoyaltyCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='loyalty_card')
    points_balance = models.IntegerField(default=0)
    # DateField, not DateTimeField 
    issued_date = models.DateField(default=timezone.localdate)

    class Meta:
        db_table = 'loyalty_card'
        constraints = [
            models.CheckConstraint(condition=models.Q(points_balance__gte=0), name="loyalty_points_balance_gte_0"),
        ]

    def __str__(self):
        return f"Loyalty#{self.card_id} - {self.customer}"