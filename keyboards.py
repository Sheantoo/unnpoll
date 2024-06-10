# keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создание динамической клавиатуры с пагинацией
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

# Отправка вопроса типа checkbox
async def send_checkbox_question(chat_id, question, bot):
    buttons = []
    for option in question["options"]:
        button = [InlineKeyboardButton(text=option["optionText"], callback_data=option["optionText"])]
        buttons.append(button)
    buttons.append([InlineKeyboardButton(text="Подтвердить выбранный ответ", callback_data="confirm_checkbox")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(chat_id, question["question_text"], reply_markup=keyboard)

# Отправка вопроса типа radio
async def send_radio_question(chat_id, question, bot):
    buttons = []
    for option in question["options"]:
        button = [InlineKeyboardButton(text=option["optionText"], callback_data=option["optionText"])]
        buttons.append(button)
    buttons.append([InlineKeyboardButton(text="Подтвердить", callback_data="confirm_radio")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(chat_id, question["question_text"], reply_markup=keyboard)


# Отправка вопроса типа text
async def send_text_question(chat_id, question, bot):
    await bot.send_message(chat_id, question["question_text"])


async def send_checkbox_question_false(chat_id, question, bot):
    buttons = []
    for option in question["options"]:
        button = [InlineKeyboardButton(text=option["optionText"], callback_data=option["optionText"])]
        buttons.append(button)
    buttons.append([InlineKeyboardButton(text="Подтвердить выбранный ответ", callback_data="confirm_checkbox")])
    buttons.append([InlineKeyboardButton(text="Пропустить вопрос\nВопрос необязательный.", callback_data="question_false")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(chat_id, question["question_text"], reply_markup=keyboard)

async def send_radio_question_false(chat_id, question, bot):
    buttons = []
    for option in question["options"]:
        button = [InlineKeyboardButton(text=option["optionText"], callback_data=option["optionText"])]
        buttons.append(button)
    buttons.append([InlineKeyboardButton(text="Подтвердить", callback_data="confirm_radio")])
    buttons.append([InlineKeyboardButton(text="Пропустить вопрос\nВопрос необязательный.", callback_data="question_false")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(chat_id, question["question_text"], reply_markup=keyboard)


# Отправка вопроса типа text
async def send_text_question_false(chat_id, question, bot):
    await bot.send_message(chat_id, question["question_text"]+'. Необязательный вопрос наберите "/skip" для перехода к следующему вопросу')
    



