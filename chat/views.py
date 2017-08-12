import random
import string
from django.db import transaction
from django.shortcuts import render, redirect
from haikunator import Haikunator
from .models import Room, Member, MemberAccept
from django.views.decorators.cache import never_cache
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .forms import FriendForm, LabelForm


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


    def get(self, request, pk, *args, **kwargs):
        
        room = Member.objects.get(pk=pk)
        if request.user.id == room.current_user_id:
            form = FriendForm()
            users = User.objects.exclude(id=request.user.id)

            query = request.GET.get("q")

            true_members=[]
        

            if query:
                queryset_list = User.objects.filter(username=query)
            else:
                queryset_list = None

            #your followers
            drugs = room.who_added_user(request.user)
            memberlist = []
        
            member, created = Member.objects.get_or_create(current_user=request.user, pk=pk)
            members = member.users.all()

        
        

            for member in members:
                memberlist.append(member)
                
                for drug in drugs:
                 
                    if drug.pk == member.pk:
                        true_members.append(drug)
                        drugs.remove(drug)
                        memberlist.remove(drug)
            
                


            context = {'form': form, 'users': users,
                   'members': members,
                   'drugs': drugs,
                   'object_list': queryset_list,
                   'true_members': true_members,
                   'memberlist': memberlist,
                   'room': room,
                   }
            return render(request,self.template_name, context) 
        else:
            return redirect('home')       

@never_cache
@login_required
def change_members(request, pk, operation, pkid):
    
    member = User.objects.get(pk=pkid)
    label = Member.objects.get(pk=pk)
    if operation == 'add':
        Member.make_member(request.user, label, member)
        MemberAccept.objects.get_or_create(accepter=member,acceptroom=label,agree=False)
        return redirect('chat_index:private_room', pk = pk)
    elif operation == 'remove':
        Member.remove_member(request.user, label, member)
        return redirect('chat_index:private_room', pk = pk)
    return redirect('chat_index:private_room', pk = pk)


from django.contrib import messages
@never_cache
@login_required
def get_name(request):
    #template_name = "chat/title_room.html"
    new_room = None
    form = LabelForm(request.POST or None)
    
    if request.method == 'POST':
        '''
        while not new_room:
            query = request.POST.get("label")
            userid = request.user.id
            #checkmember = Member.objects.filter(current_user_id=userid)
            new_room = Member.objects.create(label=query, current_user_id=userid)
        '''

        #form = LabelForm(request.POST)
        if form.is_valid():
            query = request.POST.get("label")
            userid = request.user.id
            new_room = Member.objects.create(label=query, current_user_id=userid)
            return HttpResponseRedirect('/chat/private/%s/' % new_room.id)

        else:
            render(request, 'chat/title_room.html', {'form': LabelForm()})
    #else:
        #form = LabelForm()
    # if a GET (or any other method) we'll create a blank form
    

    return render(request, 'chat/title_room.html', {'form': form})


@never_cache
@login_required
def select_room(request, *args,**kwargs):

    list_room = []
    rooms = Member.objects.all()
    room_members = MemberAccept.objects.filter(accepter=request.user.id, agree=True)
    userinrooms = Member.objects.filter(users__id = request.user.id)
    for userinroom in userinrooms:
        for room_member in room_members:
            if room_member.acceptroom.pk == userinroom.pk:
                list_room.append(room_member.acceptroom.label)

    
    return render(request, "chat/select_room.html", {
        'rooms': rooms,
        'room_members': room_members,
        'userinrooms': userinrooms,
        'list_room': list_room
        
    })



@never_cache
@login_required
def accept_members(request, pk, operation, pkid):
    
    accepter = User.objects.get(pk=pkid)
    acceptroom = Member.objects.get(pk=pk)
    if operation == 'agree':
        MemberAccept.objects.get_or_create(accepter=accepter,acceptroom=acceptroom,agree=True)
        return redirect('chat_index:select_room')
    elif operation == 'disagree':
        Member.remove_member(request.user, label, member)
        return redirect('chat_index:private_room', pk = pk)
    return redirect('chat_index:select_room')
