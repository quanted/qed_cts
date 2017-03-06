# In consumers.py
import logging

from channels import Group
# from cts_channels.cts_calcs import chemaxon_cts  # works, but no content within chemaxon_cts...
# from cts_calcs import chemaxon_cts  # import error doing it this way
# from cts_app.cts_calcs import chemaxon_cts  # works, also not content in chemaxon_cts/
# from qed_cts.cts_app.cts_calcs import chemaxon_cts
# from qed_cts.cts_channels.cts_calcs import chemaxon_cts
# from cts_channels import cts_calcs
from cts_channels.cts_calcs import chemaxon_cts

# logging.warning("CTS_CALCS: {}".format(dir(cts_calcs)))

import os


logging.warning("JCHEM VAL: {}".format(os.environ.get('CTS_JCHEM_SERVER')))
logging.warning("CHEMAXON_CTS CONTENTS: {}".format(dir(chemaxon_cts)))

# chemaxon_worker = chemaxon_cts.worker


def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    message.reply_channel.send({
        "text": message.content['text'],
    })

# Connected to websocket.connect
def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("chat").add(message.reply_channel)

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)

def ws_pchem_request(message):
	# assuming p-chem request from single user.
	# parse out request to workers..
	check_mess = message;
	message.reply_channel.send({
		# "text": message.content['text'],
		"text": "hello, this is pchem channel",
	})


# @app.task
# def chemaxon_channel(request_post):
#     request = NotDjangoRequest()
#     request.POST = request_post
#     logging.info("Request: {}".format(request_post))
#     return chemaxon_worker.request_manager(request)
def chemaxon_channel(message):
    logging.info("incoming message to chemaxon channel: {}".format(message))
    post_request = message.content  # expecting json request for chemaxon pchem data
    # return chemaxon_worker.request_manager(request)
    pchem_response = chemaxon_cts.worker.request_manager({'this': 'is', 'not': 'real'})
    message.reply_channel.send({'text': 'chemaxon worker made p-chem request'})


# Do I need a custom channel? A connected user establishes a new channel
# automatically, which I'm assuming can all use the same channel functions...