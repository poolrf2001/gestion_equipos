# Generated by Django 5.1.3 on 2024-12-05 20:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0012_alter_periferico_area_actual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periferico',
            name='area_actual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='perifericos', to='inventario.area'),
        ),
    ]