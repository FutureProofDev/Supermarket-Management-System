from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from matplotlib import lines
from django.contrib.auth.decorators import permission_required

from ..forms import SaleHeaderForm, SaleLineFormSet
from ..models import Inventory, Sale, SaleItem

from collections import defaultdict

LOYALTY_THRESHOLD = Decimal('1000.00')
LOYALTY_DISCOUNT_RATE = Decimal('0.15')
EXPIRY_DISCOUNT_RATE = Decimal('0.50')


@permission_required('store.add_sale', raise_exception=True)
def checkout(request):
    ...

def sale_list(request):
    sales = Sale.objects.select_related('employee', 'customer').order_by('-sale_date')
    return render(request, 'store/sale/sale_list.html', {'sales': sales})


def sale_detail(request, pk):
    sale = get_object_or_404(Sale.objects.select_related('employee', 'customer'), pk=pk)
    items = sale.items.select_related('product', 'discount')
    return render(request, 'store/sale/sale_detail.html', {'sale': sale, 'items': items})

    
@permission_required('store.add_sale', raise_exception=True)
def checkout(request):
    if request.method == 'POST':
        header_form = SaleHeaderForm(request.POST)
        formset = SaleLineFormSet(request.POST)

        if header_form.is_valid() and formset.is_valid():
            raw_lines = [
                (line['product'], line['quantity'])
                for line in formset.cleaned_data
                if line.get('product') and line.get('quantity')
            ]

            combined = defaultdict(int)
            for product, quantity in raw_lines:
                combined[product] += quantity
            lines = list(combined.items())

            if not lines:
                messages.error(request, 'Add at least one product to the sale.')
            else:
                try:
                    with transaction.atomic():
                        subtotal = Decimal('0.00')
                        prepared_items = []

                        for product, quantity in lines:
                            # select_for_update locks the row so two simultaneous
                            # checkouts can't both read the same stale stock count.
                            inventory = Inventory.objects.select_for_update().get(product=product)

                            if inventory.quantity_on_hand < quantity:
                                raise ValueError(
                                    f'Not enough stock for "{product.name}" '
                                    f'(have {inventory.quantity_on_hand}, need {quantity}).'
                                )

                            line_price = product.unit_price * quantity
                            if product.is_near_expiry():
                                line_price *= (1 - EXPIRY_DISCOUNT_RATE)

                            subtotal += line_price
                            prepared_items.append(
                                {'product': product, 'inventory': inventory,
                                 'quantity': quantity, 'line_total': line_price}
                            )

                        loyalty_applied = subtotal > LOYALTY_THRESHOLD
                        total_amount = subtotal * (1 - LOYALTY_DISCOUNT_RATE) if loyalty_applied else subtotal

                        sale = Sale.objects.create(
                            employee=header_form.cleaned_data['employee'],
                            customer=header_form.cleaned_data.get('customer'),
                            sale_date=timezone.now(),
                            total_amount=total_amount,
                        )

                        for item in prepared_items:
                            SaleItem.objects.create(
                                sale=sale,
                                product=item['product'],
                                quantity=item['quantity'],
                                line_total=item['line_total'],
                            )
                            item['inventory'].quantity_on_hand = F('quantity_on_hand') - item['quantity']
                            item['inventory'].save(update_fields=['quantity_on_hand'])

                    messages.success(
                        request,
                        f'Sale #{sale.sale_id} completed — GH₵{total_amount:.2f}'
                        + (' (loyalty discount applied)' if loyalty_applied else '')
                    )
                    return redirect('sale_detail', pk=sale.sale_id)

                except ValueError as exc:
                    messages.error(request, str(exc))
    else:
        header_form = SaleHeaderForm()
        formset = SaleLineFormSet()

    return render(request, 'store/sale/checkout.html', {
        'header_form': header_form,
        'formset': formset,
    })