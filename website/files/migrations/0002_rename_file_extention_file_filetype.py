# Generated by Django 4.0.2 on 2023-12-03 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='file_extention',
            new_name='fileType',
        ),
    ]
