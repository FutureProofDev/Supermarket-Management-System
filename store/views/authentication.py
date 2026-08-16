from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_not_required


@login_not_required
def login_view(request):
    '''
    Authenticates the user and starts their session.
    '''
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Determine role name for display message
            role = "Store Manager" if user.is_superuser else (
                user.groups.first().name if user.groups.exists() else "Staff"
            )
            messages.success(request, f"Welcome back, {user.username} ({role})!")

            # Safe redirect: return to requested URL if intercepted by login_required
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please verify your credentials.")
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'next': request.GET.get('next', ''),
        'title': 'Sign In - Essentials MS',
    }
    return render(request, 'store/auth/login.html', context)


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """
    Logs the user out and redirects to the login screen.
    """
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been successfully logged out.")
    return redirect('login')