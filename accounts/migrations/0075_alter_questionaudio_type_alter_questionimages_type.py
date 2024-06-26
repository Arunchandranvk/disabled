# Generated by Django 4.2.5 on 2024-01-07 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0074_alter_question_type_alter_questionaudio_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionaudio',
            name='type',
            field=models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.types'),
        ),
        migrations.AlterField(
            model_name='questionimages',
            name='type',
            field=models.ForeignKey(default=3, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.types'),
        ),
    ]
