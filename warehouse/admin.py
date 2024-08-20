from django.contrib import admin
from .models import*

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Stock)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(MaterialRequest)
admin.site.register(Notification)
