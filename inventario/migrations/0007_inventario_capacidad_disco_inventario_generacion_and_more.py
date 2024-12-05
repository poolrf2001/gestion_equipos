# Generated by Django 5.1.3 on 2024-12-05 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0006_mantenimiento_tareas_otros'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='capacidad_disco',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='inventario',
            name='generacion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='inventario',
            name='procesador',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='inventario',
            name='ram',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventario',
            name='sistema_operativo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='inventario',
            name='tipo_disco',
            field=models.CharField(blank=True, choices=[('HDD', 'HDD'), ('SSD', 'SSD')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='inventario',
            name='velocidad',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='detalle_bien',
            field=models.CharField(choices=[('CPU', 'CPU'), ('LAPTOP', 'Laptop'), ('IMPRESORA', 'Impresora'), ('ALL IN ONE', 'All in One')], max_length=50),
        ),
    ]