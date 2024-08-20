from django.shortcuts import get_object_or_404, render,redirect
from django.shortcuts import HttpResponse
from django.template import loader
from django_tables2 import SingleTableView
from .tables import ordertable, stocktable, itemtable, cattable
from .models import Item, Order, Stock, Category,Notification
from .forms import OrderForm, AddItemForm,catForm,stockform
from django.db.models import Q

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
    
        





