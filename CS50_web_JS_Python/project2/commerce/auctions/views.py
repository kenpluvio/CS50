from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from .models import User, Auction_listings, Watchlist, Bids, Comments, Categories

class NewCreateForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )
    description = forms.CharField(
        label="Description",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )
    starting_bid = forms.IntegerField(
        label="Starting bid",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )
    image_url = forms.URLField(
        label="Image URL(optional)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )

  
class BidPrice(forms.Form):
    price = forms.IntegerField(
        label="Give your bid price",
        min_value=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )

class NewComment(forms.Form):
    new_comment = forms.CharField(
        label="Comment",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )

def index(request):
    all_auctions = Auction_listings.objects.all()
    return render(request, "auctions/index.html", {
        "all_auctions": all_auctions
    })
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_list(request):
    if request.method == "POST":
        auction_fm = NewCreateForm(request.POST)
        if auction_fm.is_valid():
            # get data from form
            auction_fm_title = auction_fm.cleaned_data['title']
            auction_fm_description = auction_fm.cleaned_data['description']
            auction_fm_SB = auction_fm.cleaned_data['starting_bid']
            auction_fm_ImgUrl = auction_fm.cleaned_data['image_url']
            # save to DB
            auction_db = Auction_listings(title = auction_fm_title, 
                                          description = auction_fm_description, 
                                          starting_bid = auction_fm_SB, 
                                          image_url=auction_fm_ImgUrl,
                                          create_user=request.user)
            auction_db.save()
            return render(request, "auctions/create_list.html", {
                "form" : NewCreateForm(),
                "new_form" : auction_fm_title
            })
        else:
            print(auction_fm.errors)
            return HttpResponse("Please Check URL validation")

    else:
        return render(request, "auctions/create_list.html", {
            "form" : NewCreateForm()
        })

def details(request, auctionId):
    # Get the auction from the database or return a 404 if not found
    auction = get_object_or_404(Auction_listings, pk=auctionId)
    user = request.user
    bid_price = BidPrice()
    bid = Bids.objects.last()
    comment_form = NewComment()
    all_comment = Comments.objects.all()
    # Check whether auction is in the user watchlist
    if user not in User.objects.all():
        return HttpResponse("please log in")
    elif user == auction.create_user:
        if not user.watchlist.filter(auction=auction).exists():
            return render(request, "auctions/details.html", {
                "auction": auction,
                "rm_flg": 0,
                "is_user": 1,
                "bid_price": bid_price,
                "bid_winner": bid.user.username,
                "current_user": user,
                "all_comment": all_comment,
                "comment_form": comment_form
            })
        else:
            return render(request, "auctions/details.html", {
                "auction": auction,
                "rm_flg": 1,
                "is_user": 1,
                "bid_winner": bid.user.username,
                "bid_price": bid_price,
                "current_user": user,
                "all_comment": all_comment,
                "comment_form": comment_form
            }) 
    else:
        if not user.watchlist.filter(auction=auction).exists():
            return render(request, "auctions/details.html", {
                "auction": auction,
                "rm_flg": 0,
                "is_user": 2,
                "bid_winner": bid.user.username,
                "bid_price": bid_price,
                "current_user": user,
                "all_comment": all_comment,
                "comment_form": comment_form
            })
        else:
            return render(request, "auctions/details.html", {
                "auction": auction,
                "rm_flg": 1,
                "is_user": 2,
                "bid_winner": bid.user.username,
                "bid_price": bid_price,
                "current_user": user,
                "all_comment": all_comment,
                "comment_form": comment_form
            }) 

@login_required
def watchlist(request, auctionId):
    # Get the auction from the database or return a 404 if not found
    auction = get_object_or_404(Auction_listings, id=auctionId)
    user = request.user
    bid_price = BidPrice()
    comment_form = NewComment()
    all_comment = Comments.objects.all()
    # Check whether auction is in the user watchlist
    if not user.watchlist.filter(auction=auction).exists():
        new_watchlist = Watchlist(user=user, auction=auction)
        new_watchlist.save()
        return render(request, "auctions/details.html", {
            "auction": auction,
            "rm_flg": 2,
            "bid_price": bid_price,
            "comment_form": comment_form,
            "all_comment": all_comment
        })
    else:
        return render(request, "auctions/details.html", {
            "auction": auction,
            "rm_flg": 1,
            "bid_price": bid_price,
            "comment_form": comment_form,
            "all_comment": all_comment
        }) 
    
def remove_watchlist(request, auctionId):
    auction = get_object_or_404(Auction_listings, id=auctionId)
    user = request.user
    user.watchlist.filter(auction = auction).delete()
    bid_price = BidPrice()
    comment_form = NewComment()
    all_comment = Comments.objects.all()
    return render(request, "auctions/details.html", {
            "auction": auction,
            "rm_flg": 3,
            "bid_price": bid_price,
            "comment_form": comment_form,
            "all_comment": all_comment
    }) 

def bid(request, auctionId):
    auction = get_object_or_404(Auction_listings, id=auctionId)
    bid_price = BidPrice()
    if request.method == "POST":
        new_price = request.POST["price"]
        comment_form = NewComment()
        all_comment = Comments.objects.all()
        if int(new_price) <= auction.starting_bid:
            return render(request, "auctions/details.html", {
                "auction": auction,
                "bid_price": bid_price,
                "bid_status": 2,
                "new_price": new_price,
                "comment_form": comment_form,
                "all_comment": all_comment
            })
        elif int(new_price) > auction.starting_bid:
            new_bid = Bids(user=request.user, price=int(new_price))
            new_bid.save()
            auction.starting_bid=int(new_price)
            auction.save()
            return render(request, "auctions/details.html", {
                "auction": auction,
                "bid_price": bid_price,
                "bid_status": 1,
                "new_price": new_price,
                "comment_form": comment_form,
                "all_comment": all_comment
            })

def close_auction(request, auctionId):
    auction = get_object_or_404(Auction_listings, id=auctionId)
    bid = Bids.objects.last()
    if request.method == "POST":
        auction.close_status = True
        auction.save()
        comment_form = NewComment()
        all_comment = Comments.objects.all()
        return render(request, "auctions/details.html", {
                "bid_winner": bid.user.username,
                "auction": auction,
                "comment_form": comment_form,
                "all_comment": all_comment
            })

def comment(request, auctionId):
    auction = get_object_or_404(Auction_listings, id=auctionId)
    if request.method == "POST":
        comment_content = request.POST["new_comment"]
        bid_price = BidPrice()
        new_comment = Comments(auction=auction, user = request.user, comment = comment_content)
        new_comment.save()
        comment_form = NewComment()
        all_comment = Comments.objects.all()
        return render(request, "auctions/details.html", {
                "all_comment": all_comment,
                "auction": auction,
                "bid_price": bid_price,
                "comment_form": comment_form
            })

def show_watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/show_watchlist.html", {
        "watchlist": watchlist
    })

def categories(request):
    categories = Categories.objects.values('Category_name').distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_details(request, Category_name):
    category_list = Categories.objects.filter(Category_name=Category_name)
    return render(request, "auctions/category_details.html", {
        "category_list": category_list
    })