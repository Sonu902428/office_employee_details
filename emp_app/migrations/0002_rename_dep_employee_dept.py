# Generated by Django 5.0.4 on 2024-09-13 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emp_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='dep',
            new_name='dept',
        ),
    ]