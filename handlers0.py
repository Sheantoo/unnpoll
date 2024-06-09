import re
from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import database as db
import keyboards as kb
import prs

router = Router()
js_arr = [
    '{"doc_id":"2299a939-d9a3-6a33-815f-4f9dfc8a8fc0","document_name":"Предпочтения слушателей подкастов","doc_desc":"","questions":[{"questionText":"Укажите ваш пол","qustionType":"radio","options":[{"optionText":"Мужской"},{"optionText":"Женский"}],"open":false,"required":true},{"questionText":"Укажите ваш возраст","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":true},{"questionText":"Укажите уровень вашего образования","qustionType":"radio","options":[{"optionText":"неполное высшее"},{"optionText":"высшее"},{"optionText":"среднее"}],"open":false,"required":true},{"questionText":"Слушаете ли вы подкасты о культуре?","qustionType":"radio","options":[{"optionText":"Да"},{"optionText":"Нет"}],"open":false,"required":true},{"questionText":"Хотели бы вы узнать больше о событиях в сфере культуры вашего города? ","qustionType":"radio","options":[{"optionText":"Да"},{"optionText":"Нет"}],"open":false,"required":true},{"questionText":"В каком формате Вам было бы комфортнее слушать подкаст?","qustionType":"radio","options":[{"optionText":"Каждое направление - отдельный сезон подкаста"},{"optionText":"Каждый выпуск - новое направление, в одном сезоне несколько направлений в сфере культуры."}],"open":false,"required":true},{"questionText":"Оцените ваш интерес к теме культуры от 1 до 5:","qustionType":"radio","options":[{"optionText":"1"},{"optionText":"2"},{"optionText":"3"},{"optionText":"4"},{"optionText":"5"}],"open":true,"required":true}]}',
    '{"doc_id":"ae7e6026-c01b-f136-f5e1-c4244405e46a","document_name":"Жизненные планы молодежи","doc_desc":"","questions":[{"questionText":"КАК ИЗМЕНИЛАСЬ ВАША ЖИЗНЬ ЗА ПОСЛЕДНИЕ 1,5-2 ГОДА?","qustionType":"radio","options":[{"optionText":"Стала заметно лучше"},{"optionText":"Немного улучшилась"},{"optionText":"Практически не изменилась"},{"optionText":"Немного ухудшилась"},{"optionText":"Стала гораздо хуже"}],"open":false,"required":true},{"questionText":"С КАКИМИ ЧУВСТВАМИ ВЫ ДУМАЕТЕ О СВОЕМ БУДУЩЕМ?","qustionType":"radio","options":[{"optionText":"С надеждой, оптимизмом"},{"optionText":"Спокойно, без иллюзий"},{"optionText":"С беспокойством, тревогой"},{"optionText":"Со страхом и отчаянием"}],"open":false,"required":true},{"questionText":"КТО И ЧТО ПОМОГАЕТ ВАМ ПРИ ВЫБОРЕ МЕСТА БУДУЩЕЙ РАБОТЫ/УЧЕБЫ И МЕСТА ЖИТЕЛЬСТВА? ","qustionType":"checkbox","options":[{"optionText":"Советы семьи"},{"optionText":"Советы учителей (преподавателей)"},{"optionText":"Интернет"},{"optionText":"Советы друзей"},{"optionText":"Публикации в газетах и журналах"}],"open":false,"required":true},{"questionText":"КАК ВЫ ДУМАЕТЕ, ПОЧЕМУ МОЛОДЫЕ ЛЮДИ УЕЗЖАЮТ ИЗ СВОЕГО НАСЕЛЕННОГО ПУНКТА? ","qustionType":"checkbox","options":[{"optionText":"Хотят найти интересную работу"},{"optionText":"Хотят получать хорошую зарплату"},{"optionText":"Желают сделать карьеру"},{"optionText":"Хотят поменять место жительства"},{"optionText":"Стремятся получить более качественное образование"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: За границей больше возможностей для карьерного роста","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: За границей выше уровень безопасности","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: За границей лучше развиты инфраструктура и услуги, которые улучшают комфорт жизни","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: Качество жизни в зарубежных странах выше, чем в России","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: Меня привлекает идея познания новых культур и обычаев, которые представлены в зарубежных странах","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: Я бы хотел(а) путешествовать по различным странам","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"Согласны ли вы с утверждением: Мне интересно изучать иностранные языки","qustionType":"radio","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":false,"required":false},{"questionText":"ЧТО, ПО-ВАШЕМУ, ВАЖНО, ЧТОБЫ СЧИТАТЬ СЕБЯ УСПЕШНЫМ В ЖИЗНИ?","qustionType":"checkbox","options":[{"optionText":"Иметь высшее образование"},{"optionText":"Иметь престижную профессию"},{"optionText":"Сделать карьеру"},{"optionText":"Получать большую заработную плату"},{"optionText":"Реализовать свои таланты"}],"open":true,"required":false}]}',
    '{"doc_id":"60d367a0-ec26-f6cc-5059-0db11879d149","document_name":"Влияние интернет-рекламы на поведение студенческой молодежи","doc_desc":"","questions":[{"questionText":"Сколько времени в сутки Вы проводите в интернете?","qustionType":"radio","options":[{"optionText":"Менее 1 часа"},{"optionText":"1-2 часа"},{"optionText":"3-4 часа"},{"optionText":"Более 4 часов"}],"open":true,"required":false},{"questionText":"Какое устройство Вы чаще используете для выхода в интернет?","qustionType":"radio","options":[{"optionText":"Смартфон"},{"optionText":"Ноутбук"},{"optionText":"Планшет"},{"optionText":"Компьютер"}],"open":false,"required":false},{"questionText":"Какие из сервисов Вы чаще всего используете?","qustionType":"checkbox","options":[{"optionText":"Видеохостинги (YouTube)"},{"optionText":"Социальные сети"},{"optionText":"Веб-браузер"},{"optionText":"Онлайн-магазины"}],"open":false,"required":false},{"questionText":"Как Вы относитесь к рекламе в целом?","qustionType":"radio","options":[{"optionText":"Положительно"},{"optionText":"Нейтрально"},{"optionText":"Отрицательно"}],"open":false,"required":false},{"questionText":"Как Вы считаете, какие из следующих факторов наиболее сильно раздражают в рекламе?","qustionType":"radio","options":[{"optionText":"Навязчивость рекламы (всплывающие окна, автоматическое воспроизведение рекламы)"},{"optionText":"Нежелательная персонализация (реклама, подобранная под Вас путем сбора данных о Вашей активности)"},{"optionText":"Неправдивая реклама (реклама с нерабочими промокодами, обманом относительно цены, функций товара и тд.)"}],"open":false,"required":false},{"questionText":"Как часто Вы обращаете внимание на рекламу в интернете?","qustionType":"radio","options":[{"optionText":"Почти всегда"},{"optionText":"Часто"},{"optionText":"Иногда"},{"optionText":"Редко"},{"optionText":"Никогда"}],"open":false,"required":false},{"questionText":"Сколько раз за последний месяц Вы совершали покупки товаров, увиденных в интернет-рекламе?","qustionType":"radio","options":[{"optionText":"Ни разу"},{"optionText":"1-2 раза"},{"optionText":"3-5 раз"}],"open":false,"required":false},{"questionText":"Какие из следующих факторов наиболее важны для Вас при покупке товара?","qustionType":"checkbox","options":[{"optionText":"Мода"},{"optionText":"Страна-производитель"},{"optionText":"Цена"},{"optionText":"Качество"}],"open":false,"required":false},{"questionText":"Какие товары Вы чаще предпочитаете покупать вживую?","qustionType":"checkbox","options":[{"optionText":"Одежда и обувь"},{"optionText":"Электроника и техника"},{"optionText":"Продукты питания"},{"optionText":"Книги и другой досуг (фильмы, музыка)"}],"open":false,"required":false},{"questionText":"Как реклама чаще влияет на формуВашего выбора покупки онлайн или вживую?","qustionType":"radio","options":[{"optionText":"Побуждает к покупке вживую"},{"optionText":"Побуждает к онлайн покупке"},{"optionText":"Никак не влияет на выбор"},{"optionText":"Затрудняюсь ответить"}],"open":false,"required":false},{"questionText":"Согласны ли Вы с утверждением, что интернет-реклама влияет на Ваш выбор товаров?","qustionType":"radio","options":[{"optionText":"Полностью согласен"},{"optionText":"Согласен частично"},{"optionText":"Частично не согласен"},{"optionText":"Полностью не согласен"}],"open":false,"required":false},{"questionText":"Укажите ваш пол","qustionType":"radio","options":[{"optionText":"Мужской"},{"optionText":"Женский"}],"open":false,"required":false},{"questionText":"Укажите Ваш уровень образования","qustionType":"radio","options":[{"optionText":"Бакалавриат"},{"optionText":"Специалитет"},{"optionText":"Магистратура"},{"optionText":"Аспирантура"}],"open":false,"required":false}]}',
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b170c","document_name":"фффф","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}'
]
arr = prs.parse_json_document(js_arr)
        
items = [arr[0]['document_name'],arr[1]['document_name'],arr[2]['document_name'],arr[3]['document_name']]
print(items)
class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

class Edit(StatesGroup):
    name = State()
    age = State()
    number = State()

class QuizStates(StatesGroup):
    waiting_for_answer = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = await db.search_user_id(message.from_user.id)
    if user_id == message.from_user.id:
        await message.answer('Выберите опрос', reply_markup= kb.create_dynamic_keyboard(items))
    else:
        await message.answer('Привет! Вы не зарегистрированы. Для регистрации нажмите кнопку /register')

@router.callback_query(lambda c: c.data.startswith('next_') or c.data.startswith('prev_'))
async def handle_pagination(callback_query: CallbackQuery):
    page = int(callback_query.data.split('_')[1])
    keyboard = kb.create_dynamic_keyboard(items, page=page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)




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
    await state.finish()

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



