# Generated by Django 3.2.8 on 2022-05-21 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0025_remove_campaign_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packagefromclient',
            name='transporter',
        ),
    ]
