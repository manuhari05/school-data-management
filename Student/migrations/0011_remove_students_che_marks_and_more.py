# Generated by Django 5.1.2 on 2024-11-04 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0010_remove_students_che_pass_remove_students_maths_pass_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='che_marks',
        ),
        migrations.RemoveField(
            model_name='students',
            name='maths_marks',
        ),
        migrations.RemoveField(
            model_name='students',
            name='phy_marks',
        ),
    ]
