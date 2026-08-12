from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Customer
from ..forms import CustomerForm


def customer_list(request):
    customers = Customer.objects.all().order_by('last_name', 'first_name')
    return render(request, 'store/customer/customer_list.html', {'customers': customers})


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'store/customer/customer_detail.html', {'customer': customer})


def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer "{customer}" created.')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    return render(request, 'store/customer/customer_form.html', {'form': form, 'title': 'Add Customer'})


def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer "{customer}" updated.')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'store/customer/customer_form.html', {'form': form, 'title': 'Edit Customer'})


def customer_delete(request, pk):
    # Note: no try/except ProtectedError needed here -- Sale.customer is
    # SET_NULL and LoyaltyCard.customer is CASCADE. Deleting a customer
    # never raises ProtectedError; it just nulls out their sales and
    # deletes their loyalty card automatically.
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, f'Customer "{customer}" deleted.')
        return redirect('customer_list')
    return render(request, 'store/customer/customer_confirm_delete.html', {'customer': customer})