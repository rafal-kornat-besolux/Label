# Generated by Django 3.2.8 on 2022-01-03 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0002_auto_20220103_1813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ismade',
            new_name='is_made',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='issent',
            new_name='is_sent',
        ),
    ]
