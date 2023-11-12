# Generated by Django 4.2.6 on 2023-11-12 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='transaction_details',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='transaction_type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]