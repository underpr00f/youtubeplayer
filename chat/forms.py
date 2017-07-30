from django import forms
from django.contrib.auth.models import User
from .models import Member



class FriendForm(forms.ModelForm):
    """Master form for editing the user's profile"""
    username = forms.CharField()
    
    
    class Meta(object):
        """Configuration for the ModelForm"""
        model = User

        fields = ('username', ) 