# -*- coding: utf-8 -*-
import requests
import json

TOKEN = '230906963:AAGD_tKVKN9K58zEBPUVCS5WZvSMxdBqNV8'
URL = ('https://api.telegram.org/bot{0}/').format(TOKEN)
callback = None

offset = 0

def init():
    read_offset()
    get_updates()

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
        dictionary = json.load(f)
        offset = dictionary.get('offset')
    return(offset)

def change_offset(new_offset):
    global offset
    new_offset = str(int(new_offset) + 1)
    offset = new_offset
    with open('config.json', 'w') as f:
        json.dump({"offset": offset}, f)
    return(read_offset())

def send_message(**kwargs):
    global URL
    payload = {}
    for key, value in kwargs.items():
        payload[key] = value
    req = requests.post(URL + 'sendMessage', json=payload)
    return(req.json())


def answer_query_callback(chat_id, string):
    global URL
    print('answering query callback')
    send_message(chat_id=chat_id, text=string)
    

def handle_query_callback(update):
    print(update)
    msg = update['callback_query']
    data = msg["data"]
    user = msg["from"]["username"] if msg['from'].get('username') else msg['from']['first_name']
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
    if msg is None: #Handle requests with no message: inline queries for example
        pass
    elif msg.get('text', None) is None:
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
            with open ('README.txt', 'r') as file:
                text = file.read()
            msg = (send_message(chat_id=chat_id, text=text, parse_mode="Markdown"))
        else: # if message is not something that is in network, pass it to the dispatcher
            pushDataToDispatcher(data)

def handle_updates(res):
    res = res.json()
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
            print(read_offset())
            # print(msg)

def get_updates():
    while True:
        string = URL + 'getUpdates?offset={0}&timeout={1}'.format(read_offset(), 3600)
        req = requests.get(string)
        handle_updates(req)
