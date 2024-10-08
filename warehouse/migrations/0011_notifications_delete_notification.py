# Generated by Django 5.0.7 on 2024-08-28 12:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0010_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('notification_date', models.DateField()),
                ('read', models.BooleanField(default=False)),
                ('notification_type', models.CharField(choices=[('User', 'User'), ('Category', 'Category'), ('Stock', 'Stock'), ('Item', 'Item'), ('Order', 'Order'), ('MaterialRequest', 'MaterialRequest')], default='MaterialRequest', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
