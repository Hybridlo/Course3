# Generated by Django 3.0.6 on 2020-05-30 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_auto_20200527_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='digital',
            field=models.FileField(blank=True, null=True, upload_to='books/'),
        ),
    ]
