# Generated by Django 2.1 on 2019-12-26 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panopticum', '0007_auto_20191227_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentmodel',
            name='life_status',
            field=models.CharField(choices=[('unknown', '?'), ('new', 'New'), ('mature', 'Mature'), ('legacy', 'Legacy'), ('eol', 'End Of Life'), ('eos', 'End Of Support')], default='unknown', max_length=16),
        ),
    ]
