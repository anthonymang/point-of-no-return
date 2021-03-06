# Generated by Django 3.2.4 on 2021-06-30 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_no_return', '0004_music_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='bandcamp_embed',
        ),
        migrations.AlterField(
            model_name='artist',
            name='bandcamp_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='bio',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='artist',
            name='discogs_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='instagram_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='location',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='artist',
            name='spotify_embed',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='artist',
            name='spotify_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='twitter_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='curator',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='music',
            name='bandcamp_embed',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='music',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='music',
            name='discogs_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='genre',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='music',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='music',
            name='release_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='release_type',
            field=models.CharField(blank=True, choices=[('LP', 'LP'), ('EP', 'EP'), ('Single', 'Single'), ('Song', 'Song')], max_length=10),
        ),
        migrations.AlterField(
            model_name='music',
            name='release_year',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='spotify_embed',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='submission',
            name='artist_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='submission',
            name='comments',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='submission',
            name='link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='social_media_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='you',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3),
        ),
    ]
