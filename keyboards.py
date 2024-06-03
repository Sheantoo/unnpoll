from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup,InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1'),
                                      KeyboardButton(text='2'),
                                      KeyboardButton(text='3')]],
                            resize_keyboard=True, input_field_placeholder='Выберите цифру')

choose_poll = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data = 'one')],
    [InlineKeyboardButton(text='2', callback_data = 'two')],
    [InlineKeyboardButton(text='3', callback_data = 'three')]])
