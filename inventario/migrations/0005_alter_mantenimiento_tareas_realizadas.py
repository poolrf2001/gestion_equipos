# Generated by Django 5.1.3 on 2024-12-05 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_alter_inventario_detalle_bien'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimiento',
            name='tareas_realizadas',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
