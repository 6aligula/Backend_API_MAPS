# Generated by Django 4.0 on 2024-08-04 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_alter_lineafactura_iva'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='fecha_pago',
            field=models.DateField(blank=True, null=True),
        ),
    ]
