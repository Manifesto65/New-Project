# Generated by Django 3.2.13 on 2022-07-13 07:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20220713_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='client',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(0)]),
        ),
    ]