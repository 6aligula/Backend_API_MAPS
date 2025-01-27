# Generated by Django 4.0 on 2024-08-03 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_remove_lineafactura_total_sin_iva_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineafactura',
            name='iva',
            field=models.IntegerField(choices=[(10, '10%'), (21, '21%'), (0, '0%')], default=0),
        ),
    ]
