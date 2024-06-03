import re
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import database as db

router = Router()

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
        await message.answer('Выберите опрос')
    else:
        await message.answer('Привет! Вы не зарегистрированы. Для регистрации нажмите кнопку /register')

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



