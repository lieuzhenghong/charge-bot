# -*- coding: utf-8 -*-
current_games = []
lobby_callback = None
lobby_callback_game = None

def sendMessagesTo(fn):
    global lobby_callback
    lobby_callback = fn

def send_message(**kwargs):
    global lobby_callback
    lobby_callback(**kwargs)

def startGameTo(fn):
    global lobby_callback_game
    lobby_callback_game = fn

def start_game(data):
    global lobby_callback_game
    lobby_callback_game(data)

def lobby_route(data):
    """
    lobby_route handles the commands that come in, and calls functions depending
    on the action.
    """
    print(data['text'])
    if data['text'] == "/start" or data['text'] == "/start@charge_game_bot":
        join_game(data['chat_id'], data['user_id'], data['user'])
    elif data['text'] == "/join" or data['text'] == "/join@charge_game_bot":
        join_game(data["chat_id"], data['user_id'], data['user'])
    elif data['text'] == "/remake" or data['text'] == "/remake@charge_game_bot":
        remake_game(data["chat_id"])
    else:
        text = 'Unknown command.'
        send_message(chat_id=data['chat_id'], text=text)

def remake_game(chat_id):
    global current_games
    if find_game(chat_id) != None:
        current_games.remove(find_game(chat_id))
        send_message(chat_id=chat_id, text="Game remade.")
        add_game(chat_id)
    else:
        send_message(chat_id=chat_id, text="Game remade.")

def add_game(chat_id):
    global current_games
    text = ''
    if find_game(chat_id) != None:
        text = ('A duel already exists. /join to join a duel.')
    else:
        current_games.append({
            'chat_id': chat_id,
            'current_players': [],
            'player_names': []
            })
        text = "A duel has been started. /join to join (2 max)."
    send_message(chat_id=chat_id, text=text)

def find_game(chat_id):
    global current_games
    for game in current_games:
        if game["chat_id"] == chat_id:
            return game
    return None

def join_game(chat_id, player_id, player):
    global current_games
    game = find_game(chat_id)
    if game is None:
        add_game(chat_id)
        join_game(chat_id, player_id, player)
    elif len(game['current_players']) >= 2:
        players = find_game(chat_id)['player_names']
        text = 'The room is full. Players: {0}, {1}'.format(players[0],players[1])
        send_message(chat_id=chat_id, text=text)
    elif player_id in game['current_players']:
        text = 'You have already joined. Current players:{0}'.format(' '.join(game['player_names']))
        send_message(chat_id=chat_id, text=text)
    else:
        game['current_players'].append(player_id)
        game['player_names'].append(player)
        
        text = "{0} joined the game. Current players: {1}".format(game['player_names'][-1], 
                                                                  ' '.join(game['player_names']))
        send_message(chat_id=chat_id, text=text)
        if len(game['current_players']) >=2:
            send_message(chat_id=chat_id, text='Game is starting.')
            start_game(game)

