# Generated by Django 4.0 on 2024-08-03 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_incidencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_factura', models.CharField(max_length=50, unique=True)),
                ('fecha_emision', models.DateField()),
                ('fecha_vencimiento', models.DateField()),
                ('total_facturado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(choices=[('Pagado', 'Pagado'), ('Pendiente', 'Pendiente'), ('Vencido', 'Vencido')], max_length=100)),
                ('consumos', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factura_asociada', to='backend.consumos')),
                ('control_pago', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factura_asociada', to='backend.controlpagos')),
                ('parcela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facturas', to='backend.caracteristicasparcela')),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
            },
        ),
    ]
