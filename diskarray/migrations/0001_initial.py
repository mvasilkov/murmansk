# Generated by Django 2.0 on 2018-01-01 17:25

import datetime
import diskarray.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('objectid', models.CharField(default=diskarray.models._objectid, editable=False, max_length=24, unique=True)),
                ('coupling', models.CharField(choices=[('local', 'local'), ('roaming', 'roaming')], default='local', max_length=10)),
                ('dev_name', models.CharField(blank=True, max_length=20)),
                ('mount_point', models.CharField(blank=True, max_length=40)),
                ('is_healthy', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
                ('pictures', models.ManyToManyField(blank=True, related_name='disks', to='finder.Picture')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('size', models.BigIntegerField()),
                ('sha256', models.CharField(max_length=64, unique=True)),
                ('storage_class', models.PositiveSmallIntegerField(default=1)),
                ('media_class', models.CharField(choices=[('binary', 'binary'), ('video', 'video')], default='binary', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
                ('folders', models.ManyToManyField(blank=True, related_name='files', to='finder.Folder')),
                ('pictures', models.ManyToManyField(blank=True, related_name='files', to='finder.Picture')),
            ],
        ),
        migrations.CreateModel(
            name='FileCopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=1000)),
                ('is_healthy', models.BooleanField()),
                ('last_checked', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0))),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('disk', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='diskarray.Disk')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='copies', to='diskarray.File')),
            ],
            options={
                'verbose_name_plural': 'file copies',
            },
        ),
        migrations.CreateModel(
            name='Oplog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(max_length=1000)),
                ('stage', models.CharField(choices=[('waiting', 'waiting'), ('working', 'working'), ('ended', 'ended')], default='waiting', max_length=10)),
                ('error_code', models.SmallIntegerField(default=-1)),
                ('stdout', models.TextField()),
                ('stderr', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='filecopy',
            unique_together={('disk', 'file')},
        ),
    ]
