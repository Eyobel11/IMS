from django.shortcuts import get_object_or_404, render,redirect
from django.shortcuts import HttpResponse
from django.template import loader
from django_tables2 import SingleTableView
from .tables import ordertable, stocktable, itemtable, cattable,MaterialRequesttable
from .models import Item, Order, Stock, Category,Notification,User,MaterialRequest
from .forms import OrderForm, AddItemForm,catForm,stockform,EditmaterialrequestForm,materialrequestForm
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm,UserEditForm
from .decorators import admin_required, manager_required, staff_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

#home view

@login_required

def home(request):
    
    templates = loader.get_template('WARE/home.html')
    return HttpResponse(templates.render({},request))

def permission(request):
       templates = loader.get_template('WARE/403.html')
       return HttpResponse(templates.render({},request))

#item management views

@staff_required

def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items')  
          
    
    return render(request, 'WARE/item.html', {'form': AddItemForm()})  

@staff_required

def item_edit(request, order_id):
    order = get_object_or_404(Item, pk=order_id)
    success = False
    if request.method == 'POST':
        form = AddItemForm(request.POST, instance=order)  # Bind the form to the order instance
        if form.is_valid():
            form.save()
            success = True
            # return redirect('items')  # Redirect to the orders list after saving
    else:
        form = AddItemForm(instance=order)  # Load the form with the current order data
    
    return render(request, 'WARE/edit_item.html', {'form': form,'success':success})

@staff_required

def item_delete(request,order_id):
     
     order = get_object_or_404(Item, id=order_id)  # Get the specific order by ID
     success = False
     if request.method == 'POST':
         order.delete()
         success = True

        #  return redirect('items')  # Redirect to the orders list after deletion
     
     return render(request, 'WARE/delete_item.html', {'order': order,'success':success})

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
    
    return render(request, 'WARE/order.html', {'form': form})

@manager_required

def edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Get the specific order by ID
    success = False
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)  # Bind the form to the order instance
        if form.is_valid():
            form.save()
            success = True
            # return redirect('orders')  # Redirect to the orders list after saving
    else:
        form = OrderForm(instance=order)  # Load the form with the current order data
    
    return render(request, 'WARE/edit_order.html', {'form': form, 'success':success})

@manager_required

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Get the specific order by ID
    success = False
    if request.method == 'POST':
        order.delete()
        success = True
        # return redirect('orders')  # Redirect to the orders list after deletion
    
    return render(request, 'WARE/delete_order.html', {'order': order, 'success':success})


#stock management views


@manager_required

def add_stock(request):
    if request.method == 'POST':
        form = stockform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stocks') 
   
    return render(request, 'WARE/stock.html', {'form': stockform()})

@manager_required

def stock_edit(request,order_id):

    order = get_object_or_404(Stock, id=order_id)  # Get the specific order by ID
    success = False
    
    if request.method == 'POST':
        form = stockform(request.POST, instance=order)  # Bind the form to the order instance
        if form.is_valid():
            form.save()
            success = True
            # return redirect('stocks')  # Redirect to the orders list after saving
    else:
        form = stockform(instance=order)  # Load the form with the current order data
    
    return render(request, 'WARE/edit_stock.html', {'form': form,'success':success})

@manager_required

def stock_delete(request,order_id):
    
     order = get_object_or_404(Stock, id=order_id)  # Get the specific order by ID
     success = False

     if request.method == 'POST':
        order.delete()
        success = True
        # return redirect('stocks')  # Redirect to the orders list after deletion
    
     return render(request, 'WARE/delete_stock.html', {'order': order,'success':success})

    
# category management views

@admin_required

def add_catagory(request):
    if request.method == 'POST':
        form = catForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cat')  
          
    
    return render(request, 'WARE/add_catagory.html', {'form': catForm()})  

@manager_required

def catagory_edit(request, order_id):
    
    order = get_object_or_404(Category, id=order_id)  # Get the specific order by ID
    success = False
    if request.method == 'POST':
        form = catForm(request.POST, instance=order)  # Bind the form to the order instance
        if form.is_valid():
            form.save()
            success = True
            # return redirect('cat')  # Redirect to the orders list after saving
    else:
        form = catForm(instance=order)  # Load the form with the current order data
    
    return render(request, 'WARE/edit_catagory.html', {'form': form,'success':success})

@manager_required

def delete_catagory(request,order_id):

     order = get_object_or_404(Category, id=order_id)  # Get the specific order by ID
     success= False
     if request.method == 'POST':
        order.delete()
        success= True
        # return redirect('cat')  # Redirect to the orders list after deletion
    
     return render(request, 'WARE/delete_catagory.html', {'order': order,'success':success})

# @login_required

# def notification_list(request):
#     notifications = request.user.notifications.filter(is_read=False).order_by('-created_at')
#     return render(request, 'WARE/notifications.html', {'notifications': notifications})

# # @login_required

# def mark_as_read(request, notification_id):
#     notification = Notification.objects.get(id=notification_id, user=request.user)
#     notification.is_read = True
#     notification.save()
#     return redirect('notifications')



     



class OrdersView(SingleTableView):
    model = Order
    table_class = ordertable
    template_name = 'WARE/orders.html'

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
    template_name = 'WARE/stocks.html'
    
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
    template_name = 'WARE/items.html'
    
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
    template_name = 'WARE/test.html'
    
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
    return render(request, 'WARE/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'WARE/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


############# edit the user  forget the user_add for now

#user management views

@admin_required

def user_list(request):
    users = User.objects.all()
    return render(request, 'WARE/user_list.html', {'users': users})

@admin_required

# def user_add(request):

#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'WARE/user_form.html', {'form': form, 'form_title': 'Add User'})

@admin_required
def user_edit(request, id):
    user = get_object_or_404(User, id=id)  # Fetch the user to edit
    success = False
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)  # Use UserEditForm
        if form.is_valid():
            form.save()
            success = True  # Success flag
            
        else:
            # Print errors to the console for debugging
            print(form.errors)
    else:
        form = UserEditForm(instance=user)  # Use UserEditForm for GET requests
    return render(request, 'WARE/user_form.html', {'form': form, 'form_title': 'Edit User', 'success': success})


@admin_required

def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    success= False
    if request.method == 'POST':
        user.delete()
        success = True # Success flag
    return render(request, 'WARE/delete_user.html', {'user': user,'success': success})

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

    return render(request, 'WARE/materialrequest.html', {'form': form})

def MaterialRequests(request):
    if request.method == 'POST':
        form = materialrequestForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('MaterialRequestview')  
    else:
        form = materialrequestForm()
    
    return render(request, 'WARE/MaterialRequest.html', {'form': form})

class MaterialRequestview(SingleTableView):
    
    model = MaterialRequest
    table_class = MaterialRequesttable
    template_name = 'WARE/material_request_list.html'

    def get_queryset(self):
        return super().get_queryset().order_by('-request_date')
    


@manager_required

def editstatus(request, id):
    # Retrieve the material request object or return a 404 error if not found
    material_request = get_object_or_404(MaterialRequest, id=id)
    success = False

    if request.method == 'POST':
        # Initialize the form with POST data and the instance to be updated
        form = EditmaterialrequestForm(request.POST, instance=material_request)
        if form.is_valid():
            form.save()
            # Redirect to the material request list view or another relevant view
            success = True
            # return redirect('MaterialRequestview')  # Ensure this URL name matches your URL pattern
    else:
        # Initialize the form with the instance to be edited for GET requests
        form = EditmaterialrequestForm(instance=material_request)
    
    # Render the template with the form
    return render(request, 'WARE/editrequest.html', {'form': form,'success': success})


