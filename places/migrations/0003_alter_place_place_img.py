# Generated by Django 4.1.3 on 2022-12-09 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0002_alter_place_latitude_alter_place_longitude"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="place_img",
            field=models.TextField(null=True, verbose_name="장소 이미지"),
        ),
    ]