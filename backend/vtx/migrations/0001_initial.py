# Generated by Django 3.2.6 on 2021-08-16 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='dispositivo')),
                ('address', models.IntegerField(default=1, unique=True, verbose_name='endereço')),
                ('port', models.CharField(default='COM1', max_length=20, verbose_name='porta')),
                ('boudrate', models.IntegerField(default=19200, verbose_name='BoudRate')),
                ('online', models.BooleanField(verbose_name='Online')),
            ],
            options={
                'verbose_name': 'Gateway',
                'verbose_name_plural': 'Gateways',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Equipamento')),
                ('address', models.IntegerField(default=1, verbose_name='endereço')),
                ('node', models.IntegerField(default=1, verbose_name='Node')),
                ('ciclo', models.IntegerField(default=60, verbose_name='ciclo de logs (s)')),
                ('addrVibraX', models.IntegerField(default=1, verbose_name='endereço eixo x')),
                ('addrVibraZ', models.IntegerField(default=1, verbose_name='endereço eixo z')),
                ('addrTemp', models.IntegerField(default=1, verbose_name='endereço Temperatura')),
                ('alertVibraX', models.DecimalField(decimal_places=3, default=5.0, max_digits=7, verbose_name='Alert eixo x')),
                ('alertVibraZ', models.DecimalField(decimal_places=3, default=5.0, max_digits=7, verbose_name='Alert eixo z')),
                ('alertTemp', models.DecimalField(decimal_places=1, default=60.0, max_digits=5, verbose_name='Alert Temperatura')),
                ('vibraX', models.DecimalField(decimal_places=3, default=0.0, max_digits=7, verbose_name='eixo x')),
                ('vibraZ', models.DecimalField(decimal_places=3, default=0.0, max_digits=7, verbose_name='eixo z')),
                ('temp', models.DecimalField(decimal_places=1, default=0.0, max_digits=5, verbose_name='Temperatura')),
                ('estado', models.CharField(max_length=30, verbose_name='Estado')),
                ('online', models.BooleanField(verbose_name='Online')),
            ],
            options={
                'verbose_name': 'Node',
                'verbose_name_plural': 'Nodes',
            },
        ),
        migrations.CreateModel(
            name='Hist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('alertVibraX', models.DecimalField(decimal_places=3, default=5.0, max_digits=7, verbose_name='Alert eixo x')),
                ('alertVibraZ', models.DecimalField(decimal_places=3, default=5.0, max_digits=7, verbose_name='Alert eixo z')),
                ('alertTemp', models.DecimalField(decimal_places=1, default=60.0, max_digits=5, verbose_name='Alert Temperatura')),
                ('vibraX', models.DecimalField(decimal_places=3, default=0.0, max_digits=7, verbose_name='eixo x')),
                ('vibraZ', models.DecimalField(decimal_places=3, default=0.0, max_digits=7, verbose_name='eixo z')),
                ('temp', models.DecimalField(decimal_places=1, default=0.0, max_digits=5, verbose_name='Temperatura')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vtx.node')),
            ],
            options={
                'verbose_name': 'Registro',
                'verbose_name_plural': 'Registros',
            },
        ),
    ]
