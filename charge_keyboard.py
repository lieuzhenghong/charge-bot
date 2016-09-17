#!/usr/bin/env python
# -*- coding: utf-8 -*- 

high_block_button = {"text": "High Block", "callback_data": 'high_block'}
lightning_button = {"text": "Lightning (3)", "callback_data": 'lightning'}
reflect_button = {"text": "Reflect (2)", "callback_data": 'reflect'} 
hadouken_button ={"text": "波動拳 (1)", "callback_data": 'hadouken'}
low_block_button =  {"text": "Low Block", "callback_data": 'low block'}
earthquake_button = {"text": "Earthquake (3)", "callback_data": 'earthquake'}
charge_button = {"text": "Charge", "callback_data": 'charge'} 
tian_di_button = {"text": "天地 (5)", "callback_data": 'tiandi'}


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
