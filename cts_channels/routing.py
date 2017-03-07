from channels.routing import route, route_class
# from cts_channels.consumers import ws_add, ws_message, ws_disconnect, ws_pchem_request, chemaxon_channel
from cts_channels import consumers

channel_routing = [
    route("websocket.connect", consumers.ws_add),
    route("websocket.disconnect", consumers.ws_disconnect),
    # route("websocket.receive", consumers.chemaxon_channel, path=r"^/channel/chemaxon/?$"),
    # route("websocket.receive", consumers.sparc_channel, path=r"^/channel/sparc/?$"),
    # route_class(consumers.ChemaxonConsumer, path=r"^/chemaxon/"),
    # route("websocket.receive", consumers.worker_channels, path=r'^/channel/(?P<calc>.*?)'),
    
    # allows strings that are alphanumeric, underscore, or slugs:
    # ??? Will having one route for calcs bottleneck ???
    # ??? Is a bottleneck prevented with assigning workers to specific paths ???
    # ??? Is it possible to assign workers to specific paths, or does it have
    # to be with channel names ???
    route("websocket.receive", consumers.worker_channels, path=r'^/channels/(?P<service>[\w\-]+)/?$'),
]