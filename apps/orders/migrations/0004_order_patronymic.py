# Generated by Django 4.2.5 on 2023-10-10 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_deliverymethod_paymentmethod_alter_country_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='patronymic',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
