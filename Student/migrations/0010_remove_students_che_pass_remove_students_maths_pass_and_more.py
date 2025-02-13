# Generated by Django 5.1.2 on 2024-11-04 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0009_alter_students_dept_alter_students_school_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='che_pass',
        ),
        migrations.RemoveField(
            model_name='students',
            name='maths_pass',
        ),
        migrations.RemoveField(
            model_name='students',
            name='percentage',
        ),
        migrations.RemoveField(
            model_name='students',
            name='phy_pass',
        ),
        migrations.AlterField(
            model_name='students',
            name='total_marks',
            field=models.FloatField(default=0.0),
        ),
    ]
