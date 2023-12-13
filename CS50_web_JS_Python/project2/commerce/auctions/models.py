from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction_listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    image_url = models.URLField()

    def __str__(self):
        return f"{self.title}: {self.description} start with {self.starting_bid}"

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass