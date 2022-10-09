from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
class User(AbstractUser):
    pass


class Categorie(models.Model):
    Category = [
    ('Cameras & Photo', 'Cameras & Photo'),
    ('Cell Phones & Accessories', 'Cell Phones & Accessories'),
    ('Clothing, Shoes & Accessories', 'Clothing, Shoes & Accessories'),
    ('Antiques', 'Antiques'),
    ('Collectibles', 'Collectibles'),
    ('Real Estate & Boats','Real Estate & Boats'),
    ('Art', 'Art'),
    ('Everything Else', 'Everything Else'),
    ]
    name = models.CharField(max_length=32, choices = Category, default=7)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']



class Listing(models.Model):
    title = models.CharField(max_length=128, default=None)
    description = models.CharField(max_length=180, default=None)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    current_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    image = models.URLField(max_length=1024, blank=True, null=True)
    category = models.ForeignKey(Categorie, on_delete=models.SET_DEFAULT, default='2')
    active = models.BooleanField(default=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    watcher = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def current_price(self):
        return max([bid.offer for bid in self.bids.all()]+[self.starting_bid])

    def __str__(self):
         return f'{self.title} by {self.seller}: {self.description}'






class Bid(models.Model):
    offer = models.DecimalField(max_digits=9, decimal_places=2, validators = [MinValueValidator(1)], default=None)
    buyer = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user_bids", default=None)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", default=None)
    winner = models.BooleanField(default = False)


    def clean(self):
        # Checks if offer is lower than current price of listing
        print(self.offer)
        print(self.listing.current_price())
        if self.offer and self.listing.current_price():
            if self.offer <= self.listing.current_price():
                raise ValidationError({'offer': (' Your bid  must be higher than the current ' 
                                                        'price!') })
    
    def __str__(self):
        return (f"A bid of {self.offer} made for the item - \n{self.listing.current_price()}\n by user - {self.buyer}")



class Comment(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", default=None, null=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=False)
    commentBox = models.TextField(verbose_name="Comment", default="", max_length=2048, null=False)
    timestamps = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_ID} commented on {self.listing} ({self.timestamps.date()})"



# class Watchlist(models.Model):
#     pass