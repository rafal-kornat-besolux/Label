# Generated by Django 3.2.8 on 2022-06-12 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0039_auto_20220612_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='transporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='label.transporter'),
        ),
    ]
