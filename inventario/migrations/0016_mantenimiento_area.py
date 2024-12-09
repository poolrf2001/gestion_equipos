# Generated by Django 5.1.3 on 2024-12-06 03:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0015_mantenimiento_foto_antes_mantenimiento_foto_despues_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mantenimiento',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.area'),
        ),
    ]