# Generated by Django 5.1.2 on 2024-10-23 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachers',
            name='empid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
