from decimal import Decimal
from collections import defaultdict
import json

from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from ..forms import SaleHeaderForm, SaleLineFormSet
from ..models import Employee, Inventory, Sale, SaleItem, Product, Discount

LOYALTY_THRESHOLD = Decimal('1000.00')
LOYALTY_DISCOUNT_RATE = Decimal('0.15')
EXPIRY_DISCOUNT_RATE = Decimal('0.50')


@login_required
def sale_list(request):
    sales = Sale.objects.select_related('employee', 'customer').order_by('-sale_date')
    return render(request, 'store/sale/sale_list.html', {'sales': sales})


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale.objects.select_related('employee', 'customer'), pk=pk)
    items = sale.items.select_related('product', 'discount')
    
    # Retrieve previous stock levels stored in session for the demo confirmation view
    stock_audit = request.session.pop(f'sale_{sale.sale_id}_stock_audit', None)
    
    return render(request, 'store/sale/sale_detail.html', {
        'sale': sale,
        'items': items,
        'stock_audit': stock_audit
    })


@login_required
def checkout(request):
    # Derive active employee from logged-in user
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        employee = Employee.objects.filter(email__iexact=request.user.email).first() or Employee.objects.first()

    if not employee:
        messages.error(request, "No active Employee profile linked to this user account.")
        return redirect('home')

    if request.method == 'POST':
        header_form = SaleHeaderForm(request.POST)
        formset = SaleLineFormSet(request.POST)

        if header_form.is_valid() and formset.is_valid():
            # Combine duplicate line products
            combined = defaultdict(int)
            for form in formset.cleaned_data:
                product = form.get('product')
                quantity = form.get('quantity')
                if product and quantity:
                    combined[product] += quantity

            lines = list(combined.items())

            if not lines:
                messages.error(request, "Please add at least one product with a valid quantity.")
            else:
                try:
                    with transaction.atomic():
                        promo_discount = header_form.cleaned_data.get('discount')
                        promo_rate = (promo_discount.percent_off / Decimal('100.00')) if promo_discount else Decimal('0.00')

                        subtotal = Decimal('0.00')
                        prepared_items = []
                        stock_audit = []

                        for product, quantity in lines:
                            # Row-level lock to prevent concurrent stock overdrafts
                            inventory = Inventory.objects.select_for_update().filter(product=product).first()

                            if not inventory:
                                raise ValueError(f'No inventory record exists for "{product.name}".')

                            if inventory.quantity_on_hand < quantity:
                                raise ValueError(
                                    f'Insufficient stock for "{product.name}" '
                                    f'(Available: {inventory.quantity_on_hand}, Requested: {quantity}).'
                                )

                            unit_price = Decimal(str(product.unit_price))
                            base_line_total = unit_price * quantity

                            # Determine applicable line discounts (Near-expiry 50% OR Promotional campaign)
                            active_discount_applied = None
                            if product.is_near_expiry():
                                line_price = base_line_total * (Decimal('1.00') - EXPIRY_DISCOUNT_RATE)
                            elif promo_discount:
                                line_price = base_line_total * (Decimal('1.00') - promo_rate)
                                active_discount_applied = promo_discount
                            else:
                                line_price = base_line_total

                            subtotal += line_price

                            stock_audit.append({
                                'product_name': product.name,
                                'old_stock': inventory.quantity_on_hand,
                                'deducted': quantity,
                                'new_stock': inventory.quantity_on_hand - quantity
                            })

                            prepared_items.append({
                                'product': product,
                                'inventory': inventory,
                                'quantity': quantity,
                                'line_total': round(line_price, 2),
                                'discount': active_discount_applied
                            })

                        # Apply Loyalty bulk volume discount if subtotal exceeds threshold
                        loyalty_applied = subtotal > LOYALTY_THRESHOLD
                        total_amount = subtotal * (Decimal('1.00') - LOYALTY_DISCOUNT_RATE) if loyalty_applied else subtotal
                        total_amount = round(total_amount, 2)

                        customer = header_form.cleaned_data.get('customer')

                        # 1. Insert Parent Sale Transaction
                        sale = Sale.objects.create(
                            employee=employee,
                            customer=customer,
                            sale_date=timezone.now(),
                            total_amount=total_amount,
                        )

                        # 2. Insert Line Items & Deduct Inventory On-Hand
                        for item in prepared_items:
                            SaleItem.objects.create(
                                sale=sale,
                                product=item['product'],
                                discount=item['discount'],
                                quantity=item['quantity'],
                                line_total=item['line_total'],
                            )
                            item['inventory'].quantity_on_hand = F('quantity_on_hand') - item['quantity']
                            item['inventory'].save(update_fields=['quantity_on_hand'])

                        # 3. Add Customer Loyalty Points (1 point per GHS 10 spent)
                        if customer and hasattr(customer, 'loyalty_card'):
                            points_earned = int(total_amount // 10)
                            if points_earned > 0:
                                customer.loyalty_card.points_balance = F('points_balance') + points_earned
                                customer.loyalty_card.save(update_fields=['points_balance'])

                    # Store stock deduction audit in session for immediate receipt display
                    request.session[f'sale_{sale.sale_id}_stock_audit'] = stock_audit

                    messages.success(request, f"Sale #{sale.sale_id} finalized! Total: GHS {total_amount:.2f}")
                    return redirect('sale_detail', pk=sale.sale_id)

                except ValueError as exc:
                    messages.error(request, str(exc))
                except Exception as exc:
                    messages.error(request, f"Database transaction failed: {exc}")
    else:
        header_form = SaleHeaderForm()
        formset = SaleLineFormSet()

    # Pass live product catalog metadata into template for instant JS pricing calculations
    product_data = {}
    for p in Product.objects.select_related('inventory').all():
        product_data[str(p.pk)] = {
            'price': float(p.unit_price),
            'stock': p.inventory.quantity_on_hand if hasattr(p, 'inventory') else 0,
            'is_near_expiry': p.is_near_expiry()
        }

    # Pass active discount percentages
    discount_data = {}
    for d in Discount.objects.all():
        discount_data[str(d.pk)] = float(d.percent_off)

    return render(request, 'store/sale/checkout.html', {
        'header_form': header_form,
        'formset': formset,
        'employee': employee,
        'product_data_json': json.dumps(product_data),
        'discount_data_json': json.dumps(discount_data),
    })