import django_tables2 as tables
from django.urls import reverse
from .models import Order, Stock, Category,Item,MaterialRequest


class ordertable(tables.Table):
    edit_link = tables.LinkColumn(
        viewname='edit',  
        args=[tables.A('pk')], 
        text='edit',  
        empty_values=(),  
    )
    delete_link = tables.LinkColumn(
        viewname='delete_order',  
        args=[tables.A('pk')], 
        text='delete',  
        empty_values=(),  
    )
    class Meta:
        model= Order
        template_name = "django_tables2/bootstrap.html"
        fields = ("item","quantity","status","order_date","edit_link","delete_link" )

class stocktable(tables.Table):
    edit_link = tables.LinkColumn(
        viewname='stock_edit',  
        args=[tables.A('pk')], 
        text='edit',  
        empty_values=(),  
    )
    delete_link = tables.LinkColumn(
        viewname='stock_delete',   
        args=[tables.A('pk')], 
        text='delete',  
        empty_values=(),  
    )
    class Meta:
        model = Stock
        template_name = "django_tables2/bootstrap.html"
        fields = ("stock_no","category","description","current_level","edit_link","delete_link")

class itemtable(tables.Table):
    edit_link = tables.LinkColumn(
        viewname='item_edit',  
        args=[tables.A('pk')], 
        text='edit',  
        empty_values=(),  
    )
    delete_link = tables.LinkColumn(
        viewname='item_delete',  
        args=[tables.A('pk')], 
        text='delete',  
        empty_values=(),  
    )
    class Meta:
        model= Item
        template_name = "django_tables2/bootstrap.html"
        fields = ("name","price","description","stock","edit_link","delete_link" )

class cattable(tables.Table):
    name = tables.Column()
    description = tables.Column()

    
    edit_link = tables.LinkColumn(
        viewname='catagory_edit',  
        args=[tables.A('pk')], 
        text='edit',  
        empty_values=(),  
    )
    delete_link = tables.LinkColumn(
        viewname='delete_catagory',  
        args=[tables.A('pk')], 
        text='delete',  
        empty_values=(),  
    )
    class Meta:
        model= Category
        template_name = "django_tables2/bootstrap.html"
        fields = ("name","description","edit_link","delete_link")


class MaterialRequesttable(tables.Table):
        edit_link = tables.LinkColumn(
        viewname='editstatus',  
        args=[tables.A('pk')], 
        text='edit',  
        empty_values=(),  
    )
        
        user = tables.Column(accessor='user.user_name')
    
        class Meta:
         
         model= MaterialRequest
         template_name = "django_tables2/bootstrap.html"
         fields = ("user","item","quantity_requested","status","request_date","edit_link")
