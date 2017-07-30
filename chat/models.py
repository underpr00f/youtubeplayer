from __future__ import unicode_literals

from django.db import models

#from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from channels import Group
import json
from .settings import MSG_TYPE_MESSAGE
from django.utils import timezone
from django.shortcuts import get_object_or_404

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.label

    
    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("chat-%s" % self.id)
    
    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        recent_msgs = Message.objects.filter(room=self.id).order_by('-timestamp')[:10]
        history = []

        if user.social_profile.avatar:
            img = settings.MEDIA_URL + str(user.social_profile.avatar)
        elif user.social_profile.image_url:
            img = user.social_profile.image_url
        else:
            img = 'http://www.gravatar.com/avatar/00000000000000000000000000000000?d=mm'

        for msg in recent_msgs:
            history.append({
                'message': msg.message,
                'handle': msg.handle,
                'messageid': msg.id,
                'now': str(msg.timestamp),
                'avatar': msg.image_url,

                })

        if not history:
            final_msg = {'room': str(self.id), 'message': message,
                     'username': user.username, 'msg_type': msg_type, 
                     'now': now,
                     'user': user.id, 
                     'avatar': img, 
                     'history': history,
                     'msgid': 1,
                     }
        else:
            final_msg = {'room': str(self.id), 'message': message,
                     'username': user.username, 'msg_type': msg_type, 
                     'now': now,
                     'user': user.id, 
                     'avatar': img, 
                     'history': history,
                     'msgid': history[0]["messageid"]+1,
                     }
        


        #final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        # Send out the message to everyone in the room
        
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )
        
        if final_msg['message'] is not None:
            if final_msg['message'] != "":
                messages = get_object_or_404(Room, id=final_msg["room"]) #уходим от ошибки must be a "User" instance.
                #users = get_object_or_404(User, id=final_msg["user"])
                com = Message()
                com.room = messages #уходим от ошибки must be a "User" instance.
                #com.user = users
                com.message = final_msg['message']
                com.handle = final_msg['username']
                com.timestamp = final_msg['now']
                com.image_url = final_msg['avatar']
                #com.user = final_msg['user']
                com.save()
    
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField(blank=True, null=True, default="Anonimous")
    #user = models.OneToOneField(User)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    image_url = models.URLField(blank=True, null=True, max_length=500, default='http://www.gravatar.com/avatar/00000000000000000000000000000000?d=mm')
        
    def __str__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}
