# Generated by Django 4.2.5 on 2023-10-09 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
