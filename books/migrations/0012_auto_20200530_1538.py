# Generated by Django 3.0.6 on 2020-05-30 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_auto_20200530_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='digital',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
