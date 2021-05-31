# Generated by Django 3.2 on 2021-05-30 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_auto_20210422_1827'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscriber', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.category'),
        ),
        migrations.DeleteModel(
            name='PostCategory',
        ),
    ]