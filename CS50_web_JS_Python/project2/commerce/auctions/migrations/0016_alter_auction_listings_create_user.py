# Generated by Django 5.0 on 2023-12-14 21:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auction_listings_create_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listings',
            name='create_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='auction_item', to=settings.AUTH_USER_MODEL),
        ),
    ]