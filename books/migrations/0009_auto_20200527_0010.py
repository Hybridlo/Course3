# Generated by Django 3.0.6 on 2020-05-26 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20200526_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='books.Book'),
        ),
        migrations.AlterField(
            model_name='taking',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='takings', to='books.Book'),
        ),
    ]
