from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    #  user = models.ForeignKey(
    #     'User',
    #     on_delete=models.CASCADE,
    # )
    #  post_date = models.DateField()
    #  user_post = models.TextField()
    pass
    


class Listing(models.Model):
    pass

class Bid(models.Model):
    pass

class Categories(models.Model):
    pass
