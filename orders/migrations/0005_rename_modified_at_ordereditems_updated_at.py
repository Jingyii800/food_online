# Generated by Django 4.2.7 on 2023-11-19 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_ordereditems_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordereditems',
            old_name='modified_at',
            new_name='updated_at',
        ),
    ]
