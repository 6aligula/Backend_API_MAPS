# Generated by Django 4.0 on 2024-08-02 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_registrodocumento_entrada_salida'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrodocumento',
            old_name='entrada_salida',
            new_name='entrada',
        ),
        migrations.AddField(
            model_name='registrodocumento',
            name='salida',
            field=models.BooleanField(default=True),
        ),
    ]
