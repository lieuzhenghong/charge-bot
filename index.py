"""The main file of the Telegram Charge bot."""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lobby
import network
import game

def init():
    """Initialises the app and sets up all callbacks"""
    network.setPushDataTo(dispatcher)
    lobby.sendMessagesTo(announcer)
    lobby.startGameTo(game_handler)
    game.sendMessagesTo(announcer)
    game.answerCallBackTo(query_callback_handler)
    game.resetGameTo(reset_game_handler)
    network.init()

def game_handler(data):
    """
    This game_handler function is called by lobby.py when lobby is full
    and calls the start_game function in game.py
    """
    game.start_game(data)

def reset_game_handler(chat_id):
    """
    This reset_game_handler is called by game.py when a game ends and
    calls the remake_game function in lobby.py
    """
    lobby.remake_game(chat_id)

def query_callback_handler(chat_id, text):
    """
    This handler is called by game.py when a player clicks on the button
    of an inline keyboard, and calls the answer_query_callback function in
    network.py
    """
    print('query_callback_handler called')
    network.answer_query_callback(chat_id, text)

def dispatcher(data):
    """
    This dispatcher receives Updates from network.py. Depending on the type of
    message it is, it will route to lobby.py or game.py.

    Note that this dispatcher is called when network.py cannot handle it (i.e. it's
    either an inline keyboard press or /join, /remake.)

    Inline keyboard press: call game.game_route, message call lobby.lobby_route
    """
    if data['type'] == 'message':
        lobby.lobby_route(data)
    elif data['type'] == 'query_callback':
        # The following line gets the game lobby corresponding to the chat
        game_lobby = lobby.find_game(data['chat_id'])
        game.game_route(data, game_lobby)

def announcer(**kwargs):
    """
    This announcer function receives messages from lobby.py and game.py. It then
    routes it to network.send_message due to the fact that lobby and game have no access
    to network.py.
    """
    args = {}
    for key, value in kwargs.items():
        args[key] = value
    reply_markup = args.get('reply_markup', None)
    edit = args.get('edit', None)
    if reply_markup is None:
        msg = network.send_message(chat_id=args['chat_id'], text=args['text'])
        return msg
    else:
        if edit is None:
            msg = network.send_message(chat_id=args['chat_id'], text=args['text'],
                                       reply_markup=args['reply_markup'])
            return msg
        else:
            return msg
init()

