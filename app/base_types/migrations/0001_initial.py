# Generated by Django 4.1 on 2022-12-11 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CDCs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=64, verbose_name='ОКД')),
            ],
            options={
                'verbose_name': 'ОКД',
                'verbose_name_plural': 'ОКД',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ClueAttrs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Значащий атрибут',
                'verbose_name_plural': 'Значащие атрибуты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DataObjects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Объект данных')),
            ],
            options={
                'verbose_name': 'Объект данных логического узла',
                'verbose_name_plural': 'Объекты данных логического узла',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Datasets',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, verbose_name='Датасет')),
            ],
            options={
                'verbose_name': 'Датасет',
                'verbose_name_plural': 'Датасеты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LogicDevices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Обозначение логического устройства')),
                ('fb_name', models.CharField(max_length=128, unique=True, verbose_name='Обозначение функционального блока')),
                ('description', models.TextField(blank=True, max_length=1024, verbose_name='Назначение логического устройства (ФБ)')),
            ],
            options={
                'verbose_name': 'Логическое устройство',
                'verbose_name_plural': 'Логические устройства',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LogicNodesTypes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Имя типа ЛУ')),
                ('description', models.TextField(blank=True, max_length=1024, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Тип логического узла',
                'verbose_name_plural': 'Типы логических узлов',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Signals',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Сигналы')),
            ],
            options={
                'verbose_name': 'Перечень сигналов',
                'verbose_name_plural': 'Перечни сигналов',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, verbose_name='Статусы сигнала')),
            ],
            options={
                'verbose_name': 'Статус сигнала',
                'verbose_name_plural': 'Статусы сигнала',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Terminals',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Обозначение ИЭУ')),
                ('description', models.TextField(blank=True, max_length=1024, verbose_name='Назначение ИЭУ')),
            ],
            options={
                'verbose_name': 'ИЭУ',
                'verbose_name_plural': 'ИЭУ',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PhDLDconnections',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ied', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.terminals', verbose_name='Физическое устройство')),
                ('ld', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.logicdevices', verbose_name='Логическое устройство')),
            ],
            options={
                'verbose_name': 'Связь между физическими и логическими устройствами',
                'verbose_name_plural': 'Связи между физическими и логическими устройствами',
                'ordering': ['ied'],
            },
        ),
        migrations.CreateModel(
            name='LogicNodeInstantiated',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('short_name', models.CharField(blank=True, default='', max_length=64, verbose_name='Краткое имя функции')),
                ('ln_prefix', models.CharField(blank=True, max_length=32, verbose_name='Префикс ЛУ')),
                ('class_name', models.CharField(max_length=4, verbose_name='Класс')),
                ('instance', models.IntegerField(blank=True, verbose_name='Номер экземпляра')),
                ('ln_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.logicnodestypes', verbose_name='Тип ЛУ')),
            ],
            options={
                'verbose_name': 'Экземпляр логического узла',
                'verbose_name_plural': 'Экземпляр логического узла',
                'ordering': ['short_name'],
            },
        ),
        migrations.CreateModel(
            name='LNobject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('func_group', models.IntegerField(default=-1, verbose_name='Функ. группа')),
                ('cus', models.CharField(choices=[('+', '+'), ('-', '-')], default='-', max_length=1, verbose_name='ЦУС')),
                ('rdu', models.CharField(choices=[('+', '+'), ('-', '-')], default='-', max_length=1, verbose_name='РДУ')),
                ('ras', models.CharField(choices=[('+', '+'), ('-', '-'), ('П', 'П')], default='-', max_length=1, verbose_name='РАС')),
                ('sgras_name', models.CharField(blank=True, max_length=64, verbose_name='Обозначение РАС/Уставка')),
                ('signal_type', models.CharField(choices=[('Внутр', 'Внутренний сигнал'), ('ВнутрШтрих', 'Внутренний штриховой'), ('-', 'Без прорисовки')], default='-', max_length=32, verbose_name='Тип сигнала (чертеж)')),
                ('signal_number', models.IntegerField(default=0, verbose_name='Номер выхода (чертеж)')),
                ('cdc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_types.cdcs', verbose_name='ОКД')),
                ('clue_attr', models.ForeignKey(default='<не задан>', on_delete=django.db.models.deletion.CASCADE, to='base_types.clueattrs', verbose_name='Значащий атрибут')),
                ('data_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_types.dataobjects', verbose_name='Объект данных')),
                ('dataset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.datasets', verbose_name='Датасет')),
                ('signal', models.ForeignKey(default='<не задан>', null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.signals', verbose_name='Сигнал')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.statuses', verbose_name='Статус сигнала')),
            ],
            options={
                'verbose_name': 'Объект логического узла',
                'verbose_name_plural': 'Объекты логических узлов',
                'ordering': ['data_object'],
            },
        ),
        migrations.CreateModel(
            name='LNobjConnections',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ln_inst', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.logicnodeinstantiated', verbose_name='Экземпляр логического узла')),
                ('ln_obj', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.lnobject', verbose_name='Объект лог. узла')),
            ],
            options={
                'verbose_name': 'Связь между экземплярами логических узлов и объектами',
                'verbose_name_plural': 'Связи между экземплярами логических узлов и объектами',
                'ordering': ['ln_inst'],
            },
        ),
        migrations.CreateModel(
            name='LDLNconnections',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ld', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.logicdevices', verbose_name='Логическое устройство')),
                ('ln', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.logicnodeinstantiated', verbose_name='Экземпляр лог. узла')),
            ],
            options={
                'verbose_name': 'Связь между логическими устройствами и экземплярами логических узлов',
                'verbose_name_plural': 'Связи между логическими устройствами и экземплярами логических узлов',
                'ordering': ['ld'],
            },
        ),
        migrations.CreateModel(
            name='Cabinets',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='Обозначение шкафа')),
                ('description', models.TextField(max_length=1024, verbose_name='Назначение шкафа')),
                ('terminal1', models.ForeignKey(max_length=64, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ied1_set', to='base_types.terminals', verbose_name='ИЭУ1')),
                ('terminal2', models.ForeignKey(blank=True, max_length=64, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ied2_set', to='base_types.terminals', verbose_name='ИЭУ2')),
                ('terminal3', models.ForeignKey(blank=True, max_length=64, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ied3_set', to='base_types.terminals', verbose_name='ИЭУ3')),
            ],
            options={
                'verbose_name': 'Шкаф',
                'verbose_name_plural': 'Шкафы',
                'ordering': ['name'],
            },
        ),
    ]
