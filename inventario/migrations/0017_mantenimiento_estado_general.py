# Generated by Django 5.1.3 on 2024-12-06 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0016_mantenimiento_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='mantenimiento',
            name='estado_general',
            field=models.CharField(choices=[('Óptimo', 'Óptimo'), ('Bueno', 'Bueno'), ('Regular', 'Regular'), ('Malo', 'Malo')], default='Bueno', max_length=50),
        ),
    ]
