# Generated by Django 5.0.4 on 2024-06-26 22:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Canino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_canino', models.CharField(max_length=100, unique=True)),
                ('nombre_canino', models.CharField(max_length=100)),
                ('nombre_dueño', models.CharField(max_length=100)),
                ('dictamen', models.CharField(max_length=100)),
                ('cedula', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=100)),
                ('años_canino', models.IntegerField()),
                ('imagen', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Pruebas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_prueba', models.CharField(choices=[('Aliento', 'Aliento'), ('opcion2', 'Opción 2'), ('opcion3', 'Opción 3')], max_length=100)),
                ('diagnostico', models.IntegerField(choices=[(0, 'Con Erliquiosis'), (1, 'Sin Erliquiosis')])),
                ('archivo', models.FileField(upload_to='uploads/')),
                ('dimensiones', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('canino', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.canino')),
            ],
        ),
    ]
