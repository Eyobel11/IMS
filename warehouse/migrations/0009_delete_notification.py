# Generated by Django 5.0.7 on 2024-08-28 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_materialrequest_notification_delete_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
