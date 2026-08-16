from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Customer
from ..forms import CustomerForm
from django.contrib.auth.decorators import permission_required
from django.db import connection


@permission_required('store.view_customer', raise_exception=True)
def customer_list(request):
    customers = Customer.objects.all().order_by('last_name', 'first_name')
    return render(request, 'store/customer/customer_list.html', {'customers': customers})


@permission_required('store.view_customer', raise_exception=True)
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    with connection.cursor() as cursor:
        cursor.callproc('sp_customer_order_history', [customer.pk])
        columns = [col[0] for col in cursor.description]
        order_history = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'store/customer/customer_detail.html', {
        'customer': customer,
        'order_history': order_history,
    })


@permission_required('store.add_customer', raise_exception=True)
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


@permission_required('store.change_customer', raise_exception=True)
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


@permission_required('store.delete_customer', raise_exception=True)
def customer_delete(request, pk):

    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, f'Customer "{customer}" deleted.')
        return redirect('customer_list')
    return render(request, 'store/customer/customer_confirm_delete.html', {'customer': customer})


