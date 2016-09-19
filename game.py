# -*- coding: utf-8 -*-
from charge_keyboard import *
from textwrap import dedent

game_config = {
    'msg_callback':  None,
    'ans_callback': None,
    'reset_callback': None
}

game_states = []

def reset_game(game):
    chat_id = game['chat_id']
    # Need to call remake_game in the lobby.
    for game in game_states:
        if game['chat_id'] == chat_id:
            game_states.remove(game)
    game_config['reset_callback'](chat_id)

def resetGameTo(function):
    global game_config
    game_config['reset_callback'] = function

def sendMessagesTo(function):
    global game_config
    game_config['msg_callback'] = function

def send_message(**kwargs):
    global game_config
    game_config['msg_callback'](**kwargs)

def answerCallBackTo(function):
    global game_config
    game_config['ans_callback'] = function

def ans_callback(chat_id, text):
    print('ans_callback called')
    global game_config
    game_config['ans_callback'](chat_id, text)

def handle_move(data):
    '''
    data
    {
        'type': 'query_callback',
        "chat_id": chat_id,
        'user_id': msg['from']['id'],
        'user': user,
        'callback': data
    }
    game
    {
        'chat_id': data['chat_id
        '],
        'players':
        {
            'player_1': {
                'id': data['current_players'][0],
                'name': data['player_names'][0],
                'mana': 0,
                'current_move' : None
                },
            'player_2': {
                'id': data['current_players'][1],
                'name': data['player_names'][1],
                'mana': 0,
                'current_move' : None
                },
            },
        'winner': None
        }
    '''
    # Here, the player has made his move.
    # We already verified that the player is legit.
    # So we don't have to check if the player is in either player_1 or player_2
    # as we already checked previously.
    global game_states
    global scratch_message

    def find_game_state(chat_id):
        for game in game_states:
            if game["chat_id"] == chat_id:
                return game

    game = find_game_state(data['chat_id'])

    p1 = game['players']['player_1']
    p2 = game['players']['player_2']

    if p1['id'] == data['user_id']:
        player = p1
    else:
        player = p2

    if player['current_move'] is not None:
        data['callback'] = None
        text = "{0}, you have already moved.".format(player['name'])
        send_message(chat_id=data['chat_id'], text=text)

    else:
        player['current_move'] = data['callback']
        idx = MOVES.index(player['current_move'])
        if player['mana'] - MOVES_MANA[idx] < 0:
            player['current_move'] = None
            text = "{0}, you don't have enough mana to make that move.".format(player['name'])
            #ans_callback(data['id'], text)
            send_message(chat_id=data['chat_id'], text=text)
        else:
            p1_move = p1['current_move']
            p2_move = p2['current_move']

            player['mana'] = player['mana'] - MOVES_MANA[idx]

            print(player)

            if p1_move != None and p2_move != None:
                # Both players have made their move
                result = clash(p1_move, p2_move)
                print(result)
                if (p1_move == tian_di_button['callback_data'] and
                        p2_move == tian_di_button['callback_data']):
                    text = dedent("""The earth is torn asunder as both players call
                           upon the mighty power of the heavens!!!""")
                elif (p1_move == tian_di_button['callback_data'] and
                      p2_move == reflect_button['callback_data']):
                    pass
                elif p1_move == tian_di_button['callback_data']:
                    text = dedent("""
                        天地玄黃 , 宇宙洪荒!!! 
                        {0} moved heaven and earth to destroy {2}!
                        {2} moved {3}.
                        """.format(p1['name'], p1_move, p2['name'], p2_move))
                elif p2_move == tian_di_button['callback_data']:
                    text = dedent("""
                        天地玄黃 , 宇宙洪荒!!! 
                        {2} moved heaven and earth to destroy {0}! 
                        {0} moved {1}.
                        """.format(p1['name'], p1_move, p2['name'], p2_move))
                else:
                    text = dedent(
                        """
                        {0} used {1}!
                        {2} used {3}!
                        {0}: {4} mana.
                        {2}: {5} mana.
                        """
                        ).format(p1['name'], p1_move, p2['name'],
                                 p2_move, p1['mana'], p2['mana'])
                # ans_callback(data['id'], text)
                # Now I have to reset both moves
                game['players']['player_1']['current_move'] = None
                game['players']['player_2']['current_move'] = None
                send_message(chat_id=data['chat_id'], text=text, parse_mode="Markdown")

                if result == 1:
                    game['winner'] = p1['name']
                    text2 = 'Winner: {0}'.format(p1['name'])
                    # ans_callback(data['id'], text)
                    send_message(chat_id=data['chat_id'], text=text2)
                    reset_game(game)
                elif result == -1:
                    game['winner'] = p2['name']
                    text2 = 'Winner: {0}'.format(p2['name'])
                    # ans_callback(data['id'], text)
                    send_message(chat_id=data['chat_id'], text=text2)
                    reset_game(game)
                else:
                    text2 = 'What action would you like to perform?'
                    send_message(chat_id=data['chat_id'], text=text2,
                                 reply_markup=charge_keyboard)
            else:
                text = '{0} moved. Waiting for other player'.format(data['user'])
                send_message(chat_id=data['chat_id'], text=text)


