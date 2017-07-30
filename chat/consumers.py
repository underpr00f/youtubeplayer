import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
from .models import Room, Message
from channels.auth import channel_session_user_from_http, channel_session_user
from django.contrib.auth.models import User


from channels import Channel
from .utils import get_room_or_error, catch_client_error
from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER, NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS
from .exceptions import ClientError

log = logging.getLogger(__name__)

#Serialize json
def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat().replace('T', ' ')
    else:
        raise TypeError

@channel_session_user_from_http
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    
    message.reply_channel.send({'accept': True})
    try:
        prefix, pk = message['path'].strip('/').split('/')
        #handle = Message.objects.get(handle)
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
        room = Room.objects.get(id=pk)
        #handle = Message.objects.get(handle=handle)
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return
    except Room.DoesNotExist:
        log.debug('ws room does not exist pk=%s', pk)
        return

    log.debug('chat connect room=%s client=%s:%s', 
        room.id, message['client'][0], message['client'][1])
    
    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('chat-'+str(room.id), channel_layer=message.channel_layer).add(message.reply_channel)
    
    message.channel_session['room'] = room.id
    '''#for multichat
    message.reply_channel.send({'accept': True})
    # Initialise their session
    message.channel_session['rooms'] = []
    '''

@channel_session
@channel_session_user
def ws_receive(message):
    
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)
    '''
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        #handle = Message.objects.get(handle=message.user)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('recieved message, buy room does not exist label=%s', label)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        #handle = message.user
        
        dataS = json.loads(message.content['text'])
        dataS = dataS['message']


        handle = message.user.username
        

        data = {'message': dataS, 'handle': handle}
        #mess = Message.objects.get(handle=handle)
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return
    
    if set(data.keys()) != set(('message','handle')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s handle=%s message=%s', 
            room.label, data['handle'], data['message'])
        m = room.messages.create(**data)

        # See above for the note about Group
        Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})
    '''
@channel_session_user
def ws_disconnect(message):
    '''
    try:
        pk = message.channel_session['room']
        room = Room.objects.get(id=pk)
        Group('chat-'+str(room.id), channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass
    
    '''
    #for multichat
    room_id = message.channel_session['room']
    try:
        room = Room.objects.get(pk=room_id)
        # Removes us from the room's send group. If this doesn't get run,
        # we'll get removed once our first reply message expires.
        room.websocket_group.discard(message.reply_channel)
    except Room.DoesNotExist:
        log.debug('ws room does not exist pk=%s', room_id)
        return


@channel_session_user
@catch_client_error
def chat_join(message):
    # Find the room they requested (by ID) and add ourselves to the send group
    # Note that, because of channel_session_user, we have a message.user
    # object that works just like request.user would. Security!
    room = get_room_or_error(message["room"], message.user)

    # Send a "enter message" to the room if available
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_ENTER)

    # OK, add them in. The websocket_group is what we'll send messages
    # to so that everyone in the chat room gets them.
    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
    # Send a message back that will prompt them to open the room
    # Done server-side so that we could, for example, make people
    # join rooms automatically.
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "label": room.label,
        }),
    })

@channel_session_user
@catch_client_error
def chat_leave(message):
    # Reverse of join - remove them from everything.
    room = get_room_or_error(message["room"], message.user)

    # Send a "leave message" to the room if available
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_LEAVE)

    room.websocket_group.discard(message.reply_channel)
    message.channel_session['room'] = room.id
    # Send a message back that will prompt them to close the room
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })

@channel_session_user
@catch_client_error
def chat_send(message):
    # Check that the user in the room
    '''
    if message['room'] not in message.channel_session['rooms']:
        raise ClientError("ROOM_ACCESS_DENIED")
    '''
    # Find the room they're sending to, check perms

    room = get_room_or_error(message["room"], message.user)
    # Send the message along
    room.send_message(message["message"], message.user)
    recent_msgs = Message.objects.filter(room=room.id).order_by('-timestamp')[:10]
    # Send a message back that will prompt them to open the room
    # Done server-side so that we could, for example, make people
    # join rooms automatically.
    history = []
    for msg in recent_msgs:
        history.append({
            'message': msg.message,
            'handle': msg.handle,
            'messageid': msg.id,
            'now': msg.timestamp,
            'avatar': msg.image_url,
            #'user': msg.user,
            #'room': msg.room,
            })
    
    message.reply_channel.send({
        "text": json.dumps({
            #"join": str(room.id),
            #"title": room.title,
            "history": history,
        },
        default=date_handler),
    })
    