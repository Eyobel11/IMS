from django.shortcuts import get_object_or_404, render,redirect
from django.shortcuts import HttpResponse
from django.template import loader
from django_tables2 import SingleTableView
from .tables import ordertable, stocktable, itemtable, cattable,MaterialRequesttable
from .models import Item, Order, Stock, Category,Notification,User,MaterialRequest
from .forms import OrderForm, AddItemForm,catForm,stockform,EditmaterialrequestForm,materialrequestForm
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm
from .decorators import admin_required, manager_required, staff_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

#home view

def home(request):
    
    templates = loader.get_template('warehouse/home.html')
    return HttpResponse(templates.render({},request))

def permission(request):
       templates = loader.get_template('warehouse/403.html')
       return HttpResponse(templates.render({},request))

#item management views

@staff_required

def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items')  
          
    
    return render(request, 'warehouse/item.html', {'form': AddItemForm()})  

@staff_required

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

@staff_required

def item_delete(request,order_id):
     
     order = get_object_or_404(Item, id=order_id)  # Get the specific order by ID
    
     if request.method == 'POST':
         order.delete()
         return redirect('items')  # Redirect to the orders list after deletion
     
     return render(request, 'warehouse/delete_item.html', {'order': order})

#order managment views

@manager_required

def order_item(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('orders')  
    else:
        form = OrderForm()
    
    return render(request, 'warehouse/order.html', {'form': form})

@manager_required

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

@manager_required

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Get the specific order by ID
    
    if request.method == 'POST':
        order.delete()
        return redirect('orders')  # Redirect to the orders list after deletion
    
    return render(request, 'warehouse/delete_order.html', {'order': order})


#stock management views


@manager_required

def add_stock(request):
    if request.method == 'POST':
        form = stockform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stocks') 
   
    return render(request, 'warehouse/stock.html', {'form': stockform()})

@manager_required

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

@manager_required

def stock_delete(request,order_id):
    
     order = get_object_or_404(Stock, id=order_id)  # Get the specific order by ID
    
     if request.method == 'POST':
        order.delete()
        return redirect('stocks')  # Redirect to the orders list after deletion
    
     return render(request, 'warehouse/delete_stock.html', {'order': order})

    
# category management views

@admin_required

def add_catagory(request):
    if request.method == 'POST':
        form = catForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cat')  
          
    
    return render(request, 'warehouse/add_catagory.html', {'form': catForm()})  

@manager_required

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

@manager_required

def delete_catagory(request,order_id):

     order = get_object_or_404(Category, id=order_id)  # Get the specific order by ID
    
     if request.method == 'POST':
        order.delete()
        return redirect('cat')  # Redirect to the orders list after deletion
    
     return render(request, 'warehouse/delete_catagory.html', {'order': order})

# @login_required

# def notification_list(request):
#     notifications = request.user.notifications.filter(is_read=False).order_by('-created_at')
#     return render(request, 'warehouse/notifications.html', {'notifications': notifications})

# # @login_required

# def mark_as_read(request, notification_id):
#     notification = Notification.objects.get(id=notification_id, user=request.user)
#     notification.is_read = True
#     notification.save()
#     return redirect('notifications')



     



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

#user management views

@admin_required

def user_list(request):
    users = User.objects.all()
    return render(request, 'warehouse/user_list.html', {'users': users})

@admin_required

def user_add(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'warehouse/user_form.html', {'form': form, 'form_title': 'Add User'})

@admin_required

def user_edit(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            # Print errors to the console for debugging
            print(form.errors)
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, 'warehouse/user_form.html', {'form': form, 'form_title': 'Edit User'})

@admin_required

def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'warehouse/delete_user.html', {'user': user})

################################ this is for the roles





#### report 

# @staff_required

@admin_required

def inventory_report(request):
    stocks = Stock.objects.all()
    return render(request, 'warehouse/inventory_report.html', {'stocks': stocks})

@admin_required

def order_history_report(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'warehouse/order_history_report.html', {'orders': orders})


from django.http import JsonResponse

def fetch_notifications(request):
    notifications = Notification.objects.filter(read=False,user=request.user)  # Adjust the queryset as needed
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'id': notification.id,
            'message': notification.message,
            'notification_date': notification.notification_date.strftime('%Y-%m-%d'),
            'read': notification.read,
        })
    return JsonResponse({'notifications': notifications_data})


@csrf_exempt 

def mark_notification_as_read(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.read = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


########## materials #####
@staff_required

def material_requests(request):
    if request.method == 'POST':
        form = materialrequestForm(request.POST)
        if form.is_valid():
            material_request = form.save(commit=False)
            material_request.user = request.user  # Assign the current user to the request
            material_request.save()

           # messages.success(request, 'Material request submitted successfully!')
            return redirect('MaterialRequestview')  # Ensure this URL name matches your URL pattern
    else:
        form = materialrequestForm()

    return render(request, 'warehouse/MaterialRequest.html', {'form': form})

def MaterialRequests(request):
    if request.method == 'POST':
        form = materialrequestForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('MaterialRequestview')  
    else:
        form = materialrequestForm()
    
    return render(request, 'warehouse/MaterialRequest.html', {'form': form})

class MaterialRequestview(SingleTableView):
    
    model = MaterialRequest
    table_class = MaterialRequesttable
    template_name = 'warehouse/material_request_list.html'

    def get_queryset(self):
        return super().get_queryset().order_by('-request_date')
    


@manager_required

def editstatus(request, id):
    # Retrieve the material request object or return a 404 error if not found
    material_request = get_object_or_404(MaterialRequest, id=id)
    
    if request.method == 'POST':
        # Initialize the form with POST data and the instance to be updated
        form = EditmaterialrequestForm(request.POST, instance=material_request)
        if form.is_valid():
            form.save()
            # Redirect to the material request list view or another relevant view
            return redirect('MaterialRequestview')  # Ensure this URL name matches your URL pattern
    else:
        # Initialize the form with the instance to be edited for GET requests
        form = EditmaterialrequestForm(instance=material_request)
    
    # Render the template with the form
    return render(request, 'warehouse/materialrequest.html', {'form': form})


