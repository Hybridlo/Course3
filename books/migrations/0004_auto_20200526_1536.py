# Generated by Django 3.0.6 on 2020-05-26 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20200524_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='descripton',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.RemoveField(
            model_name='book',
            name='authors',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
    ]
