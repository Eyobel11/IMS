# warehouse/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import*

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Category, Stock, Item, Order, MaterialRequest, Notification

@receiver(post_save)
def create_notification(sender, instance, created, **kwargs):
    if sender in [User, Category, Stock, Item, Order, MaterialRequest]:
        action = "created" if created else "updated"
        message = f"A {sender.__name__.lower()} has been {action}: {instance}"

        users = User.objects.filter(is_active=True)
        for user in users:
            if user.is_superuser:
                Notification.objects.create(
                    user=user,
                    message=message,
                    notification_date=timezone.now(),
                    notification_type=sender.__name__
                )
            elif user.user_type == 'Registeror' and sender.__name__ != 'User':
                Notification.objects.create(
                    user=user,
                    message=message,
                    notification_date=timezone.now(),
                    notification_type=sender.__name__
                )
            elif user.user_type == 'Engineer' and sender.__name__ == 'MaterialRequest':
                Notification.objects.create(
                    user=user,
                    message=message,
                    notification_date=timezone.now(),
                    notification_type=sender.__name__
                )

@receiver(post_save, sender=Order)
def update_stock_on_order(sender, instance, **kwargs):
    if instance.status == 'shipped':
        stock = instance.stock
        stock.current_level += instance.quantity
        stock.save()


@receiver(post_save, sender=MaterialRequest)
def update_stock_on_request(sender, instance, **kwargs):
    item=instance.item
    stock = item.stock
    if instance.status == 'issued':
        
        stock.current_level -= 1
    elif instance.status == 'returned':
        stock.current_level += 1
    else:
        None    
        
    stock.save()
