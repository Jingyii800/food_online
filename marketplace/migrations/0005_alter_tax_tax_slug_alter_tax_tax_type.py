# Generated by Django 4.2.7 on 2023-11-17 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0004_tax_tax_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tax',
            name='tax_slug',
            field=models.SlugField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='tax',
            name='tax_type',
            field=models.CharField(max_length=20),
        ),
    ]
