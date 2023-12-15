from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_list", views.create_list, name="create_list"),
    path("details/<int:auctionId>", views.details, name="details"),
    path("watchlist/<int:auctionId>", views.watchlist, name="watchlist"),
    path("bid/<int:auctionId>", views.bid, name="bid"),
    path("remove_watchlist/<int:auctionId>", views.remove_watchlist, name="remove_watchlist"),
    path("close_auction/<int:auctionId>", views.close_auction, name="close_auction"),
    path("comment/<int:auctionId>", views.comment, name="comment"),
    path("show_watchlist", views.show_watchlist, name="show_watchlist"),
    path("category_details", views.categories, name="categories"),
    path("category_details/<str:Category_name>", views.category_details, name="category_details")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)