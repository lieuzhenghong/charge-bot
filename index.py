#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import Flask
import requests
import json

import lobby
import network
import game
from charge_keyboard import *


def init():
    network.setPushDataTo(dispatcher)
    lobby.sendMessagesTo(announcer)
    lobby.startGameTo(game_handler)
    game.sendMessagesTo(announcer)
    game.answerCallBackTo(query_callback_handler)
    game.resetGameTo(reset_game_handler)
    network.init()

def game_handler(data):
    game.start_game(data)

def reset_game_handler(chat_id):
    lobby.remake_game(chat_id)
    
def query_callback_handler(id, text):
    print('query_callback_handler called')
    network.answer_query_callback(id, text)

def dispatcher(data):
    if data['type'] == 'message':
        lobby.lobby_route(data)
    elif data['type'] == 'query_callback':
        # The following line gets the game lobby corresponding to the chat
        game_lobby = lobby.find_game(data['chat_id'])
        game.game_route(data, game_lobby)
    
def announcer(**kwargs):
    args = {}
    for key, value in kwargs.items():
        args[key] = value
    reply_markup = args.get('reply_markup', None)
    edit = args.get('edit', None)
    if reply_markup == None:
        msg = network.send_message(chat_id=args['chat_id'], text=args['text'])
        return(msg)
    else:
        if edit == None:
            msg = network.send_message(chat_id=args['chat_id'],
                    text=args['text'],reply_markup=args['reply_markup'])
            return(msg)
        else:
            return(msg) 

  
init()

