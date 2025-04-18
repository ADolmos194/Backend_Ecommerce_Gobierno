# Generated by Django 5.2 on 2025-04-18 02:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
        ('app_categorias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemandaProductosAgropecuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_publicacion', models.DateField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('nota', models.TextField(blank=True, null=True)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('contacto', models.TextField(blank=True, null=True)),
                ('telefono', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('distrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.distrito')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.estado')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_categorias.producto')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.provincia')),
            ],
            options={
                'db_table': 'demandaproductosagropecuarios',
            },
        ),
    ]
