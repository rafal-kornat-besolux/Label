# Generated by Django 3.2.8 on 2022-06-05 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0028_client_transporter'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_campaign',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='client',
            name='type',
            field=models.CharField(choices=[('Casual', 'Casual'), ('CasualOneInformation', 'CasualOneInformation'), ('DropshippingOutside', 'DropshipingOutside'), ('Dropshipping', 'Dropshipping')], default='Casual', max_length=50),
        ),
        migrations.AddField(
            model_name='factory',
            name='factoryReferenceRequirement',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderb2c',
            name='dropshippingApproval',
            field=models.CharField(default=False, max_length=100),
        ),
    ]
