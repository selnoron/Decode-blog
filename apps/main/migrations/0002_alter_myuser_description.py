# Generated by Django 5.1.5 on 2025-02-17 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='description',
            field=models.CharField(default='', max_length=100, verbose_name='описание'),
        ),
    ]
