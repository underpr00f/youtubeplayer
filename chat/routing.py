from channels.staticfiles import StaticFilesConsumer
from . import consumers
from channels import route

channel_routing = {
    # This makes Django serve static files from settings.STATIC_URL, similar
    # to django.views.static.serve. This isn't ideal (not exactly production
    # quality) but it works for a minimal example.
    'http.request': StaticFilesConsumer(),

    # Wire up websocket channels to our consumers:
    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,
}

# You can have as many lists here as you like, and choose any name.
# Just refer to the individual names in the include() function.
custom_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    route("chat.receive", consumers.chat_join, command="^join$"),
    route("chat.receive", consumers.chat_leave, command="^leave$"),
    #route("chat.receive", consumers.chat_send, command="^send$"),
]
