# handlers.py

import re
from aiogram import F, types, Router, Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import database as db
import keyboards as kb
import prs

router = Router()
bot = Bot(token="6458503910:AAGORHNT4np02C_8kp8EaYyTBrdiLxmUnVs")

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

js_arr = [
    '{"doc_id":"2299a939-d9a3-6a33-815f-4f9dfc8a8fc0","document_name":"Предпочтения слушателей подкастов","doc_desc":"","questions":[{"questionText":"Укажите ваш пол","qustionType":"radio","options":[{"optionText":"Мужской"},{"optionText":"Женский"}],"open":false,"required":true},{"questionText":"Укажите ваш возраст","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":true},{"questionText":"Укажите уровень вашего образования","qustionType":"radio","options":[{"optionText":"неполное высшее"},{"optionText":"высшее"},{"optionText":"среднее"}],"open":false,"required":true},{"questionText":"Слушаете ли вы подкасты о культуре?","qustionType":"radio","options":[{"optionText":"Да"},{"optionText":"Нет"}],"open":false,"required":true},{"questionText":"Хотели бы вы узнать больше о событиях в сфере культуры вашего города? ","qustionType":"radio","options":[{"optionText":"Да"},{"optionText":"Нет"}],"open":false,"required":true},{"questionText":"В каком формате Вам было бы комфортнее слушать подкаст?","qustionType":"radio","options":[{"optionText":"Каждое направление - отдельный"},{"optionText":"Каждый выпуск - новое направление"}],"open":false,"required":true},{"questionText":"Оцените ваш интерес к теме культуры от 1 до 5:","qustionType":"radio","options":[{"optionText":"1"},{"optionText":"2"},{"optionText":"3"},{"optionText":"4"},{"optionText":"5"}],"open":true,"required":true}]}',
    '{"doc_id":"ae7e6026-c01b-f136-f5e1-c4244405e46a","document_name":"Жизненные планы молодежи","doc_desc":"","questions":[{"questionText":"КАК ИЗМЕНИЛАСЬ ВАША ЖИЗНЬ ЗА ПОСЛЕДНИЕ 1,5-2 ГОДА?","qustionType":"radio","options":[{"optionText":"Стала заметно лучше"},{"optionText":"Немного улучшилась"},{"optionText":"Практически не изменилась"},{"optionText":"Немного ухудшилась"},{"optionText":"Стала гораздо хуже"}],"open":false,"required":true},{"questionText":"С КАКИМИ ЧУВСТВАМИ ВЫ ДУМАЕТЕ О СВОЕМ БУДУЩЕМ?","qustionType":"radio","options":[{"optionText":"С надеждой, оптимизмом"},{"optionText":"Спокойно, без иллюзий"},{"optionText":"С беспокойством, тревогой"},{"optionText":"Со страхом и отчаянием"}],"open":false,"required":true},{"questionText":"КТО И ЧТО ПОМОГАЕТ ВАМ ПРИ ВЫБОРЕ МЕСТА БУДУЩЕЙ РАБОТЫ/УЧЕБЫ И МЕСТА ЖИТЕЛЬСТВА? ","qustionType":"checkbox","options":[{"optionText":"Советы семьи"},{"optionText":"Советы учителей"},{"optionText":"Интернет"},{"optionText":"Советы друзей"},{"optionText":"Публикации в газета"}],"open":false,"required":true},{"questionText":"КАК ВЫ ДУМАЕТЕ, ПОЧЕМУ МОЛОДЫЕ ЛЮДИ УЕЗЖАЮТ ИЗ СВОЕГО НАСЕЛЕННОГО ПУНКТА? ","qustionType":"checkbox","options":[{"optionText":"Хотят найти интересную работу"},{"optionText":"Хотят получать хорошую зарплату"},{"optionText":"Желают сделать карьеру"},{"optionText":"Хотят поменять место жительства"},{"optionText":"Стремятся получить "}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: За границей больше возможностей для карьерного роста","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: За границей выше уровень безопасности","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: За границей лучше развиты инфраструктура и услуги, которые улучшают комфорт жизни","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: Качество жизни в зарубежных странах выше, чем в России","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: Меня привлекает идея познания новых культур и обычаев, которые представлены в зарубежных странах","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: Я бы хотел(а) путешествовать по различным странам","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: Мне интересно изучать иностранные языки","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"ЧТО, ПО-ВАШЕМУ, ВАЖНО, ЧТОБЫ СЧИТАТЬ СЕБЯ УСПЕШНЫМ В ЖИЗНИ?","qustionType":"checkbox","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":true,"required":false}]}',
    '{"doc_id":"60d367a0-ec26-f6cc-5059-0db11879d149","document_name":"Влияние интернет-рекламы на поведение студенческой молодежи","doc_desc":"","questions":[{"questionText":"Сколько времени в сутки Вы проводите в интернете?","qustionType":"radio","options":[{"optionText":"Менее 1 часа"},{"optionText":"1-2 часа"},{"optionText":"3-4 часа"},{"optionText":"Более 4 часов"}],"open":true,"required":false},{"questionText":"Какое устройство Вы чаще используете для выхода в интернет?","qustionType":"radio","options":[{"optionText":"Смартфон"},{"optionText":"Ноутбук"},{"optionText":"Планшет"},{"optionText":"Компьютер"}],"open":false,"required":false},{"questionText":"Какие из сервисов Вы чаще всего используете?","qustionType":"checkbox","options":[{"optionText":"Видеохостинги (YouTube)"},{"optionText":"Социальные сети"},{"optionText":"Веб-браузер"},{"optionText":"Онлайн-магазины"}],"open":false,"required":false},{"questionText":"Как Вы относитесь к рекламе в целом?","qustionType":"radio","options":[{"optionText":"Положительно"},{"optionText":"Нейтрально"},{"optionText":"Отрицательно"}],"open":false,"required":false},{"questionText":"Как Вы считаете, какие из следующих факторов наиболее сильно раздражают в рекламе?","qustionType":"radio","options":[{"optionText":"Навязчивость рекламы (всплывающие окна, автоматическое воспроизведение рекламы)"},{"optionText":"Нежелательная персонализация (реклама, подобранная под Вас путем сбора данных о Вашей активности)"},{"optionText":"Неправдивая реклама (реклама с нерабочими промокодами, обманом относительно цены, функций товара и тд.)"}],"open":false,"required":false},{"questionText":"Как часто Вы обращаете внимание на рекламу в интернете?","qustionType":"radio","options":[{"optionText":"Почти всегда"},{"optionText":"Часто"},{"optionText":"Иногда"},{"optionText":"Редко"},{"optionText":"Никогда"}],"open":false,"required":false},{"questionText":"Сколько раз за последний месяц Вы совершали покупки товаров, увиденных в интернет-рекламе?","qustionType":"radio","options":[{"optionText":"Ни разу"},{"optionText":"1-2 раза"},{"optionText":"3-5 раз"}],"open":false,"required":false},{"questionText":"Какие из следующих факторов наиболее важны для Вас при покупке товара?","qustionType":"checkbox","options":[{"optionText":"Мода"},{"optionText":"Страна-производитель"},{"optionText":"Цена"},{"optionText":"Качество"}],"open":false,"required":false},{"questionText":"Какие товары Вы чаще предпочитаете покупать вживую?","qustionType":"checkbox","options":[{"optionText":"Одежда и обувь"},{"optionText":"Электроника и техника"},{"optionText":"Продукты питания"},{"optionText":"Книги и другой досуг (фильмы, музыка)"}],"open":false,"required":false},{"questionText":"Как реклама чаще влияет на формуВашего выбора покупки онлайн или вживую?","qustionType":"radio","options":[{"optionText":"Побуждает к покупке вживую"},{"optionText":"Побуждает к онлайн покупке"},{"optionText":"Никак не влияет на выбор"},{"optionText":"Затрудняюсь ответить"}],"open":false,"required":false},{"questionText":"Согласны ли Вы с утверждением, что интернет-реклама влияет на Ваш выбор товаров?","qustionType":"radio","options":[{"optionText":"Полностью согласен"},{"optionText":"Согласен частично"},{"optionText":"Частично не согласен"},{"optionText":"Полностью не согласен"}],"open":false,"required":false},{"questionText":"Укажите ваш пол","qustionType":"radio","options":[{"optionText":"Мужской"},{"optionText":"Женский"}],"open":false,"required":false},{"questionText":"Укажите Ваш уровень образования","qustionType":"radio","options":[{"optionText":"Бакалавриат"},{"optionText":"Специалитет"},{"optionText":"Магистратура"},{"optionText":"Аспирантура"}],"open":false,"required":false}]}',
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b170c","document_name":"фффф","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}'
]

