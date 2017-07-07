from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Message, PrivRoom
from socialprofile.models import SocialProfile

import random
import string
from django.db import transaction
from haikunator import Haikunator
from django.views.decorators.cache import never_cache
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse

from django.template.response import TemplateResponse

from django.contrib.auth.models import User

from django.utils import timezone
haikunator = Haikunator()


@never_cache
@login_required
def index(request, *args,**kwargs):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")
    #users = User.objects.all()
    
    messages = reversed(Message.objects.order_by('-timestamp')[:50])
    #messages = reversed(Message.objects.all().values("room__title","username","message","timestamp","user__id",).order_by('-timestamp')[:50])
    #profile = SocialProfile.objects.get(pk=Message.user)
    
    #messages = reversed(rooms.messages.order_by('-timestamp')[:50])
    # Render that in the index template
    return render(request, "indexchat.html", {
        "rooms": rooms,
        "messages": messages,
        #"profile": profile,
    })


@never_cache
@login_required
def new_room(request,*args,**kwargs):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            title = haikunator.haikunate()
            if Room.objects.filter(title=title).exists():
                continue
            new_room = Room.objects.create(title=title)
    
    #rooms = Room.objects.order_by("title")

    return render(request, "new_room.html", {
        "new_room": new_room
        #"rooms": rooms,
        #"messages": messages,
        #"profile": profile,
    })

@never_cache
@login_required
def new_room_private(request,*args,**kwargs):


    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")
    users = User.objects.order_by("username")
    if request.method == 'POST':

        #group_name = request.POST.get('group_name', None)
        search_id = request.POST.get('user_name', None)

        try:
            #user1 = User.objects.filter(username__contains = search_id)
            '''
            groupname = PrivRoom.objects.order_by("title")
            if group_name == groupname.title:
                groupName = "this name is used"
            else:
                groupName = group_name
            '''
            #groupName = group_name 
                
            user1 = User.objects.get(username__exact = search_id)
            #do something with user
            #html = ("<H1>%s</H1>", user1)
            #return user1
            #return HttpResponse(user1)
            return TemplateResponse(request, 'new_room_private.html', {
                'rooms': rooms, 'user1': user1,
                })

            
        except: 
            user1 = "no such user"
            
            #return user1

            #return HttpResponse("no such user")
            '''
            return render_to_response(
                "new_room_private.html", {
                    "rooms": rooms,
                    "user1": user1,
                    }
                )
            '''
            return TemplateResponse(request, 'new_room_private.html', {
                'rooms': rooms, 'user1': user1, 
                })

    '''
        get_text = request.POST.get("user_name", None)
    else:
        get_text = None
    '''

        

    # Render that in the index template
    return render(request, "new_room_private.html", {
        "rooms": rooms,
        #"user1": user1,
        #"get_text": get_text,
          
    })

from django.views.generic import DeleteView, TemplateView
from django.conf import settings
from .forms import PrivateRoomForm
import logging
from django.contrib import messages

LOGGER = logging.getLogger(name='chat')
DEFAULT_RETURNTO_PATH = getattr(settings, 'DEFAULT_RETURNTO_PATH', '/')
class PrivateGroupView(TemplateView):

    
    template_name = 'new_privateroom_edit.html'

    http_method_names = {'get'}
    
    def get(self, title, request, *args, **kwargs):
        
        pg_form = PrivateRoomForm()
        query = request.GET.get("q")

        if query:
            queryset_list = User.objects.filter(username=query)
        else:
            queryset_list = None

        context = {'pg_form': pg_form,
                   #'users': users,
                   #'friends': friends,
                   #'drugs': drugs,
                   'object_list': queryset_list,
                   #'true_friends': true_friends,
                   #'friendlist': friendlist,
                   }
        return render(request,self.template_name, context)
    
    """


    def get_context_data(self, **kwargs):
        
        LOGGER.debug("chat.views.PrivateGroupView.get_context_data")
        title = self.kwargs.get('title')


        if title:
            user = get_object_or_404(User)
        elif self.request.user.is_authenticated():
            user = self.request.user
        else:
            raise Http404  # Case where user gets to this view anonymously for non-existent user

        #return_to = self.request.GET.get('returnTo', DEFAULT_RETURNTO_PATH)

        pg_form = PrivateRoomForm(instance=title)
        #user_form = UserForm(instance=user)

        #sp_form.initial['returnTo'] = return_to

        return {'pg_form': pg_form,
                #'user_form': user_form
                }
    """
class PrivateGroupEditView(PrivateGroupView):
    """
    Profile Editing View

    url: /profile/edit
    """

    template_name = 'new_room_private.html'

    http_method_names = {'get', 'post'}

    def get(self, request, *args, **kwargs):
        
        pg_form = PrivateRoomForm()
        query = request.GET.get("q")

        if query:
            queryset_list = User.objects.filter(username=query)
        else:
            queryset_list = None

        context = {'pg_form': pg_form,
                   #'users': users,
                   #'friends': friends,
                   #'drugs': drugs,
                   'object_list': queryset_list,
                   #'true_friends': true_friends,
                   #'friendlist': friendlist,
                   }
        return render(request,self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        pg_form = PrivateRoomForm(request.POST,instance=request.user)
        
        if pg_form.is_valid():
            title = pg_form.cleaned_data['title']
            
            #check checkbox for private
            if request.POST.get('private', False):
                privroom = PrivRoom.objects.create(current_user=request.user)
            else: 
                privroom = Room.objects.create(title=title)
            #private_room=PrivRoom.objects.get(id=privroom.id)
            pg_form = PrivateRoomForm(request.POST,instance=privroom)
            #privroom = Privroom.objects.(title=request.POST.get('new_room_private',''))
            #privrooms = privroom.members.all()
            #PrivRoom.title = request.POST.get('new_room_private')
                        
            pg_form.save()
            #messages.add_message(self.request, messages.INFO, _('Ваш профиль успешно изменен.'))
            return HttpResponseRedirect(pg_form.cleaned_data.get('returnTo', DEFAULT_RETURNTO_PATH))
        else:
            #messages.add_message(self.request, messages.INFO, _('Ваш профиль не изменен.'))
            return self.render_to_response({'pg_form': pg_form,
                                            #'object_list': queryset_list
                                            #'user_form': user_form
                                            })
        return render(request, template_name, {'pg_form': pg_form})

@never_cache
@login_required
def change_members(request, operation, pk):
    roomfriend = User.objects.get(pk=pk)
    if operation == 'add':
        PrivRoom.make_roomfriend(request.user, roomfriend)
    elif operation == 'remove':
        PrivRoom.remove_roomfriend(request.user, roomfriend)
    return redirect('new_room_private')
    
#correct chat
@never_cache
@login_required
def chat_room(request, title, *args,**kwargs):
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).

    room = Room.objects.get(title=title)
    # show id of required room
    roomobj = Room.objects.filter(title=title).values_list('id', flat=True).first()
  
    #get messages from this room
    messages = reversed(Message.objects.filter(room_id=roomobj).order_by('-timestamp')[:50])
    

    return render(request, "room.html", {
        'room': room,
        'roomobj': roomobj,
        'messages': messages,
        
    })    

from django.contrib.auth import get_user_model
User = get_user_model()

@never_cache
@login_required
def chat_list_rooms(request):


    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    #check for user status
    users = User.objects.select_related('logged_in_user')
    for user in users:
        user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
    
    return render(request, "list_rooms.html", {
        "rooms": rooms,
        'users': users,
    })

