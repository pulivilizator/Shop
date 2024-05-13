# Generated by Django 5.0.5 on 2024-05-09 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='product',
        ),
        migrations.AddField(
            model_name='property',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='properties', to='shop_app.product'),
        ),
    ]