

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=100, verbose_name='제목')),
                ('content', models.TextField(max_length=100, verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='후기 생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='후기 수정 시간')),
                ('rating_cnt', models.PositiveIntegerField(verbose_name='별점')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place', verbose_name='장소')),
                ('review_like', models.ManyToManyField(blank=True, related_name='like_review', to=settings.AUTH_USER_MODEL, verbose_name='후기 좋아요')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'db_table': 'review',
            },
        ),
    ]
