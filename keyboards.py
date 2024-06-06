from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                            InlineKeyboardMarkup,InlineKeyboardButton)
import prs 

import json

def create_dynamic_keyboard(items, page=0, items_per_page=3):
    total_pages = (len(items) + items_per_page - 1) // items_per_page
    start = page * items_per_page
    end = start + items_per_page
    buttons = [[InlineKeyboardButton(text=item, callback_data=f'item_{start + i}')] for i, item in enumerate(items[start:end])]

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f'prev_{page-1}'))
    if page < total_pages - 1:
        navigation_buttons.append(InlineKeyboardButton(text="Вперед", callback_data=f'next_{page+1}'))

    if navigation_buttons:
        buttons.append(navigation_buttons)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def create_multi_select_keyboard(data, selected_items):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in data:
        if item[0] in selected_items:
            button_text = f'✅ {item[1]} ({item[2]})'
        else:
            button_text = f'{item[1]} ({item[2]})'
        button = InlineKeyboardButton(text=button_text, callback_data=f'select_{item[0]}')
        keyboard.add(button)
    return keyboard

def create_confirm_button():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='Подтвердить выбор', callback_data='confirm_selection')
    keyboard.add(button)
    return keyboard

async def generate_question_keyboard(question_data):
    parsed_data = json.loads(question_data)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for question in parsed_data['questions']:
        button_text = question['questionText']
        callback_data = f'answer_{question["questionText"]}'
        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return keyboard

