# Generated by Django 4.2.7 on 2023-11-19 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_ordereditems_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordereditems',
            options={'verbose_name': 'ordered items', 'verbose_name_plural': 'ordered items'},
        ),
    ]
