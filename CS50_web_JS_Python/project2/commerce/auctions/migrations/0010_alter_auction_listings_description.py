# Generated by Django 5.0 on 2023-12-14 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_auction_listings_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listings',
            name='description',
            field=models.CharField(max_length=256),
        ),
    ]