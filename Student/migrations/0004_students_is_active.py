# Generated by Django 5.1.2 on 2024-10-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0003_alter_students_che_marks_alter_students_maths_marks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
