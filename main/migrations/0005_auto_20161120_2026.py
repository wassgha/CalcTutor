# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-20 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_course_course_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='topic_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_active',
            field=models.BooleanField(default=False),
        ),
    ]
