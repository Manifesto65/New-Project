# Generated by Django 4.0.5 on 2022-06-24 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_about_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='company_logo',
            field=models.ImageField(default=1, upload_to='uploads/about'),
            preserve_default=False,
        ),
    ]
