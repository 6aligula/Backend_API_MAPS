# Generated by Django 4.0 on 2024-08-03 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_remove_factura_consumos_remove_factura_control_pago_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lineafactura',
            options={},
        ),
        migrations.AlterField(
            model_name='lineafactura',
            name='iva',
            field=models.DecimalField(choices=[(10, '10%'), (21, '21%'), (0, 'Exento')], decimal_places=2, default=0, max_digits=4),
        ),
    ]
