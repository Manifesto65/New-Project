# Generated by Django 3.2.13 on 2022-07-05 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('project_image', models.ImageField(upload_to='uploads/projects')),
            ],
        ),
    ]
