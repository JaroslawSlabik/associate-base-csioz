# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name_text', models.CharField(max_length=300, null=True)),
                ('street_text', models.CharField(max_length=200, null=True)),
                ('number_text', models.CharField(max_length=200, null=True)),
                ('local_text', models.CharField(max_length=200, null=True)),
                ('zip_code_text', models.CharField(max_length=8, null=True)),
                ('city_text', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Associate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name_text', models.CharField(max_length=200)),
                ('surname_text', models.CharField(max_length=200)),
                ('specialization_text', models.CharField(max_length=200, null=True)),
                ('pwz_num', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name_text', models.CharField(max_length=200)),
                ('value_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('associate_file', models.FileField(null=True, upload_to='')),
                ('addresses_file', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='addresses',
            name='associate',
            field=models.ForeignKey(to='associate.Associate'),
        ),
    ]
