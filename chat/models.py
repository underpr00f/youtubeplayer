from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .settings import MSG_TYPE_MESSAGE


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.label

    '''
    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )
    '''
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField(blank=True, null=True, default="Anonimous")
    #user = models.OneToOneField(User)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

        
    def __str__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%d %m %Y %H:%M:%S')

    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}
