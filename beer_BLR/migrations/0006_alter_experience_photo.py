# Generated by Django 4.2.4 on 2023-09-07 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_BLR', '0005_alter_technology_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='Blog/experience/'),
        ),
    ]