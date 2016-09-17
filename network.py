#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from charge_keyboard import *
import requests
import json

TOKEN = '230906963:AAGD_tKVKN9K58zEBPUVCS5WZvSMxdBqNV8'
URL = ('https://api.telegram.org/bot{0}/').format(TOKEN)
callback = None

offset = 0

def init():
    read_offset()
    requests.get(URL +
    'getUpdates?offset={0}&timeout={1}'.format(offset,0),
    hooks=dict(response=get_updates))

def setPushDataTo(func):
    global callback
    callback = func

def pushDataToDispatcher(data):
    global callback
    callback(data)

def setRoute(func):
    global route
    route = func

def read_offset():
    with open ('config.json', 'r') as f: 
        #r+ means read-write, open the file as f
        global offset
        dict = json.load(f)
        offset = dict.get('offset')

def change_offset(new_offset):
    global offset
    new_offset = str(int(new_offset) + 1)
    offset = new_offset
    with open('config.json', 'w') as f:
        json.dump({"offset": offset}, f)
    read_offset()

def send_message(**kwargs):
    global URL
    payload = {}
    for key, value in kwargs.items():
        payload[key] = value
    req = requests.post(URL + 'sendMessage', json=payload)
    return(req.json())

def edit_message(**kwargs):
    global URL
    payload = {}
    for key, value in kwargs.items():
        payload[key] = value
    print(payload)
    req = requests.post(URL + 'editMessageText', json=payload)
    

def answer_query_callback(id, string):
    global URL
    print('answering query callback')
    send_message(chat_id=id, text=string)
    

def handle_query_callback(update):
    print update
    msg = update['callback_query']
    data = msg["data"]
    user = msg["from"]["username"] if \
            msg['from'].get('username') else msg['from']['first_name']
    chat_id = msg["message"]["chat"]["id"]
    payload = {
            'type': 'query_callback',
            'id': msg['id'],
            "chat_id": chat_id,
            'user_id': msg['from']['id'],
            'user': user,
            'callback': data
            }
    pushDataToDispatcher(payload)

def handle_message(msg):

    if msg.get('text', None) == None:
        pass

    else:
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]
        user = msg["from"]["username"] if \
        msg["from"].get("username") else msg["from"]["first_name"]
       
        data = {
                'type': 'message',
                'chat_id': msg['chat']['id'],
                'user_id': msg['from']['id'],
                'user': user,
                'text': msg['text']
                }

        if msg['text'] == '/help@charge_game_bot' or msg['text'] == '/help':
            text = """
=== Charge Bot ===
=== lieuzhenghong.github.io ===

Charge is a double-blind battle game for two players. The objective is to hit the other player with an attack and win the game.

Each turn, secretly choose a move. Some moves cost mana, which can only be obtained with the Charge move.

Charge: Gain 1 mana.

波動拳, Hadouken (1): A basic attack. Blockable with High Block or Low Block.
Lightning (3): A mid-level attack. Trumps Hadouken, and is blockable only with High Block.
Earthquake (3): A mid-level attack. Trumps Hadouken, and is blockable only with Low Block.
天地, Heaven and Earth (5): The strongest attack. Trumps all other attacks, and can't be blocked.

High Block: Blocks Hadouken or Lightning.
Low Block: Blocks Hadouken or Earthquake.
Reflect (2): Reflect any attack back at your opponent (even Heaven and Earth).            """
            msg = (send_message(chat_id=chat_id, text=text))
        else:
            pushDataToDispatcher(data)

def handle_updates(res):
    if res['ok'] and len(res['result']) > 0: # In the case of no message
        res = res['result'] # Strip the boolean ok
        for update in res:
            msg = update.get('callback_query')
            if msg == None:
                msg = update.get('message')
                handle_message(msg)
            else:
                handle_query_callback(update)
            change_offset(update['update_id'])
            # print(msg)

def get_updates(r, *args, **kwargs):
    global URL
    res = r.json()
    handle_updates(res)
    string = URL + 'getUpdates?offset={0}&timeout={1}'.format(offset,100)
    # print(string)
    req = requests.get(string, hooks=dict(response=get_updates))



