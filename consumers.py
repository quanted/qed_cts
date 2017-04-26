# from __future__ import absolute_import

# In consumers.py
import logging
from channels import Group, Channel
# from channels.sessions import channel_session
import os
import time
import json

# from cts_app import cts_calcs
# from cts_app.cts_calcs import worker_chemaxon
from cts_app.cts_calcs.calculator import Calculator
from cts_app.cts_calcs.calculator_chemaxon import JchemCalc
from cts_app.cts_calcs.calculator_epi import EpiCalc
from cts_app.cts_calcs.calculator_measured import MeasuredCalc
from cts_app.cts_calcs.calculator_test import TestCalc
from cts_app.cts_calcs.calculator_sparc import SparcCalc
from cts_app.cts_calcs.calculator_metabolizer import MetabolizerCalc

# import celery_tasks

# logging.warning("CHEMAXON DIR: {}".format(dir(cts_calcs)))


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



# Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# of its own with a few attributes extra so we can route it
# This doesn't need @channel_session_user as the next consumer will have that,
# and we preserve message.reply_channel (which that's based on)
def ws_receive(message):
    # All WebSocket frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this encoding/decoding
    # for you as well as handling common errors.
    try:
        payload = json.loads(message.content['text'])
    except Exception as e:
        logging.warning("Exception serializing payload in consumers.py: {}".format(e))
        raise  # TODO: a different escape plan

    payload['reply_channel'] = message.content['reply_channel']
    payload['sessionid'] = message.content['reply_channel'].split('!')[1]  # ID after "!" in reply ch.
    payload['channel_name'] = message.reply_channel.name

    if 'cancel' in payload:
        # still need this remove user jobs from queue condition?
        # TODO: Canceling jobs on worker servers in Django Channels
        logging.warning("cancel request received at consumers.py")
        return

    if payload.get('calc') == 'chemaxon':
        Channel("chemaxon.receive").send(payload)  # send chemaxon request to chemaxon channel
    elif payload.get('calc') == 'sparc':
        Channel('sparc.receive').send(payload)
    elif payload.get('calc') == 'epi':
        Channel('epi.receive').send(payload)
    elif payload.get('calc') == 'test':
        Channel('test.receive').send(payload)
    elif payload.get('calc') == 'measured':
        Channel('measured.receive').send(payload)

# @channel_session
def chemaxon_channel(payload):
    _response_data = JchemCalc().data_request_handler(payload.content)
    payload.reply_channel.send({'text': json.dumps(_response_data)})

# @channel_session
def sparc_channel(payload):
    _response_data = SparcCalc().data_request_handler(payload.content)
    payload.reply_channel.send({'text': json.dumps(_response_data)})

def epi_channel(payload):
    _response_data = EpiCalc().data_request_handler(payload.content)
    payload.reply_channel.send({'text': json.dumps(_response_data)})

def test_channel(payload):
    _response_data = TestCalc().data_request_handler(payload.content)
    payload.reply_channel.send({'text': json.dumps(_response_data)})

def measured_channel(payload):
    _response_data = MeasuredCalc().data_request_handler(payload.content)
    payload.reply_channel.send({'text': json.dumps(_response_data)})


# def parse_request_by_calc(payload):
#     """
#     Parsing request up by calculator, sending it
#     to the calc's channel

#     Note: pay attention to how data comes back to client, previously
#     all props came back at once instead of one at a time despite
#     having a message.reply_channel for each prop...
#     """

#     if payload.get('service') == 'getSpeciationData':
#         Channel("chemaxon.receive").send(_payload)
#         return

#     if payload.get('service') == 'getTransProducts':
#         Channel("metabolizer.receive").send(_payload)
#         return

#     for calc_name, props_list in payload['pchem_request'].items():

#         payload['calc'] = calc_name

#         for prop in props_list:

#             logging.info("PROP {} for {} calc".format(prop, calc_name))
#             payload['prop'] = prop

#             is_chemaxon = calc_name == 'chemaxon'
#             is_kow = prop == 'kow_no_ph' or prop == 'kow_wph'

#             if is_chemaxon and is_kow:
#                 for method in JchemCalc().methods:
#                     payload['method'] = method
#                     Channel("chemaxon.receive").send(payload)
#             else:
#                 if calc_name == 'chemaxon':
#                     Channel("chemaxon.receive").send(payload)  # send chemaxon request to chemaxon channel
#                 elif calc_name == 'sparc':
#                     Channel('sparc.receive').send(payload)
#                 elif calc_name == 'epi':
#                     Channel('epi.receive').send(payload)
#                 elif calc_name == 'test':
#                     Channel('test.receive').send(payload)
#                 elif calc_name == 'measured':
#                     Channel('measured.receive').send(payload)