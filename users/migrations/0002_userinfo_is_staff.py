# Generated by Django 3.0.6 on 2020-05-26 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
