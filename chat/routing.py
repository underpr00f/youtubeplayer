from channels import route
from channels.staticfiles import StaticFilesConsumer
from .consumers import ws_connect, ws_receive, ws_disconnect, chat_join, chat_leave, chat_send #wsock_connect, wsock_receive, wsock_disconnect
from .consumers import wsock_connect, wsock_disconnect#, wsock_receive
from channels.routing import route_class

# There's no path matching on these routes; we just rely on the matching
# from the top-level routing. We _could_ path match here if we wanted.
websocket_routing = [
    route("http.request", StaticFilesConsumer()),
    # Called when WebSockets connect
    route("websocket.connect", ws_connect),

    # Called when WebSockets get sent a data frame
    route("websocket.receive", ws_receive),

    # Called when WebSockets disconnect
    route("websocket.disconnect", ws_disconnect),
]

sub_routing = [
    route("http.request", StaticFilesConsumer()),
    # Called when WebSockets connect
    route("websock.connect", wsock_connect),

    # Called when WebSockets get sent a data frame
    #route("websock.receive", wsock_receive),

    # Called when WebSockets disconnect
    route("websock.disconnect", wsock_disconnect),
]

# You can have as many lists here as you like, and choose any name.
# Just refer to the individual names in the include() function.
custom_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    route("chat.receive", chat_join, command="^join$"),
    route("chat.receive", chat_leave, command="^leave$"),
    route("chat.receive", chat_send, command="^send$"),
]
