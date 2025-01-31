from django.shortcuts import redirect
from django.contrib import messages
from django.utils.http import urlencode

def user_is_admin(user):
    return user.is_authenticated and user.user_type == 'Admin'

def user_is_manager(user):
    return user.is_authenticated and user.user_type == 'Manager'

def user_is_staff(user):
    return user.is_authenticated and user.user_type == 'Staff'

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not user_is_admin(request.user):
            error_message = urlencode({'accessDenied': 'You do not have permission to perform this action.'})
            return redirect(f"/?{error_message}")
        return view_func(request, *args, **kwargs)
    return wrapper

def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not user_is_manager(request.user):
            error_message = urlencode({'accessDenied': 'You do not have permission to perform this action.'})
            return redirect(f"/?{error_message}")
        return view_func(request, *args, **kwargs)
    return wrapper

def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not user_is_staff(request.user):
            error_message = urlencode({'accessDenied': 'You do not have permission to perform this action.'})
            return redirect(f"/?{error_message}")
        return view_func(request, *args, **kwargs)
    return wrapper
