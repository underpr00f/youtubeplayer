import random
import string
from django.db import transaction
from django.shortcuts import render, redirect
from haikunator import Haikunator
from .models import Room
from django.views.decorators.cache import never_cache
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

haikunator = Haikunator()

@never_cache
@login_required
def about(request):
    return render(request, "chat/about.html")

@never_cache
@login_required
def new_room(request,*args,**kwargs):
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
    return redirect("chat_room", label=label)

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

