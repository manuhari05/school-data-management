# Generated by Django 5.1.2 on 2024-11-01 00:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Department', '0006_remove_departments_hod_remove_departments_school'),
        ('School', '0003_schools_dept'),
        ('Student', '0008_alter_students_teacher_id'),
        ('Teacher', '0004_teachers_hod_teachers_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dept_students', to='Department.departments'),
        ),
        migrations.AlterField(
            model_name='students',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='school_students', to='School.schools'),
        ),
        migrations.AlterField(
            model_name='students',
            name='teacher_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='teacher_students', to='Teacher.teachers'),
        ),
    ]
