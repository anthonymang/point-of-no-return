# Generated by Django 3.2.4 on 2021-06-29 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=50)),
                ('bio', models.CharField(max_length=1000)),
                ('bandcamp_link', models.URLField()),
                ('spotify_link', models.URLField()),
                ('instagram_link', models.URLField()),
                ('twitter_link', models.URLField()),
                ('discogs_link', models.URLField()),
                ('spotify_embed', models.CharField(max_length=1000)),
                ('bandcamp_embed', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('comments', models.CharField(max_length=1000)),
                ('social_media_link', models.URLField()),
                ('you', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('release_year', models.IntegerField()),
                ('release_date', models.DateField()),
                ('description', models.CharField(max_length=1000)),
                ('spotify_embed', models.CharField(max_length=1000)),
                ('bandcamp_embed', models.CharField(max_length=1000)),
                ('discogs_link', models.URLField()),
                ('genre', models.CharField(max_length=1000)),
                ('release_type', models.CharField(choices=[('LP', 'LP'), ('EP', 'EP'), ('Single', 'Single'), ('Song', 'Song')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Curator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]