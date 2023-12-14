# Generated by Django 5.0 on 2023-12-13 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_listings_bids_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listings',
            name='description',
            field=models.CharField(default='description default value', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auction_listings',
            name='image_url',
            field=models.URLField(default='no img url(default value)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auction_listings',
            name='starting_bid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auction_listings',
            name='title',
            field=models.CharField(default='none (default value)', max_length=64),
            preserve_default=False,
        ),
    ]
