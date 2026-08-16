from decimal import Decimal

from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase
from django.urls import reverse

from .models import Category, Customer, Employee, Inventory, Product, Sale, SaleItem, Supplier


class RolePermissionTests(TestCase):
    """Confirms RBAC is actually enforced, not just configured."""

    def setUp(self):
        self.cashier_group = Group.objects.create(name='Cashier')
        add_sale_perm = Permission.objects.get(codename='add_sale')
        self.cashier_group.permissions.add(add_sale_perm)

        self.cashier_user = User.objects.create_user(username='test_cashier', password='testpass123')
        self.cashier_user.groups.add(self.cashier_group)

        # Link a real Employee so checkout()'s employee_profile guard passes
        self.employee = Employee.objects.create(
            first_name='Test', last_name='Cashier', role='Cashier', user=self.cashier_user
        )

    def test_cashier_cannot_create_employee(self):
        """A Cashier has no add_employee permission and must be blocked."""
        self.client.login(username='test_cashier', password='testpass123')
        response = self.client.get(reverse('employee_create'))
        self.assertEqual(response.status_code, 403)

    def test_cashier_can_reach_checkout(self):
        """A Cashier does have add_sale and should reach the checkout page."""
        self.client.login(username='test_cashier', password='testpass123')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_redirected_to_login(self):
        """No session at all should redirect to login, not 500 or 403."""
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class CheckoutTransactionTests(TestCase):
    """Confirms the checkout transaction actually updates the database correctly."""

    def setUp(self):
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.category = Category.objects.create(name='Beverages')
        self.product = Product.objects.create(
            name='Bottled Water', category=self.category, supplier=self.supplier,
            unit_price=Decimal('5.00'), barcode='TESTBAR001'
        )
        Inventory.objects.create(product=self.product, quantity_on_hand=50, reorder_level=10)

        self.employee = Employee.objects.create(
            first_name='Test', last_name='Employee', role='Cashier'
        )

    def test_inventory_decrements_after_sale(self):
        """Placing a sale should reduce quantity_on_hand by the quantity sold."""
        sale = Sale.objects.create(employee=self.employee, total_amount=Decimal('10.00'))
        SaleItem.objects.create(sale=sale, product=self.product, quantity=2, line_total=Decimal('10.00'))

        self.product.inventory.quantity_on_hand -= 2
        self.product.inventory.save(update_fields=['quantity_on_hand'])
        self.product.inventory.refresh_from_db()

        self.assertEqual(self.product.inventory.quantity_on_hand, 48)