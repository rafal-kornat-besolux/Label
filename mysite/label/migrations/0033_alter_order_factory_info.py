# Generated by Django 3.2.8 on 2022-06-06 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0032_alter_order_factory_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='factory_info',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
