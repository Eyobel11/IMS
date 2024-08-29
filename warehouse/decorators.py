from django.contrib.auth.decorators import user_passes_test

def user_is_admin(user):
    return user.is_authenticated and user.user_type == 'Admin'

def user_is_manager(user):
    return user.is_authenticated and user.user_type == 'Manager'

def user_is_staff(user):
    return user.is_authenticated and user.user_type == 'Staff'

def admin_required(view_func):
    decorated_view_func = user_passes_test(user_is_admin, login_url='/')
    return decorated_view_func(view_func)

def manager_required(view_func):
    decorated_view_func = user_passes_test(user_is_manager, login_url='/')
    return decorated_view_func(view_func)

def staff_required(view_func):
    decorated_view_func = user_passes_test(user_is_staff, login_url='/')
    return decorated_view_func(view_func)
