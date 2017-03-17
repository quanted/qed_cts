# from __future__ import absolute_import

# In consumers.py
import logging
from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer
import os
import time
import json

from cts_app import cts_calcs
# from cts_app.cts_calcs import worker_chemaxon
from cts_app.cts_calcs import calculator

logging.warning("CHEMAXON DIR: {}".format(dir(cts_calcs)))


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


def ws_request_consumer(message):
    """
    message type from django channels
    service - calc name for p-chem data, metabolizer, speciation
    """

    logging.info("incoming message to channels channel: {}".format(message))
    post_request = message.content  # expecting json request for channels pchem data

    # logging.info("arg: {}".format(service))
    logging.info("message: {}".format(message.content))

    # get sessionid:
    sessionid = message.content['reply_channel'].split('!')[1]  # ID after "!" in reply ch.
    logging.info("sessionid: {}".format(sessionid))

    service_request = json.loads(message.content['text'])  # incoming json string

    # request_handler(sessionid, service_request)
    request_handler(sessionid, message)

    # calc = service_request['calc']  # calc name, speciation, or transformation products

    # calc_obj = calculator.Calculator(calc)  # if service recognized, get sub class instance
    # response_dict = calc_obj.request_logic(service_request, message)

    # message.reply_channel.send({'text': json.dumps(response_dict)})  # push to client


def request_handler(sessionid, data_obj):

    if 'cancel' in data_obj:
        # still need this remove user jobs from queue condition?
        logging.warning("cancel request received at consumers.py")
        return

    user_jobs = []  # still track user job IDs?

    if 'nodes' in data_obj:
        for node in data_obj['nodes']:
            node_obj = data_obj['nodes'][node]
            data_obj['node'] = node_obj
            data_obj['chemical'] = node_obj['smiles']
            job_id = parse_request(sessionid, data_obj, message)
    else:
        job_id = parse_request(sessionid, data_obj, message)


def parse_request(sessionid, data_obj, message):

    if data_obj['service'] == 'getSpeciationData' or data_obj['service'] == 'getTransProducts':
        data_obj['sessionid'] = sessionid
        # client.call('tasks.chemaxonTask', [data_obj])
        response_dict = calc_obj.request_logic(data_obj, message)
        return sessionid
    else:
        parse_pchem_request(sessionid, data_obj, client)
        return sessionid


def parse_pchem_request(sessionid, data_obj, message):
    """
    python version of cts_nodejs's node_server.js
    function: pchemRequestHandler
    """
    for calc_name, props_list in data_obj['pchem_request'].items():

        data_obj['calc'] = calc_name
        data_obj['props'] = props_list
        data_obj['sessionid'] = sessionid

        # calc_obj = calculator.Calculator(calc_name)  # get calc-specific class object

        response_dict = calc_obj.request_logic(data_obj, message)  # parsed request sent to calc server(s)

        # message.reply_channel.send({'text': json.dumps(response_dict)})  # push to client

    return sessionid