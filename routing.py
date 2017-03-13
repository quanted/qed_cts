from channels.routing import route, route_class
from consumers import ws_add, ws_disconnect, ws_request_consumer

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.disconnect", ws_disconnect),
    # route("websocket.receive", consumers.ws_request_consumer, path=r'^/channels/(?P<service>[\w\-]+)/?$'),
    route("websocket.receive", ws_request_consumer, path=r'^/channels/?$'),
]