arr = prs.parse_json_document(js_arr)
items = [arr[i]['document_name'] for i in range(len(arr))]
questions = [arr[i]['questions'] for i in range(len(arr))]

class QuizStates(StatesGroup):
    QuestionState = State()

class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

class Edit(StatesGroup):
    name = State()
    age = State()
    number = State()

def unique_values(lst):
    return list(set(lst))


async def start_quiz(chat_id, bot, state: FSMContext, questions):
    if not questions or not isinstance(questions, list):
        await bot.send_message(chat_id, "Произошла ошибка при инициализации вопросов.")
        return

    await state.update_data(questions=questions, question_index=0)
    await ask_question(chat_id, bot, state)

async def ask_question(chat_id, bot, state: FSMContext):
    data = await state.get_data()
    questions = data.get('questions')
    question_index = data.get('question_index', 0)

    if questions is None or not isinstance(questions, list):
        await bot.send_message(chat_id, "Произошла ошибка при обработке вопросов.")
        return

    if question_index < len(questions):
        current_question = questions[question_index]
        if current_question['required']:
            if isinstance(current_question, dict):
                if current_question["question_type"] == "checkbox":
                    await kb.send_checkbox_question(chat_id, current_question, bot)
                elif current_question["question_type"] == "radio":
                    await kb.send_radio_question(chat_id, current_question, bot)
                elif current_question["question_type"] == "text":
                    await kb.send_text_question(chat_id, current_question, bot)
            else:
                await bot.send_message(chat_id, "Произошла ошибка при обработке вопроса.")
        else:
            if isinstance(current_question, dict):
                if current_question["question_type"] == "checkbox":
                    await kb.send_checkbox_question_false(chat_id, current_question, bot)
                elif current_question["question_type"] == "radio":
                    await kb.send_radio_question_false(chat_id, current_question, bot)
                elif current_question["question_type"] == "text":
                    await kb.send_text_question_false(chat_id, current_question, bot)
            else:
                await bot.send_message(chat_id, "Произошла ошибка при обработке вопроса.")
        await state.set_state(QuizStates.QuestionState)
    else:
        await bot.send_message(chat_id, "Спасибо, что прошли опрос!")
        await state.clear()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = await db.search_user_id(message.from_user.id)
    if user_id == message.from_user.id:
        await message.answer('Выберите опрос 📑', reply_markup=kb.create_dynamic_keyboard(items))
        
    else:
        await message.answer('Привет! Вы не зарегистрированы . Для регистрации нажмите кнопку /register')

