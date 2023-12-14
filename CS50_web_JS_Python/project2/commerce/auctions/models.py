from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auction_listings(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.IntegerField()
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.id} {self.title}: {self.description} start with {self.starting_bid}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user} have {self.auction} in their watchlist"

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass