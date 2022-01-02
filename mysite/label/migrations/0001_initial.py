# Generated by Django 3.2.8 on 2021-12-29 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('client', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('besoRef', models.CharField(max_length=50, unique=True)),
                ('factoryRef', models.CharField(default='', max_length=50)),
                ('brand', models.CharField(blank=True, default='', max_length=50)),
                ('ean', models.IntegerField(blank=True, default=0)),
                ('fabric', models.CharField(max_length=50)),
                ('color', models.CharField(blank=True, default='', max_length=50)),
                ('full', models.CharField(blank=True, default='', max_length=300)),
                ('legsPlacement', models.CharField(blank=True, default='', max_length=50)),
                ('packagesQuantity', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.CharField(max_length=500)),
                ('country', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('ordinalNumber', models.IntegerField(default=1)),
                ('furniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='label.furniture')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='label.order')),
            ],
            options={
                'unique_together': {('order', 'furniture')},
            },
        ),
        migrations.CreateModel(
            name='Transporter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PackageFromClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pack', models.IntegerField(default=1)),
                ('number', models.IntegerField(default=1, unique=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='label.campaign')),
                ('furniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='label.furniture')),
                ('transporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='label.transporter')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordinalNumber', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('pack', models.IntegerField()),
                ('codeBeso', models.IntegerField(default=1, unique=True)),
                ('codeFactory', models.IntegerField(default=0)),
                ('orderProduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='label.orderproduct')),
                ('packageFromClient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='label.packagefromclient')),
            ],
        ),
    ]