@router.callback_query(lambda c: c.data.startswith('next_') or c.data.startswith('prev_'))
async def handle_pagination(callback_query: CallbackQuery):
    page = int(callback_query.data.split('_')[1])
    keyboard = kb.create_dynamic_keyboard(items, page=page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer('')

@router.callback_query(lambda c: c.data.startswith('item_'))
async def process_item_callback(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = callback_query.message.chat.id
    item_index = int(callback_query.data.split('_')[1])
    await state.update_data(answers=[], question_index=0)
    await start_quiz(chat_id, bot, state, questions[item_index])
    await callback_query.answer('Опрос выбран')

@router.message(QuizStates.QuestionState)
async def process_answer(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    questions = data.get("questions")
    question_index = data.get("question_index", 0)
    answers = data.get("answers", [])

    if questions is None or not isinstance(questions, list):
        await bot.send_message(chat_id, "Произошла ошибка при обработке вопросов.")
        return

    current_question = questions[question_index]
    answers.append({"question": current_question["question_text"], "answer": message.text})
    await state.update_data(answers=answers)

    if question_index + 1 < len(questions):
        await state.update_data(question_index=question_index + 1)
        await ask_question(chat_id, bot, state)
    else:
        await bot.send_message(chat_id, "Спасибо, что прошли опрос!")
        await state.clear()

@router.callback_query(QuizStates.QuestionState)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = callback_query.message.chat.id
    data = await state.get_data()
    questions = data.get("questions")
    question_index = data.get("question_index", 0)
    answers = data.get("answers", [])
    confirmed = data.get("confirmed", False)
    selected_options = data.get("selected_options", [])

    if questions is None or not isinstance(questions, list):
        await bot.send_message(chat_id, "Произошла ошибка при обработке вопросов.")
        return

    current_question = questions[question_index]

    if not isinstance(current_question, dict):
        await bot.send_message(chat_id, "Произошла ошибка при обработке вопроса.")
        return

    if current_question["question_type"] == "radio":
        for opt in current_question["options"]:
            option_data = f'{opt["optionText"]}'
            # print(selected_options)
            if option_data == callback_query.data:
                selected_options = []
                selected_options.append(opt["optionText"])
                await callback_query.answer(f'Вы выбрали: {opt['optionText']}')
        await state.update_data(selected_options=selected_options)
    elif current_question["question_type"] == "checkbox":
        for opt in current_question["options"]:
            option_data = f'{opt["optionText"]}'
            # print(option_data)
            if option_data == callback_query.data:
                selected_options.append(opt["optionText"])
                #  selected_options = unique_values(selected_options)
                await callback_query.answer(f'Вы выбрали: {opt['optionText']}')
        await state.update_data(selected_options=selected_options)

    
    if current_question["question_type"] in ["checkbox", "radio"]:
        if not selected_options:
            await bot.send_message(chat_id, 'Нужно выбрать хотя бы один вариант ответа.')
            return
        await state.update_data(confirmed=True)
    else:
        await bot.send_message(chat_id, 'Нужно выбрать вариант ответа.')
        return
    
    if callback_query.data == "confirm_checkbox" or callback_query.data == "confirm_radio":
        if not confirmed:
            if current_question["question_type"] == "checkbox":
                await kb.send_checkbox_question(chat_id, current_question, bot)
            elif current_question["question_type"] == "radio":
                await kb.send_radio_question(chat_id, current_question, bot)
        else:
            #  print(answers)
            answers.append({"question": current_question["question_text"], "answer": selected_options})
            print(answers)
            #  await state.update_data(answers=answers)
            await state.update_data(confirmed=False)

            if question_index + 1 < len(questions):
                await state.update_data(question_index=question_index + 1)
                await send_next_question(chat_id, bot, state)
            else:
                await bot.send_message(chat_id, "Спасибо за участие в опросе!")
                await state.clear()
        
    if callback_query.data == "question_false":
        answers.append({"question": current_question["question_text"], "answer": selected_options})
        #  await state.update_data(answers=answers)
        await state.update_data(confirmed=False)

        if question_index + 1 < len(questions):
            await state.update_data(question_index=question_index + 1)
            await send_next_question(chat_id, bot, state)
        else:
            await bot.send_message(chat_id, "Спасибо за участие в опросе!")
            await state.clear()
    await callback_query.answer('')

async def send_next_question(chat_id: int, bot: Bot, state: FSMContext):
    data = await state.get_data()
    questions = data.get("questions")
    question_index = data.get("question_index", 0)

    if questions is None or question_index >= len(questions):
        await bot.send_message(chat_id, "Произошла ошибка при получении следующего вопроса.")
        return

    current_question = questions[question_index]
    if current_question["question_type"] == "checkbox" and current_question["required"] == True:
        await kb.send_checkbox_question(chat_id, current_question, bot)
    elif current_question["question_type"] == "radio" and current_question["required"] == True:
        await kb.send_radio_question(chat_id, current_question, bot)
    elif current_question["question_type"] == "text" and current_question["required"] == True:
        await kb.send_text_question(chat_id, current_question, bot)
    elif current_question["question_type"] == "checkbox" and current_question["required"] == False:
        await kb.send_checkbox_question_false(chat_id, current_question, bot)
    elif current_question["question_type"] == "radio" and current_question["required"] == False:
        await kb.send_radio_question_false(chat_id, current_question, bot)
    elif current_question["question_type"] == "text" and current_question["required"] == False:
        await kb.send_text_question_false(chat_id, current_question, bot)


@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    user_id = await db.search_user_id(message.from_user.id)
    if user_id == message.from_user.id:
        await message.answer('Вы уже зарегистрированы')
    else:
        await state.set_state(Register.name)
        await message.answer('Введите ваше имя')

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')

@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите только числовое значение для возраста.')
        return

    await state.update_data(age=int(message.text))
    await state.set_state(Register.number)
    await message.answer('Введите ваш номер телефона (только цифры без дополнительных символов)')

@router.message(Register.number)
async def register_number(message: Message, state: FSMContext):
    phone_number = re.search(r'^(\+7|8)?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}$', message.text)

    if not phone_number:
        await message.answer('Пожалуйста, введите только цифры для номера телефона. Попробуйте снова.')
        return
    await state.update_data(number=message.text)
    data = await state.get_data()
    await db.set_col(message.from_user.id, data["name"], data["age"], data["number"])
    await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nВаш телефон: {data["number"]}')
    await state.clear()

@router.message(Command('id'))
async def show_user_id(message: Message):
    user_info = await db.show_id(message.from_user.id)
    if user_info:
        name, age, phone_number = user_info
        await message.answer(f'Ваше имя: {name}\nВаш возраст: {age}\nВаш телефон: {phone_number}')
    else:
        await message.answer('Вы не зарегистрированы. Для регистрации нажмите /register')

@router.message(Command('edit'))
async def edit_info(message: Message, state: FSMContext):
    user_info = await db.show_id(message.from_user.id)
    if user_info:
        await state.set_state(Edit.name)
        await message.answer('Введите новое имя (или текущее, если не хотите изменять)')
    else:
        await message.answer('Вы не зарегистрированы. Для регистрации нажмите /register')

@router.message(Edit.name)
async def edit_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Edit.age)
    await message.answer('Введите новый возраст (или текущий, если не хотите изменять)')

@router.message(Edit.age)
async def edit_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите только числовое значение для возраста.')
        return

    await state.update_data(age=int(message.text))
    await state.set_state(Edit.number)
    await message.answer('Введите новый номер телефона (или текущий, если не хотите изменять)')

@router.message(Edit.number)
async def edit_number(message: Message, state: FSMContext):
    phone_number = re.search(r'^(\+7|8)?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}$', message.text)
    
    if not phone_number:
        await message.answer('Пожалуйста, введите только цифры для номера телефона. Попробуйте снова.')
        return

    await state.update_data(number=message.text)
    data = await state.get_data()
    await db.update_user_info(message.from_user.id, data["name"], data["age"], data["number"])
    await message.answer(f'Ваша информация обновлена:\nИмя: {data["name"]}\nВозраст: {data["age"]}\nТелефон: {data["number"]}')