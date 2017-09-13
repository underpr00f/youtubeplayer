from functools import wraps

from .exceptions import ClientError
from .models import Room, MemberAccept


def catch_client_error(func):
    """
    Decorator to catch the ClientError exception and translate it into a reply.
    """
    @wraps(func)
    def inner(message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except ClientError as e:
            # If we catch a client error, tell it to send an error string
            # back to the client on their reply channel
            e.send_to(message.reply_channel)
    return inner


def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    
    if not user.is_authenticated():
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        room = Room.objects.get(pk=room_id)
        
        #Access to writing
        access = False
        if room.private == True:
            memberaccepter = MemberAccept.objects.filter(acceptroom_id=room_id, accepter_id = user.id, agree = True)
            if not memberaccepter:
                if user.id != room.current_user_id:
                    access = False
                else:
                    access = True
            else:
                access = True

    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    # Check permissions
    '''
    if room.staff_only and not user.is_staff:
        raise ClientError("ROOM_ACCESS_DENIED")
    '''
    if access != True:
         
        raise ClientError("ACCESS_DENIED")
        
         
                    
    return room
