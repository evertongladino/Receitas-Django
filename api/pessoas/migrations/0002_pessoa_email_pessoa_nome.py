# Generated by Django 4.0.2 on 2022-02-28 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='email',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='nome',
            field=models.CharField(default='', max_length=200),
        ),
    ]