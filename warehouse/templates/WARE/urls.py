from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.test, name='new'),
    path('new1/', views.test2, name='new1'),
    path('add_item/', views.add_item, name='add_item'),
    path('order/', views.order_item, name='order'),
    path('add_catagory/', views.add_catagory, name='add_catagory'),
    path('orders/', views.OrdersView.as_view(), name='orders'), 
    path('items/', views.ItemListView.as_view(), name='items'),
    path('stocks/', views.stocks.as_view(), name='stocks'),
    path('test/', views.catView.as_view(), name='cat'),
    path('stock/', views.add_stock, name='stock'),
    path('registration/', views.register, name='register'),
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('MaterialRequest/', views.material_requests, name='MaterialRequest'),
    path('MaterialRequestview/', views.MaterialRequestview.as_view(), name='MaterialRequestview'),
    path('editstatus/<int:id>/', views.editstatus, name='editstatus'),


    path('order/edit/<int:order_id>/', views.edit, name='edit'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('item/edit/<int:order_id>/', views.item_edit, name='item_edit'),
    path('item/delete/<int:order_id>/', views.item_delete, name='item_delete'),
    path('stocks/edit/<int:order_id>/', views.stock_edit, name='stock_edit'),
    path('stocks/delete/<int:order_id>/', views.stock_delete, name='stock_delete'),
    path('catagory/edit/<int:order_id>/', views.catagory_edit, name='catagory_edit'),
    path('catagory/delete/<int:order_id>/', views.delete_catagory, name='delete_catagory'),

    path('users/', views.user_list, name='user_list'),
    #path('users/add/', views.user_add, name='user_add'),
    path('users/edit/<int:id>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:id>/', views.user_delete, name='user_delete'),
    
   
    path('inventory_report/', views.inventory_report, name='inventory_report'),
    path('order_history_report/', views.order_history_report, name='order_history_report'),
   
    
    # path('notifications/', views.notification_list, name='notifications'),
    # path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),


     path('mark_notification_as_read/', views.mark_notification_as_read, name='mark_notification_as_read'),
     path('fetch-notifications/', views.fetch_notifications, name='fetch_notifications'),
]
