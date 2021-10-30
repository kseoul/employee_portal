# Generated by Django 3.2.8 on 2021-10-29 19:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management_app', '0003_auto_20211029_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportemployees',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='leavereportemployees',
            name='leave_date',
            field=models.DateField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='leavereportemployees',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
