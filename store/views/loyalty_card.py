from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import LoyaltyCard
from ..forms import LoyaltyCardForm
from django.contrib.auth.decorators import permission_required


@permission_required('store.view_loyaltycard', raise_exception=True)
def loyaltycard_list(request):
    cards = LoyaltyCard.objects.select_related('customer').order_by('customer__last_name')
    return render(request, 'store/loyalty_card/loyaltycard_list.html', {'cards': cards})


@permission_required('store.view_loyaltycard', raise_exception=True)
def loyaltycard_detail(request, pk):
    card = get_object_or_404(LoyaltyCard, pk=pk)
    return render(request, 'store/loyalty_card/loyaltycard_detail.html', {'card': card})


@permission_required('store.add_loyaltycard', raise_exception=True)
def loyaltycard_create(request):
    if request.method == 'POST':
        form = LoyaltyCardForm(request.POST)
        if form.is_valid():
            card = form.save()
            messages.success(request, f'Loyalty card for "{card.customer}" created.')
            return redirect('loyaltycard_detail', pk=card.pk)
    else:
        form = LoyaltyCardForm()
    return render(request, 'store/loyalty_card/loyaltycard_form.html', {'form': form, 'title': 'Add Loyalty Card'})


@permission_required('store.change_loyaltycard', raise_exception=True)
def loyaltycard_update(request, pk):
    card = get_object_or_404(LoyaltyCard, pk=pk)
    if request.method == 'POST':
        form = LoyaltyCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, f'Loyalty card for "{card.customer}" updated.')
            return redirect('loyaltycard_detail', pk=card.pk)
    else:
        form = LoyaltyCardForm(instance=card)
    return render(request, 'store/loyalty_card/loyaltycard_form.html', {'form': form, 'title': 'Edit Loyalty Card'})


@permission_required('store.delete_loyaltycard', raise_exception=True)
def loyaltycard_delete(request, pk):
    # No incoming FKs point to LoyaltyCard itself, so no ProtectedError possible.
    card = get_object_or_404(LoyaltyCard, pk=pk)
    if request.method == 'POST':
        customer_name = str(card.customer)
        card.delete()
        messages.success(request, f'Loyalty card for "{customer_name}" deleted.')
        return redirect('loyaltycard_list')
    return render(request, 'store/loyalty_card/loyaltycard_confirm_delete.html', {'card': card})