# Generated by Django 5.1.3 on 2024-12-04 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='area',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='codigo_inventario_monitor',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='marca_monitor',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='modelo_monitor',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='observaciones',
        ),
        migrations.RemoveField(
            model_name='periferico',
            name='area',
        ),
        migrations.RemoveField(
            model_name='periferico',
            name='observaciones',
        ),
        migrations.AddField(
            model_name='inventario',
            name='area_actual',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventario_area_actual', to='inventario.area'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='detalle_bien',
            field=models.CharField(default='Desconocido', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventario',
            name='estado_conservacion',
            field=models.CharField(choices=[('Bueno', 'Bueno'), ('Regular', 'Regular'), ('Malo', 'Malo')], default='Regular', max_length=50),
        ),
        migrations.AddField(
            model_name='periferico',
            name='area_actual',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='periferico_area_actual', to='inventario.area'),
        ),
        migrations.AddField(
            model_name='periferico',
            name='equipo_principal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perifericos', to='inventario.inventario'),
        ),
        migrations.AddField(
            model_name='periferico',
            name='estado_conservacion',
            field=models.CharField(choices=[('Bueno', 'Bueno'), ('Regular', 'Regular'), ('Malo', 'Malo')], default='Regular', max_length=50),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='marca',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='modelo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='periferico',
            name='marca',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='periferico',
            name='modelo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='periferico',
            name='tipo',
            field=models.CharField(choices=[('Monitor', 'Monitor'), ('Teclado', 'Teclado'), ('Mouse', 'Mouse'), ('Parlantes', 'Parlantes'), ('Otros', 'Otros')], max_length=50),
        ),
        migrations.CreateModel(
            name='HistorialArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cambio', models.DateTimeField(auto_now_add=True)),
                ('area_anterior', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='historial_area_anterior', to='inventario.area')),
                ('area_nueva', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='historial_area_nueva', to='inventario.area')),
                ('inventario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.inventario')),
                ('periferico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.periferico')),
            ],
        ),
    ]