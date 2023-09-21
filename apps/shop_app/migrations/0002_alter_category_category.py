# Generated by Django 4.2.5 on 2023-09-21 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.ForeignKey(blank=True, limit_choices_to={'category__isnull': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='shop_app.category'),
        ),
    ]
