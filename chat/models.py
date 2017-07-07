import json
from django.db import models
from django.utils.six import python_2_unicode_compatible
from channels import Group
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from .settings import MSG_TYPE_MESSAGE
from django.contrib.auth.models import User
#from socialprofile.models import SocialProfile

from django.db.models.signals import post_save
#from json import dumps
from django.utils import timezone
from django.conf import settings
#timezone.activate(tz)
'''
user = User.objects.get(id=user.id)
message.user = user
'''
@python_2_unicode_compatible
class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)

    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    

    

    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        recent_msgs = Message.objects.filter(room=self.id).order_by('-timestamp')[:10]
        
        history = []
        
        for msg in recent_msgs:
            history.append({
                'message': msg.message,
                'username': msg.username,
                'messageid': msg.id,
                'timestamp': str(msg.timestamp),
                'avatar': msg.image_url,

                })
    

        
        """
        Called to send a message to the room on behalf of a user.
        """
        if user.social_profile.avatar:
            img = settings.MEDIA_URL + str(user.social_profile.avatar)
        elif user.social_profile.image_url:
            img = user.social_profile.image_url
        else:
            img = 'http://www.gravatar.com/avatar/00000000000000000000000000000000?d=mm'

        #set final_msg (check for new chat without messages) -
        #'msgid': history[0]["messageid"]+1 give typeerror in empty chat
        if not history:
            final_msg = {'room': str(self.id), 'message': message,
                     'username': user.username, 'msg_type': msg_type, 'now': now,
                     'user': user.id, 'avatar': img, 'history': history,
                     'msgid': 1,
                     }
        else:
            final_msg = {'room': str(self.id), 'message': message,
                     'username': user.username, 'msg_type': msg_type, 'now': now,
                     'user': user.id, 'avatar': img, 'history': history,
                     'msgid': history[0]["messageid"]+1,
                     }
        
        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )
        if final_msg['message'] is not None:
            if final_msg['message'] != "":
                messages = get_object_or_404(Room, id=final_msg["room"]) #уходим от ошибки must be a "User" instance.
                users = get_object_or_404(User, id=final_msg["user"])
                com = Message()
                com.room = messages #уходим от ошибки must be a "User" instance.
                com.user = users
                com.message = final_msg['message']
                com.username = final_msg['username']
                com.timestamp = final_msg['now']
                com.image_url = final_msg['avatar']
                #com.user = final_msg['user']
                com.save()
    '''
    def new_room(request,*args,**kwargs):
        """Randomly create a new room, and redirect to it."""
        new_room = None
        while not new_room:
            with transaction.atomic():
                title = haikunator.haikunate()
                if Room.objects.filter(title=title).exists():
                    continue
                new_room = Room.objects.create(title=title)
    '''
    '''
    def create_room(self, title):
        """
        Create a ``RegistrationProfile`` for a given user, and return
        the ``RegistrationProfile``.

        """
        title = str(getattr(user, User.USERNAME_FIELD))
            return self.create(title=title)
        #User = get_user_model()
        #username = str(getattr(user, User.USERNAME_FIELD))
        #hash_input = (get_random_string(5) + username).encode('utf-8')
        #activation_key = hashlib.sha1(hash_input).hexdigest()
        #return self.create(user=user,
                           #activation_key=activation_key)
    '''
        
            

class Message(models.Model):

    
    room = models.ForeignKey(Room, related_name='messages') #related_name='messages' уходим от ошибки must be a "User" instance.
    username = models.TextField(blank=True, null=True, default="Anonimous")
    #user = models.OneToOneField(User)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    user = models.ForeignKey(User, default=None, related_name='users')
    image_url = models.URLField(blank=True, null=True, max_length=500, default='http://www.gravatar.com/avatar/00000000000000000000000000000000?d=mm')
    


    '''    
    def __str__(self):
        return str(self.pk)
    
    @property
    def avatar(self):
        return SocialProfile.objects.get(pk=self.user)
        
    def as_dict(self, message, user):
        return {'username': self.username, 'message': self.message, 'timestamp': self.formatted_timestamp}
    '''

class PrivRoom(models.Model):
    title = models.CharField(u"Название", max_length=255)
    private = models.BooleanField(default=False, verbose_name=_("Приватность"))
    #members = models.ManyToManyField(User)
    #description = models.TextField(blank=True, null=True, verbose_name=_("Описание"), help_text=_("Расскажите о себе!"))
    #manually_edited = models.BooleanField(default=False)
    members = models.ManyToManyField(User, verbose_name=_("Участники"))
    current_user = models.ForeignKey(User, related_name='changeowner', null=True)
    
    
    def __str__(self):
        return self.title
    
    class Meta(object):
        ordering = ['title']

    #add roomfriend
    @classmethod
    def make_roomfriend(cls,current_user, new_roomfriend):
        privroom, created = cls.objects.get_or_create(
            current_user=current_user
            )
        privroom.members.add(new_roomfriend)

    #remove roomfriend
    @classmethod
    def remove_roomfriend(cls,current_user, new_roomfriend):
        privroom, created = cls.objects.get_or_create(
            current_user=current_user
            )
        privroom.members.remove(new_roomfriend)

def create_priv_room(sender, instance, created, **kwargs):
    """Creates a UserProfile Object Whenever a User Object is Created"""
    if created:
        PrivRoom.objects.create(title=instance)


post_save.connect(create_priv_room, sender=User)



'''
    def new_room(request,*args,**kwargs):
        """Randomly create a new room, and redirect to it."""
        new_room = None
        while not new_room:
            with transaction.atomic():
                title = request.POST.get('group_name', None) 
                if PrivRoom.objects.filter(title=title).exists():
                    continue
                new_room = PrivRoom.objects.create(title=title)
'''
class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='logged_in_user')


