# In consumers.py
import logging
from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer
import os
import time
import json


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


def worker_channels(message, service):
    """
    message type from django channels
    service - calc name for p-chem data, metabolizer, speciation
    """
    logging.info("incoming message to channels channel: {}".format(message))
    post_request = message.content  # expecting json request for channels pchem data
    # return channels_worker.request_manager(request)

    logging.warning("arg: {}".format(service))
    logging.warning("message: {}".format(message.content))

    
    # ??? Can there be multple workers that consume this same function, but
    # each worker only consumes certain requests based on "calc" arg ???

    # Do the workers even need to be separated by calc? (probably not)
    time.sleep(5)  # sleep 5s, checking for parllel worker consumption of same function/route


    # p-chem request would go here
    


    # pchem_response = channels_cts.worker.request_manager({'this': 'is', 'not': 'real'})
    message.reply_channel.send({'text': 'channels worker made p-chem request to {}'.format(calc)})

# def ws_pchem_request(message):
# 	# assuming p-chem request from single user.
# 	# parse out request to workers..
# 	check_mess = message;
# 	message.reply_channel.send({
# 		# "text": message.content['text'],
# 		"text": "hello, this is pchem channel",
# 	})


# def chemaxon_channel(message):
#     logging.info("incoming message to chemaxon channel: {}".format(message))
#     post_request = message.content  # expecting json request for chemaxon pchem data
#     # return chemaxon_worker.request_manager(request)

#     # this is where the call would go to cts_api rest endpoint


#     # pchem_response = chemaxon_cts.worker.request_manager({'this': 'is', 'not': 'real'})
#     message.reply_channel.send({'text': 'chemaxon worker made p-chem request'})


# def sparc_channel(message):
#     logging.info("incoming message to sparc channel: {}".format(message))
#     post_request = message.content  # expecting json request for sparc pchem data
#     # return sparc_worker.request_manager(request)

#     # this is where the call would go to cts_api rest endpoint


#     # pchem_response = sparc_cts.worker.request_manager({'this': 'is', 'not': 'real'})
#     message.reply_channel.send({'text': 'sparc worker made p-chem request'})


# # Generic Consumer: JSON-enabled WebSocket Class
# class ChemaxonConsumer(JsonWebsocketConsumer):

#     # set to True for ordering:
#     strict_ordering = False

#     method_mapping = {
#         'channel_chemaxon': 'method name'
#     }

#     def connection_groups(self, **kwargs):
#         """
#         Called to return the list of groups to automatically add/remove
#         this connection to/from.
#         """
#         return ["test"]

#     def connect(self, **kwargs):
#         """
#         Perform things on connection start
#         """
#         pass

#     def receive(self, content, **kwargs):
#         """
#         Called when a message is received with decoded JSON content
#         """
#         self.send(content)  # simple echo (self.send auto encodes JSON)

#     def disconnect(self, message, **kwargs):
#         """
#         Perform things on connection close
#         """
#         pass