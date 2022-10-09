# forms.py
from django import forms
from .models import *

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('seller', 'watcher',
    )
        widgets = {
            'title': forms.TextInput(attrs={'class':"form-control", 'placeholder':"title"}),
            'description': forms.TextInput(attrs={'class':"form-control"}),
            'starting_bid': forms.TextInput(attrs={'class':"form-control", 'placeholder':"price"}),
            'image': forms.URLInput(attrs={'class':"form-control", 'placeholder':"Add an image URL for your listing?"}),
            'category': forms.Select(attrs={'class':"form-control", 'placeholder':"Add an image URL for your listing?"}),
            'active': forms.CheckboxInput(attrs={'class':"form-control", 'aria-label':"Active Checkbox ",  'style': 'width:5vw;, height:5vh;'}),
            # 'seller': forms.Select(attrs={'class':"form-control", 'placeholder':"Owner"}),
            # 'watcher': forms.Select(attrs={'class':"form-control", 'placeholder':"watcher"}),     

        }




class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('offer',)
        widgets = { 

            'offer': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"your bid"}),
            }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commentBox',)

        widgets = { 
                'commentBox': forms.Textarea(attrs={'class':"form-control ml-1 shadow-none textarea", 'placeholder':"post your thought"}),
                }


class WacthListForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('active',)

        widgets = {
        'active': forms.CheckboxInput(attrs={'class':"checkbox", 'aria-label':"Is Active Listing ",  'style': 'width:5vw;, height:2vh;'}),
        }
