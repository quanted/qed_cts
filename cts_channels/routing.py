from channels.routing import route
from cts_channels.consumers import ws_add, ws_message, ws_disconnect, ws_pchem_request, chemaxon_channel

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message, path=r"^/chat/"),
    route("websocket.disconnect", ws_disconnect),
    route("websocket.receive", ws_pchem_request, path=r"^/pchem/"),
    route("websocket.receive", chemaxon_channel, path=r"^/chemaxon/"),
]