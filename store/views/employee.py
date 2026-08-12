from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from ..models import Employee
from ..forms import EmployeeForm


def employee_list(request):
    employees = Employee.objects.all().order_by('last_name', 'first_name')
    return render(request, 'store/employee/employee_list.html', {'employees': employees})


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'store/employee/employee_detail.html', {'employee': employee})


def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee "{employee}" created.')
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    return render(request, 'store/employee/employee_form.html', {'form': form, 'title': 'Add Employee'})


def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee "{employee}" updated.')
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'store/employee/employee_form.html', {'form': form, 'title': 'Edit Employee'})


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        try:
            employee.delete()
        except ProtectedError:
            # Sale.employee is on_delete=PROTECT -- an employee with sales
            # history can't be silently deleted.
            messages.error(
                request,
                f'Can\'t delete "{employee}" — sales are still recorded under this employee.'
            )
            return redirect('employee_detail', pk=employee.pk)
        messages.success(request, f'Employee "{employee}" deleted.')
        return redirect('employee_list')
    return render(request, 'store/employee/employee_confirm_delete.html', {'employee': employee})