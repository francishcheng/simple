# Generated by Django 3.1 on 2021-08-22 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ding', '0002_auto_20210822_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='SNcode',
            field=models.TextField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='location',
            field=models.CharField(max_length=100, verbose_name='地址'),
        ),
    ]
