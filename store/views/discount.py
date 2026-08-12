from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from ..models import Discount
from ..forms import DiscountForm


def discount_list(request):
    discounts = Discount.objects.all().order_by('-start_date')
    return render(request, 'store/discount/discount_list.html', {'discounts': discounts})


def discount_detail(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    return render(request, 'store/discount/discount_detail.html', {'discount': discount})


def discount_create(request):
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount = form.save()
            messages.success(request, f'Discount "{discount.name}" created.')
            return redirect('discount_detail', pk=discount.pk)
    else:
        form = DiscountForm()
    return render(request, 'store/discount/discount_form.html', {'form': form, 'title': 'Add Discount'})


def discount_update(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    if request.method == 'POST':
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            messages.success(request, f'Discount "{discount.name}" updated.')
            return redirect('discount_detail', pk=discount.pk)
    else:
        form = DiscountForm(instance=discount)
    return render(request, 'store/discount/discount_form.html', {'form': form, 'title': 'Edit Discount'})


def discount_delete(request, pk):
    # SaleItem.discount is SET_NULL -- deleting a discount never raises
    # ProtectedError, it just nulls the discount on past sale items.
    discount = get_object_or_404(Discount, pk=pk)
    if request.method == 'POST':
        discount.delete()
        messages.success(request, f'Discount "{discount.name}" deleted.')
        return redirect('discount_list')
    return render(request, 'store/discount/discount_confirm_delete.html', {'discount': discount})