# Generated by Django 3.2.8 on 2022-06-05 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0030_order_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='descriptionToFind',
            field=models.CharField(default='', max_length=100),
        ),
    ]
