# Generated by Django 2.0 on 2018-01-01 17:25

from django.db import migrations, models
import django.db.models.deletion
import finder.models
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subdirectories', to='finder.Folder')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(height_field='height', unique=True, upload_to=finder.models._picture_path, width_field='width')),
                ('height', models.PositiveSmallIntegerField()),
                ('width', models.PositiveSmallIntegerField()),
                ('size', models.BigIntegerField()),
                ('sha256', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='folder',
            name='pictures',
            field=models.ManyToManyField(blank=True, related_name='folders', to='finder.Picture'),
        ),
    ]
