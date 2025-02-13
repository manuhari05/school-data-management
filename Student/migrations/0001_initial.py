# Generated by Django 5.1.2 on 2024-10-23 12:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Department', '0002_initial'),
        ('Teacher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('rollno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phy_marks', models.FloatField(default=0.0)),
                ('che_marks', models.FloatField(default=0.0)),
                ('maths_marks', models.FloatField(default=0.0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('total_marks', models.FloatField(editable=False)),
                ('percentage', models.FloatField(editable=False)),
                ('phy_pass', models.BooleanField(default=False)),
                ('che_pass', models.BooleanField(default=False)),
                ('maths_pass', models.BooleanField(default=False)),
                ('result', models.BooleanField(default=False)),
                ('dept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Department.departments')),
                ('teacher_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Teacher.teachers')),
            ],
        ),
    ]
