# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order,Stock,Item

# @receiver(post_save, sender=Order)
# def update_stock_on_order_shipment(sender, instance, **kwargs):
#     if instance.status == 'shipped':
#         stock = instance.item.stock
#         stock.current_level += instance.quantity
#         stock.save()
# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import User, Item, Stock, Category, Notification

@receiver(post_save, sender=User)
def notify_user_change(sender, instance, created, **kwargs):
    if created:
        content = f"A new user '{instance.user_name}' has been created."
    else:
        content = f"User '{instance.user_name}' has been updated."
    
    Notification.objects.create(user=instance, content=content)

@receiver(post_save, sender=Item)
def notify_item_change(sender, instance, created, **kwargs):
    content = f"Item '{instance.name}' has been {'created' if created else 'updated'}."
    Notification.objects.create(user=instance.stock.category.stocks.first().category.stocks.first().user, content=content)

@receiver(post_save, sender=Stock)
def notify_stock_change(sender, instance, created, **kwargs):
    content = f"Stock '{instance.stock_no}' has been {'created' if created else 'updated'}."
    for item in instance.items.all():
        Notification.objects.create(user=item.stock.category.stocks.first().category.stocks.first().user, content=content)

@receiver(post_save, sender=Category)
def notify_category_change(sender, instance, created, **kwargs):
    content = f"Category '{instance.name}' has been {'created' if created else 'updated'}."
    Notification.objects.create(user=instance.stocks.first().category.stocks.first().user, content=content)
