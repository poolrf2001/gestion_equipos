# Generated by Django 5.1.3 on 2024-12-12 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0026_alter_mantenimiento_acciones_recomendadas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='ubicacion',
            field=models.CharField(choices=[('Centro Cívico', 'Centro Cívico'), ('Terrapuerto', 'Terrapuerto'), ('Moto Vivanco', 'Moto Vivanco'), ('Camal', 'Camal')], max_length=50, null=True),
        ),
    ]
