# Generated by Django 4.0.4 on 2022-04-27 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_productphotos_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wallet',
            field=models.IntegerField(default=1000),
        ),
    ]
