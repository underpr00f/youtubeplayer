import random
import string
from django.db import transaction
from django.shortcuts import render, redirect
from haikunator import Haikunator
from .models import Room
from django.views.decorators.cache import never_cache
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .forms import FriendForm


haikunator = Haikunator()

@never_cache
@login_required
def about(request):
    return render(request, "chat/about.html")

@never_cache
@login_required
def new_room(request, *args,**kwargs):
    """
    Randomly create a new room, and redirect to it.
    """

    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)

    return redirect("chat_index:chat_list_rooms")


@never_cache
@login_required
def chat_room(request, pk, *args,**kwargs):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """


    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room = Room.objects.get(pk=pk)
    # We want to show the last 50 messages, ordered most-recent-last
    messages = room.messages.order_by('-timestamp')[:10]
    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })

@never_cache
@login_required
def chat_list_rooms(request):

    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("id")
    # Render that in the index template
    return render(request, "chat/list_rooms.html", {
        "rooms": rooms,
    })
'''
@never_cache
@login_required
def priv_room(request):
    users = User.objects.order_by('id')

    return render(request, "chat/priv_room.html",{
        "users": users,
        })    
'''

class FriendView(TemplateView):
    template_name = "chat/priv_room.html"
    

    def get(self, request, *args, **kwargs):
        
        form = FriendForm()
        users = User.objects.exclude(id=request.user.id)
        #friend = get_object_or_404(Friend, current_user=request.user)
        query = request.GET.get("q")

        #true_friends=[]
        

        if query:
            queryset_list = User.objects.filter(username=query)
        else:
            queryset_list = None

        #your followers
        #drugs = Friend.who_added_user(request.user)
        #friendlist = []
        #try to get or except None
        '''
        try:

            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
            if friends:
                for fr in friends:
                    friendlist.append(fr)
                      
        except Friend.DoesNotExist:           
            friends = None
        '''
        #friend, created = Friend.objects.get_or_create(current_user=request.user)
        #friends = friend.users.all()
        '''
        for fr in friends:
            friendlist.append(fr)
        '''
        '''
        true_friends = []

        for friend in friends:
            friendlist.append(friend)
            
            for drug in drugs:
                 
                if drug.pk == friend.pk:
                    true_friends.append(drug)
                    drugs.remove(drug)
                    friendlist.remove(drug)
        '''
                


        context = {'form': form, 'users': users,
                   #'friends': friends,
                   #'drugs': drugs,
                   'object_list': queryset_list,
                   #'true_friends': true_friends,
                   #'friendlist': friendlist,
                   }
        return render(request,self.template_name, context)        
