# Generated by Django 4.1.3 on 2022-12-20 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='후기 생성 시간'),
        ),
        migrations.AlterField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='후기 수정 시간'),
        ),
    ]