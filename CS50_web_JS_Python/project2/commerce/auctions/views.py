from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

from .models import User, Auction_listings, Watchlist

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
def validate_min(value):
    if value > 20:
        raise ValidationError(f"{value} should be less than 20")
    
class BidPrice(forms.Form):
    price = forms.IntegerField(
        label="Give your bid price",
        min_value=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
        validators=[validate_min]
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
                                          image_url=auction_fm_ImgUrl)
            auction_db.save()
            return render(request, "auctions/create_list.html", {
                "form" : NewCreateForm(),
                "new_form" : auction_fm_title
            })
        else: 
            return HttpResponse("hello")

    else:
        return render(request, "auctions/create_list.html", {
            "form" : NewCreateForm()
        })

def details(request, auctionId):
    # Get the auction from the database or return a 404 if not found
    auction = get_object_or_404(Auction_listings, pk=auctionId)
    user = request.user
    bid_price = BidPrice()
    # Check whether auction is in the user watchlist
    if not user.watchlist.filter(auction=auction).exists():
        return render(request, "auctions/details.html", {
            "auction": auction,
            "rm_flg": 0,
            "bid_price": bid_price
        })
    else:
        return render(request, "auctions/details.html", {
            "auction": auction,
            "rm_flg": 1,
            "bid_price": bid_price
        }) 

@login_required
def watchlist(request, auctionId):
    # Get the auction from the database or return a 404 if not found
    auction = get_object_or_404(Auction_listings, id=auctionId)
    user = request.user
    bid_price = BidPrice()
    # Check whether auction is in the user watchlist
    if not user.watchlist.filter(auction=auction).exists():
        new_watchlist = Watchlist(user=user, auction=auction)
        new_watchlist.save()
        return render(request, "auctions/details.html", {
            "auction": auction,
            "rm_flg": 2,
            "bid_price": bid_price
        })
    else:
        return render(request, "auctions/details.html", {
            "auction": auction,
            "rm_flg": 1,
            "bid_price": bid_price
        }) 
    
def remove_watchlist(request, auctionId):
    auction = get_object_or_404(Auction_listings, id=auctionId)
    user = request.user
    user.watchlist.filter(auction = auction).delete()
    bid_price = BidPrice()
    return render(request, "auctions/details.html", {
            "auction": auction,
            "rm_flg": 3,
            "bid_price": bid_price
    }) 

def bid(request):
    if request.method == "POST":
        bid_price = request.POST["price"]
        return render(request, "auctions/bid.html", {
            "bid_price": bid_price
        })

        

        
