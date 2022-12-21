# Generated by Django 3.2.16 on 2022-12-21 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_types', '0012_alter_sg_modes_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='input',
            name='ln_inst',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_types.logicnodeinstantiated', verbose_name='Экземпляр ЛУ к которому привязан вход'),
        ),
        migrations.AddField(
            model_name='input',
            name='number',
            field=models.IntegerField(default=0, verbose_name='Номер входа'),
        ),
        migrations.AlterField(
            model_name='input',
            name='sw_type',
            field=models.CharField(choices=[('SW.2', 'SW.2'), ('SW.3', 'SW.3'), ('-', '-')], default='-', max_length=4, verbose_name='Тип переключателя'),
        ),
    ]