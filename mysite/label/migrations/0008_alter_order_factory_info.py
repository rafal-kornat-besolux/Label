# Generated by Django 3.2.8 on 2022-01-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0007_alter_order_factory_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='factory_info',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
