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
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b170c","document_name":"фффф","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}',
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b270c","document_name":"выола","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}',
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b370c","document_name":"ылова","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}',
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b470c","document_name":"зщшз","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}',
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b570c","document_name":"ывлорщ","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}'
]
arr = prs.parse_json_document(js_arr)
        
items = [arr[0]['document_name'],arr[1]['document_name'],arr[2]['document_name'],arr[3]['document_name'],arr[4]['document_name']]
print(items)
class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

class Edit(StatesGroup):
    name = State()
    age = State()
    number = State()

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



