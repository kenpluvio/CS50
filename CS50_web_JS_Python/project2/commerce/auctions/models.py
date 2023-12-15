from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auction_listings(models.Model):
    # id = models.AutoField(primary_key=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_item", default=1)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.IntegerField()
    image_url = models.URLField(blank=True)
    close_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} {self.title}: {self.description} start with {self.starting_bid}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user.username} have {self.auction} in their watchlist"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", default=1)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} have bid with {self.price}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", default=1)
    comment = models.CharField(max_length=256)
    auction = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user.username} have commented {self.comment} for {self.auction.title}"
    
class Categories(models.Model):
    Category_name = models.CharField(max_length=256)
    auction = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return f"{self.auction.title}'s category is {self.Category_name}"