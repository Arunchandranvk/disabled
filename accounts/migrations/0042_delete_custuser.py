# Generated by Django 4.2.5 on 2023-09-26 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0041_custuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustUser',
        ),
    ]