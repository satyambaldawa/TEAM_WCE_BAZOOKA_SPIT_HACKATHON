# Generated by Django 4.0.1 on 2022-01-28 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_extenduser_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.FloatField(default=150, verbose_name='Height in cm'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.FloatField(default=40, verbose_name='Weight in kg'),
        ),
    ]
