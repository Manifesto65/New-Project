# Generated by Django 3.2.13 on 2022-07-14 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_remove_home_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='website.home'),
            preserve_default=False,
        ),
    ]