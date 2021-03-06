# Generated by Django 3.2.6 on 2021-08-16 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vtx', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='addrTemp',
        ),
        migrations.RemoveField(
            model_name='node',
            name='addrVibraX',
        ),
        migrations.RemoveField(
            model_name='node',
            name='addrVibraZ',
        ),
        migrations.RemoveField(
            model_name='node',
            name='address',
        ),
        migrations.RemoveField(
            model_name='node',
            name='alertTemp',
        ),
        migrations.RemoveField(
            model_name='node',
            name='alertVibraX',
        ),
        migrations.RemoveField(
            model_name='node',
            name='alertVibraZ',
        ),
        migrations.RemoveField(
            model_name='node',
            name='ciclo',
        ),
        migrations.RemoveField(
            model_name='node',
            name='node',
        ),
        migrations.CreateModel(
            name='NodeSetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nodeId', models.IntegerField(default=1, verbose_name='Node')),
                ('address', models.IntegerField(default=1, verbose_name='endereço')),
                ('ciclo', models.IntegerField(default=60, verbose_name='ciclo de logs (s)')),
                ('addrVibraX', models.IntegerField(default=1, verbose_name='endereço eixo x')),
                ('addrVibraZ', models.IntegerField(default=1, verbose_name='endereço eixo z')),
                ('addrTemp', models.IntegerField(default=1, verbose_name='endereço Temperatura')),
                ('alertVibraX', models.DecimalField(decimal_places=3, default=5.0, max_digits=7, verbose_name='Alert eixo x')),
                ('alertVibraZ', models.DecimalField(decimal_places=3, default=5.0, max_digits=7, verbose_name='Alert eixo z')),
                ('alertTemp', models.DecimalField(decimal_places=1, default=60.0, max_digits=5, verbose_name='Alert Temperatura')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vtx.node')),
            ],
            options={
                'verbose_name': 'NodeSetup',
                'verbose_name_plural': 'NodeSetups',
            },
        ),
    ]
