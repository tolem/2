from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User, Categorie, Listing, Bid, Comment
from .forms import *
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages


def index(request, closed=None):
    closed = request.GET.get(closed)
    listing = Listing.objects.all().filter(active=True)
    print(listing)
    return render(request, "auctions/index.html",{
        'listing': listing,
        'closed' : closed
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




@login_required
def create_listing(request):
    message = ""
    if request.method == "POST":
        print(request.POST)
        # listing_form = ListingForm(request.POST, request.FILES)
        # print(request.POST['seller'])
        # print(listing_form.errors, "where ")
        # print(listing_form.is_valid())
        # print(listing_form.fields['seller'])
        _user = User.objects.get(pk=request.user.pk)
        listform = Listing(seller=_user)
        # double check to make sure its an instance of same user
        listing_form = ListingForm(request.POST, request.FILES, instance=listform)
        if listing_form.is_valid():
            # only saves a listing that matches the current users id
            # if int(request.POST['seller']) == request.user.pk:
            listing_form.save(commit=False)
            listing_form.seller = request.user.pk
            listing_form.save()
            return HttpResponseRedirect(reverse("index"))
        
        else:
            message = "hmm something went wrong from your end? Please endeavor to fill the form correctly"

    else:
        listing_form = ListingForm()

    return render(request, 'auctions/create_listing.html', {
        "form": listing_form,
        "message" : message
        })


# shows a listing information
def listing_page(request, list_id):
    listing = Listing.objects.get(pk=list_id)
    msg = ''
    name = listing.seller
    # user_id = User.objects.get(username=name)
    watchers = User.objects.all()
    # user_id = int( user_id.pk )
    winner = None
    if request.user.pk == int(name.pk):
        watchlist_form = WacthListForm(instance=listing)
    else:
        watchlist_form = None


    print(watchlist_form, 'watch?')


    # sums the count of all watchers for a listing
    total_watchers = sum([1 for us in watchers if us.watchlist.filter(pk=listing.pk) ])
    watchlist_state = ''

    # breaking the DRY rule here. I know I lazy today haha
    if (request.user.pk):
        bid = BidForm()
        comment = CommentForm()
        u_id = User.objects.get(pk=request.user.pk)
        try:
            watchlist_state =  u_id.watchlist.filter(pk=listing.pk)
            if len(watchlist_state) == 0:
                watchlist_state = False 
            elif len(watchlist_state) >= 1:
                watchlist_state = True
            else:
                watchlist_state = ''

        except User.DoesNotExist:
            msg = 'users does not exist create an account to add items'
        finally:
            user =  User.objects.get(pk=request.user.pk)
            user_watchlist = user.watchlist.filter(pk=listing.pk)
            badge = user.watchlist.all()
            _ =  user.user_bids.all()

            # check to find winner 
            if not listing.active and len(_) > 1:
                winner = listing.bids.all()[0]
                print(winner.pk, user.pk, winner.buyer.pk)
                # checks to see if user is an instance of winner 
                if winner.buyer.pk == user.pk:
                    winner.winner = True
                print(winner.winner,_)


    else:
        user = tuple()
        user_watchlist = {}
        badge = []
        bid = None 
        comment = None




    if request.method == 'POST':
        try:
            if request.POST.get('state', False): 
                watchlist_form = WacthListForm(request.POST, request.FILES,instance=listing)
                if watchlist_form.is_valid():
                    watchlist_form.save()
                else:
                    watchlist_form = WacthListForm()
               
            _user = User.objects.get(pk=request.user.pk)
            if request.POST.get('haggle', False):
                # bid_form.add(user=int(request.user.pk), listing=)
                bid_user = User.objects.get(pk=request.user.pk)
                print(bid_user.user_bids.all())
                bid_p = Bid(buyer=bid_user, listing=listing)
                bid_form = BidForm(request.POST, request.FILES, instance=bid_p)
                if bid_form.is_valid():
                    bid_form.save(commit=False)
                    bid_form.user = request.user.pk
                    bid_form.listing = listing.pk
                    bid_form.save()
                    listing.bids.add(bid_p)
                    print(bid_form.errors)

                    return HttpResponseRedirect(reverse("listing",  args=(list_id,)))
                else:
                    msg = bid_form.errors['offer']
                    
            elif request.POST.get('posts', False):
                comment_p = Comment(user_ID=_user, listing=listing)
                comment = CommentForm(request.POST, request.FILES, instance=comment_p)
                if comment.is_valid():
                    comment.save(commit=False)
                    comment.title = request.user.pk
                    comment.listing = list_id
                    comment.save()

                    return HttpResponseRedirect(reverse("listing",  args=(list_id,)))


        except Bid.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: flight does not exist")

        except Comment.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: flight does not exist")


    
    


    # print(winner)    
    # print(winner.winner if winner else None)
    # comment = CommentForm() 
    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'watchlist_state':  watchlist_state,
        # shows count of item in watchlist
        'badge': len(badge),
        # shows badge if item in watchlist
        'is_watchlist': user_watchlist,
        'total_watchers': total_watchers,
        'bid' : bid,
        'posts': comment,
        'posted': listing.comments.all(),
        'total_bids': len(listing.bids.all()),
        'msg': msg, 
        'watchlist_form':  watchlist_form,
        'winner': winner.winner if winner else None,
        'name': winner.buyer if winner else None,
        'offer': winner.offer if winner else None,
        'comments_num': len(listing.comments.all()),

        })


# view for all active listings 
def categories(request):
    all_categories = Categorie.objects.all()
    # print(all_categories)
    return render(request, "auctions/categories.html", {
        'catalog': all_categories,
    
        })

# view for filtered active listing by categories
def filtered_index(request, category):
    category_id = Categorie.objects.get(name=category)
    print(category_id.pk)
    return render(request, "auctions/index.html", {
        'listing': Listing.objects.all().filter(category=category_id.pk, active=True),
        'category' : category_id,

        })


@login_required
def watchList(request, user_id):
    user = User.objects.get(pk=user_id)
    all_listing = Listing.objects.all()
    print(user.listings.all())
    print('Sucess')
    if request.method == 'POST':
        if request.POST.get('del', False):
            # print(int(request.POST['del']))
            # grabs current listings 
            remove_watchlist = user.watchlist.get(pk=int(request.POST['del']))
            print(remove_watchlist)
            # removes that listing
            user.watchlist.remove(remove_watchlist)



        elif request.POST.get('add', False):
            print('okay')
            print(int(request.POST['add']))
            # grabs item from listings
            add_watchlist = all_listing.get(pk=int(request.POST['add']))
            print(add_watchlist)
            # adds listings to user watchlist
            user.watchlist.add(add_watchlist)

            

        else:
            pass



    return render(request, "auctions/watchlist.html",{
        "User": user,
        "wacthlist": user.watchlist.all(),
        'len': len(user.listings.all()),
        'badge': len(user.watchlist.all()),
        'placed': len(user.user_bids.all())
        })


# Page not found
def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def closed(request):
    listing = Listing.objects.exclude(active=True).all()
    closed = True
    return render(request, "auctions/index.html",{
        'listing': listing,
        'closed': closed
        })

@login_required
def all_listing(request, us_id):
    try:
        user = User.objects.get(pk=us_id)

        return render(request, 'auctions/mylist.html', {
            'all_listed': user.listings.all(),
            'msg': ''
            })


    except User.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: user does not exist")
