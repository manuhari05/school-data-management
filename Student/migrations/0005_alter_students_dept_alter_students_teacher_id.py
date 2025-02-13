# Generated by Django 5.1.2 on 2024-10-30 06:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Department', '0005_alter_departments_school'),
        ('Student', '0004_students_is_active'),
        ('Teacher', '0003_teachers_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='students', to='Department.departments'),
        ),
        migrations.AlterField(
            model_name='students',
            name='teacher_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='students', to='Teacher.teachers'),
        ),
    ]
