# -*- coding: utf-8 -*-
high_block_button = {"text": "\u21AA High Block", "callback_data": '\u21AA High Block'}
lightning_button = {"text": "🎇 Lightning (3)", "callback_data": '🎇 Lightning'}
reflect_button = {"text": "↪️ Reflect (2)", "callback_data": '↪️ Reflect'}
hadouken_button ={"text": "✴️ 波動拳 (1)", "callback_data": '✴️ Hadouken'}
low_block_button =  {"text": "⏬ Low Block", "callback_data": '⏬ Low Block'}
earthquake_button = {"text": "🌋 Earthquake (3)", "callback_data": '🌋 Earthquake'}
charge_button = {"text": "✳️ Charge", "callback_data": '✳️ Charge'} 
tian_di_button = {"text": "☯ 天地 (5)", "callback_data": '☯ tiandi'}


charge_keyboard = {
        "inline_keyboard":
            [

                [tian_di_button],
                [high_block_button, lightning_button],
                [reflect_button, hadouken_button],
                [low_block_button, earthquake_button],
                [charge_button]
            ]
            }

'''

charge_keyboard = {
        "keyboard":
            [
                [high_block_button, tian_di_button, lightning_button],
                [reflect_button, hadouken_button],
                [low_block_button, earthquake_button],
                [charge_button]
            ]
        }

'''
