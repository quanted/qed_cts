# from __future__ import absolute_import

# In consumers.py
import logging
from channels import Group

from channels.generic.websockets import JsonWebsocketConsumer
import os
import time
import json

# from cts_app.cts_calcs import smilesfilter  # adding this including only jchem_rest and jchem_calculator from chemaxon_cts... what does that even mean??
# from cts_app.cts_calcs import data_walks
from cts_app.cts_calcs import chemaxon_cts
# from cts_app.cts_calcs import smilesfilter, data_walks, calculator  # adding this including only jchem_rest and jchem_calculator from chemaxon_cts... what does that even mean??

logging.warning("CHEMAXON DIR: {}".format(dir(chemaxon_cts)))


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


def ws_request_consumer(message, service):
    """
    message type from django channels
    service - calc name for p-chem data, metabolizer, speciation
    """

    logging.info("incoming message to channels channel: {}".format(message))
    post_request = message.content  # expecting json request for channels pchem data

    logging.warning("arg: {}".format(service))
    logging.warning("message: {}".format(message.content))

    # get sessionid:
    sessionid = message.content['reply_channel'].split('!')[1]  # ID after "!" in reply ch.
    logging.warning("sessionid: {}".format(sessionid))


    service_request = json.loads(message.content['text'])  # incoming json string

    # calc_obj = calculator.Calculator()
    # calc_obj.process_ws_request(service_request)  # populates calc_obj.calc_request
    # logging.warning("REQUEST OBJ: {}".format(calc_obj.calc_request))


    # before trying the full pchem request, try a hardcoded one for chemaxon:

    message.reply_channel.send({'text': ''})

    # user_jobs = []  # still track user job IDs?
    # job_id = pchem_request_handler(sessionid, calc_obj.calc_request)

    # pchem_response = channels_cts.worker.request_manager({'this': 'is', 'not': 'real'})
    message.reply_channel.send({'text': 'channels worker made p-chem request to {}'.format(service)})


def pchem_request_handler(sessionid, data_obj):

    if 'cancel' in message.content['text']:
        # still need this remove user jobs from queue condition?
        logging.warning("cancel request received at consumers.py")
        return

    user_jobs = []  # still track user job IDs?

    if 'nodes' in message.content['text']:
        for node in data_obj['nodes']:
            node_obj = data_obj['nodes'][node]
            data_obj['node'] = node_obj
            data_obj['chemical'] = node_obj['smiles']
            jobID = parse_pchem_request(sessionid, data_obj)
    else:
        jobID = parse_pchem_request(sessionid, data_obj)


def parse_pchem_request(sessionid, data_obj):
    """
    python version of cts_nodejs's node_server.js
    function: pchemRequestHandler
    """
    for calc_name, props_list in data_obj['pchem_request'].items():

        data_obj['calc'] = calc_name
        # data_obj['props'] = data_obj['pchem_request'][calc_name]
        data_obj['props'] = props_list
        data_obj['sessionid'] = sessionid

        if calc_name == 'chemaxon':
            # client.call('tasks.chemaxonTask', [data_obj])
            # make request to calc worker?
            pass
        elif calc_name == 'sparc':
            # client.call('tasks.sparcTask', [data_obj]);   
            # make request to calc worker?
            pass
        elif calc_name == 'epi':
            # client.call('tasks.epiTask', [data_obj]);   
            # make request to calc worker?
            pass
        elif calc_name == 'test':
            # client.call('tasks.testTask', [data_obj]);   
            # make request to calc worker?
            pass
        elif calc_name == 'measured':
            # client.call('tasks.measuredTask', [data_obj]);   
            # make request to calc worker?
            pass

    return sessionid;


# def ws_pchem_request(message):
#   # assuming p-chem request from single user.
#   # parse out request to workers..
#   check_mess = message;
#   message.reply_channel.send({
#       # "text": message.content['text'],
#       "text": "hello, this is pchem channel",
#   })


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