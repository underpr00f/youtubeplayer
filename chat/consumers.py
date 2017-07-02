import json
from channels import Channel
from channels.auth import channel_session_user_from_http, channel_session_user

from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER, NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS
from .models import Room, Message
from .utils import get_room_or_error, catch_client_error
from .exceptions import ClientError

from channels.sessions import channel_session
import logging
log = logging.getLogger(__name__)

#set data in chat messages
from django.utils import timezone
now = str(timezone.now().strftime('%d %m %Y %H:%M:%S'))

### WebSocket handling ###


# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({'accept': True})
    # Initialise their session
    message.channel_session['rooms'] = []


# Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# of its own with a few attributes extra so we can route it
# This doesn't need @channel_session_user as the next consumer will have that,
# and we preserve message.reply_channel (which that's based on)
@channel_session
@channel_session_user
def ws_receive(message):
    # All WebSocket frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this encoding/decoding
    # for you as well as handling common errors.
  
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)




@channel_session_user
def ws_disconnect(message):
    # Unsubscribe from any connected rooms
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = Room.objects.get(pk=room_id)
            # Removes us from the room's send group. If this doesn't get run,
            # we'll get removed once our first reply message expires.
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass


### Chat channel handling ###


# Channel_session_user loads the user out from the channel session and presents
# it as message.user. There's also a http_session_user if you want to do this on
# a low-level HTTP usernamer, or just channel_session if all you want is the
# message.channel_session object without the auth fetching overhead.
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
    #recent_msgs = Message.objects.filter(room=room.id).order_by(ChatModelFields.CREATED_AT)[:10]
    recent_msgs = Message.objects.filter(room=room.id).order_by('-timestamp')[:10]
    # Send a message back that will prompt them to open the room
    # Done server-side so that we could, for example, make people
    # join rooms automatically.
    history = []
    for msg in recent_msgs:
        history.append({
            'message': msg.message,
            'username': msg.username,
            'messageid': msg.id,
            'timestamp': str(msg.timestamp),
            'avatar': msg.image_url,
            #'user': msg.user,
            #'room': msg.room,
            })
        
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.title,
            "history": history,
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
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
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
    if int(message['room']) not in message.channel_session['rooms']:
        raise ClientError("ROOM_ACCESS_DENIED")
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
            'username': msg.username,
            'messageid': msg.id,
            #'now': msg.timestamp,
            #'user': msg.user,
            #'room': msg.room,
            })
    
    message.reply_channel.send({
        "text": json.dumps({
            #"join": str(room.id),
            #"title": room.title,
            "history": history,
        }),
    })
    

from channels.generic.websockets import JsonWebsocketConsumer



@channel_session_user_from_http
def wsock_connect(message):
    Group('list_rooms').add(message.reply_channel)
    Group('list_rooms').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': True
        })
    })

'''
@channel_session
def wsock_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        title = message.channel_session['room']
        room = Room.objects.get(title=title)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('recieved message, buy room does not exist title=%s', title)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return
    
    if set(data.keys()) != set(('username', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s username=%s message=%s', 
            room.title, data['username'], data['message'])
        m = room.messages.create(**data)

        # See above for the note about Group
        Group('chat-'+title, channel_layer=message.channel_layer).send({'text': json.dumps(m)})
'''
@channel_session_user
def wsock_disconnect(message, title):
    Group('list_rooms').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False
        })
    })
    Group('list_rooms').discard(message.reply_channel)
