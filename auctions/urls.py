from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="createListing"),
    path("watch/<int:user_id>", views.watchList, name="watchList"),
    path("categories", views.categories, name="catalog"),
    path("categories/<str:category>", views.filtered_index, name='filtered index'),
    path("listing/<int:list_id>", views.listing_page, name="listing"),
    path("closed", views.closed, name="closed"),
    path("myLists/<int:us_id>", views.all_listing, name="myList"),

]

