# Generated by Django 5.1.3 on 2024-12-08 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0018_alter_mantenimiento_estado_general'),
    ]

    operations = [
        migrations.AddField(
            model_name='mantenimiento',
            name='pdf_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
