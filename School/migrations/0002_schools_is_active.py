# Generated by Django 5.1.2 on 2024-10-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('School', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schools',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
