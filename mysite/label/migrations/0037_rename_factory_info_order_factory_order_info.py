# Generated by Django 3.2.8 on 2022-06-12 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0036_auto_20220612_1818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='factory_info',
            new_name='factory_order_info',
        ),
    ]
