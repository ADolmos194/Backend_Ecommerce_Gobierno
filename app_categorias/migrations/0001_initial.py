# Generated by Django 5.2 on 2025-04-15 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.estado')),
            ],
            options={
                'db_table': 'tipoproducto',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.estado')),
                ('tipoproducto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_categorias.tipoproducto')),
            ],
            options={
                'db_table': 'producto',
            },
        ),
    ]
