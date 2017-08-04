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

class LabelForm(forms.ModelForm):
    """Master form for editing the user's profile
    def clean_label(self):
        title = self.cleaned_data['label']

        try:
            test = Member.objects.get(label__exact=title)
        except Member.DoesNotExist:
            return title
        else:
            raise forms.ValidationError('Дублирование данных!')
    """
    class Meta(object):
        """Configuration for the ModelForm"""
        model = Member

        fields = ('label', ) 