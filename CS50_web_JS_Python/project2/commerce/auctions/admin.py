from django.contrib import admin
from .models import Auction_listings, User, Watchlist, Bids, Comments, Categories
# Register your models here.

admin.site.register(Auction_listings)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Categories)