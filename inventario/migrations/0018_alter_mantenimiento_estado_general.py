# Generated by Django 5.1.3 on 2024-12-07 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0017_mantenimiento_estado_general'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimiento',
            name='estado_general',
            field=models.CharField(choices=[('Óptimo', 'Óptimo'), ('Bueno', 'Bueno'), ('Regular', 'Regular'), ('Malo', 'Malo')], default='Bueno', max_length=50, verbose_name='Estado General'),
        ),
    ]