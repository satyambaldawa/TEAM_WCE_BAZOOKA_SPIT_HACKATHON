# Generated by Django 4.0.1 on 2022-01-28 18:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodtracker', '0003_exercise_rename_foodtable_food_delete_exercisetable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
