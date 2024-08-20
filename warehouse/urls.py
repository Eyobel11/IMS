from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_item/', views.add_item, name='add_item'),
    path('order/', views.order_item, name='order'),
    path('add_catagory/', views.add_catagory, name='add_catagory'),
    path('orders/', views.OrdersView.as_view(), name='orders'), 
    path('items/', views.itemView.as_view(), name='items'),
    path('stocks/', views.stocks.as_view(), name='stocks'),
    path('test/', views.catView.as_view(), name='cat'),
    path('stock/', views.add_stock, name='stock'),
    path('order/edit/<int:order_id>/', views.edit, name='edit'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('item/edit/<int:order_id>/', views.item_edit, name='item_edit'),
    path('item/delete/<int:order_id>/', views.item_delete, name='item_delete'),
    path('stocks/edit/<int:order_id>/', views.stock_edit, name='stock_edit'),
    path('stocks/delete/<int:order_id>/', views.stock_delete, name='stock_delete'),
    path('catagory/edit/<int:order_id>/', views.catagory_edit, name='catagory_edit'),
    path('catagory/delete/<int:order_id>/', views.delete_catagory, name='delete_catagory'),
    path('notifications/', views.notification_list, name='notifications'),
    
    

]
