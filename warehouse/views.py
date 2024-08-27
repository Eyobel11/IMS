from django.shortcuts import get_object_or_404, render,redirect
from django.shortcuts import HttpResponse
from django.template import loader
from django_tables2 import SingleTableView
from .tables import ordertable, stocktable, itemtable, cattable
from .models import Item, Order, Stock, Category,Notification,User
from .forms import OrderForm, AddItemForm,catForm,stockform
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm
from .decorators import admin_required, manager_required, staff_required
from django.core.exceptions import PermissionDenied

def home(request):
    templates = loader.get_template('warehouse/home.html')

    return HttpResponse(templates.render({},request))

from django.shortcuts import render


def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items')  
          
    
    return render(request, 'warehouse/item.html', {'form': AddItemForm()})  

def item_edit(request, order_id):
    order = get_object_or_404(Item, pk=order_id)
    if request.method == 'POST':
        form = AddItemForm(request.POST, instance=order)  # Bind the form to the order instance
        if form.is_valid():
            form.save()
            return redirect('items')  # Redirect to the orders list after saving
    else:
        form = AddItemForm(instance=order)  # Load the form with the current order data
    
    return render(request, 'warehouse/edit_item.html', {'form': form})

def item_delete(request,order_id):
     
     order = get_object_or_404(Item, id=order_id)  # Get the specific order by ID
    
     if request.method == 'POST':
         order.delete()
         return redirect('items')  # Redirect to the orders list after deletion
     
     return render(request, 'warehouse/delete_item.html', {'order': order})



def order_item(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('orders')  
    else:
        form = OrderForm()
    
    return render(request, 'warehouse/order.html', {'form': form})


def edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Get the specific order by ID
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)  # Bind the form to the order instance
        if form.is_valid():
            form.save()
            return redirect('orders')  # Redirect to the orders list after saving
    else:
        form = OrderForm(instance=order)  # Load the form with the current order data
    
    return render(request, 'warehouse/edit_order.html', {'form': form})

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Get the specific order by ID
    
    if request.method == 'POST':
        order.delete()
        return redirect('orders')  # Redirect to the orders list after deletion
    
    return render(request, 'warehouse/delete_order.html', {'order': order})




def add_stock(request):
    if request.method == 'POST':
        form = stockform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stocks') 
   
    return render(request, 'warehouse/stock.html', {'form': stockform()})


def stock_edit(request,order_id):

    order = get_object_or_404(Stock, id=order_id)  # Get the specific order by ID
    
    if request.method == 'POST':
        form = stockform(request.POST, instance=order)  # Bind the form to the order instance
        if form.is_valid():
            form.save()
            return redirect('stocks')  # Redirect to the orders list after saving
    else:
        form = stockform(instance=order)  # Load the form with the current order data
    
    return render(request, 'warehouse/edit_stock.html', {'form': form})

def stock_delete(request,order_id):
    
     order = get_object_or_404(Stock, id=order_id)  # Get the specific order by ID
    
     if request.method == 'POST':
        order.delete()
        return redirect('stocks')  # Redirect to the orders list after deletion
    
     return render(request, 'warehouse/delete_stock.html', {'order': order})

    

def add_catagory(request):
    if request.method == 'POST':
        form = catForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cat')  
          
    
    return render(request, 'warehouse/add_catagory.html', {'form': catForm()})  

def catagory_edit(request, order_id):
    
    order = get_object_or_404(Category, id=order_id)  # Get the specific order by ID
    
    if request.method == 'POST':
        form = catForm(request.POST, instance=order)  # Bind the form to the order instance
        if form.is_valid():
            form.save()
            return redirect('cat')  # Redirect to the orders list after saving
    else:
        form = catForm(instance=order)  # Load the form with the current order data
    
    return render(request, 'warehouse/edit_catagory.html', {'form': form})

def delete_catagory(request,order_id):

     order = get_object_or_404(Category, id=order_id)  # Get the specific order by ID
    
     if request.method == 'POST':
        order.delete()
        return redirect('cat')  # Redirect to the orders list after deletion
    
     return render(request, 'warehouse/delete_catagory.html', {'order': order})

def notification_list(request):
    notifications = request.user.notifications.filter(is_read=False)
    return render(request, 'warehouse/notifications.html', {'notifications': notifications})
# views.py

def notification_list(request):
    notifications = request.user.notifications.filter(is_read=False)
    notifications.update(is_read=True)
    return render(request, 'warehouse/notifications.html', {'notifications': notifications})




     



class OrdersView(SingleTableView):
    model = Order
    table_class = ordertable
    template_name = 'warehouse/orders.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(item__name__icontains=query) | 
                Q(quantity__icontains=query) | 
                Q(status__icontains=query)
            )
        return queryset

class stocks(SingleTableView):
    model = Stock
    table_class = stocktable
    template_name = 'warehouse/stocks.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(stock_no__icontains=query) |  # Filter by stock number
                Q(description__icontains=query) |  # Filter by description
                Q(category__name__icontains=query) |  # Filter by category
                Q(current_level__icontains=query)  # Filter by current stock level (assuming it's a string)
       
            )
        return queryset
   

class itemView(SingleTableView):
    model = Item
    table_class = itemtable
    template_name = 'warehouse/items.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) | 
                Q(stock__stock_no__icontains=query)
            )
        return queryset


class catView(SingleTableView):
    model = Category
    table_class = cattable
    template_name = 'warehouse/test.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) 
        
            )
        return queryset
    
    #### register and login and logout
    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'warehouse/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'warehouse/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


############# edit the user  forget the user_add for now

def user_list(request):
    users = User.objects.all()
    return render(request, 'warehouse/user_list.html', {'users': users})

def user_add(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'warehouse/user_form.html', {'form': form, 'form_title': 'Add User'})

def user_edit(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('warehouse/user_list')
        else:
            # Print errors to the console for debugging
            print(form.errors)
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, 'warehouse/user_form.html', {'form': form, 'form_title': 'Edit User'})


def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'warehouse/delete_user.html', {'user': user})

################################ this is for the roles



@admin_required
def admin_view(request):
    # Logic for admin-only view
    return render(request, 'admin_page.html')

@manager_required
def manager_view(request):
    # Logic for manager-only view
    return render(request, 'manager_page.html')

@staff_required
def staff_view(request):
    # Logic for staff-only view
    return render(request, 'staff_page.html')

def user_is_admin(user):
    if user.is_authenticated and user.user_type == 'admin':
        return True
    raise PermissionDenied

def user_is_manager(user):
    if user.is_authenticated and user.user_type == 'manager':
        return True
    raise PermissionDenied

def user_is_staff(user):
    if user.is_authenticated and user.user_type == 'staff':
        return True
    raise PermissionDenied


