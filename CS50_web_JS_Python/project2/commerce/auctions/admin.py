from django.contrib import admin
from .models import Auction_listings, User, Watchlist
# Register your models here.

admin.site.register(Auction_listings)
admin.site.register(User)
admin.site.register(Watchlist)