def game_route(data, lobby):
    """
    This function is called by dispatcher in index.py when it receives a
    query callback Update. (Because the only possible query callback is
    from pressing the inline Charge keyboard).

    Makes sure that the person clicking the inline keyboard is an actual player.
    If he is, then call handle_move.
    """
    print('game route called')
    # Here i need to check that the user clicking is a player
    user = data['user_id']
    if lobby is None:
        return False
    # Check that user exists in current_games which is in lobby.py
    if user in lobby['current_players']:
        handle_move(data)
    else:
        pass

def start_game(data):
    """
    Called by lobby.py when game is full through the dispatcher in index.py.
    Starts a game, then sends a Message with the inline Charge keyboard.
    """
    # data is actually a game object
    global game_states
    print(charge_keyboard)
    game_states.append({
        'chat_id': data['chat_id'],
        'players':
        {
            'player_1': {
                'id': data['current_players'][0],
                'name': data['player_names'][0],
                'mana': 1,
                'current_move' : None
                },
            'player_2': {
                'id': data['current_players'][1],
                'name': data['player_names'][1],
                'mana': 1,
                'current_move' : None
                },
            },
        'winner': None
        }
                      )
    text = dedent(
        """
        Game started. What action would you like to perform?
        {0}: {2} mana. {1}: {3} mana.
        """
        ).format(data['player_names'][0], data['player_names'][1], 1, 1)

    send_message(chat_id=data['chat_id'], text=text, reply_markup=charge_keyboard)

#
# HERE ON OUT ARE CONSTANTS
#

MOVES = [
    reflect_button['callback_data'],
    tian_di_button['callback_data'],
    lightning_button['callback_data'],
    earthquake_button['callback_data'],
    high_block_button['callback_data'],
    low_block_button['callback_data'],
    hadouken_button['callback_data'],
    charge_button['callback_data']
    ]

MOVES_MANA = [
    2, 5, 3, 3, 0, 0, 1, -1
    ]

# The way to read the move matchups is you take the moves array, get the index
# of the first move, then the index of the second move. Example: lightning [2]
# and low block [5]. Then read [25] or [52], zero-indexed. [25] gives 1, [52]
# gives -1. 1 means a win for the move on the left, -1 a win for that on the
# right. The last two columns are filler to convert from base 8 to base 10

MOVE_MATCHUPS = [
    0, 1, 1, 1, 0, 0, 1, 0, 0, 0,
    -1, 0, 1, 1, 1, 1, 1, 1, 0, 0,
    -1, -1, 0, 0, 0, 1, 1, 1, 0, 0,
    -1, -1, 0, 0, 1, 0, 1, 1, 0, 0,
    0, -1, 0, -1, 0, 0, 0, 0, 0, 0,
    0, -1, -1, 0, 0, 0, 0, 0, 0, 0,
    -1, -1, -1, -1, 0, 0, 0, 1, 0, 0,
    0, -1, -1, -1, 0, 0, -1, 0, 0, 0
    ]

def clash(move1, move2):
    index = MOVES.index(move1) * 10 + MOVES.index(move2)
    return MOVE_MATCHUPS[index]


