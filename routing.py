from channels.routing import route, route_class
from channels import include
from consumers import ws_add, ws_disconnect, ws_receive, chemaxon_channel, sparc_channel, epi_channel, test_channel, measured_channel


# You can have as many lists here as you like, and choose any name.
# Just refer to the individual names in the include() function.
# SOURCE: https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/routing.py
calcs_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    route("chemaxon.receive", chemaxon_channel),
    # route("sparc.receive", sparc_channel),
    # route("epi.receive", epi_channel),
    # route("test.receive", test_channel),
    # route("measured.receive", measured_channel),
]

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.disconnect", ws_disconnect),
    route("websocket.receive", ws_receive),
    
    include(calcs_routing)  # include below custom routing
]