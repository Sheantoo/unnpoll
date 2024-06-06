from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

class Survey(StatesGroup):
    Question = State()
    Answer = State()

bot = Bot(token="TOKEN")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

js_arr = [
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b170c","document_name":"фффф","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}',
    # остальные элементы массива js_arr
]

async def generate_question_keyboard(question_data):
    parsed_data = json.loads(question_data)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for question in parsed_data['questions']:
        button_text = question['questionText']
        callback_data = f'answer_{question["questionText"]}'
        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return keyboard

@dp.message_handler(commands=['start'])
async def start_survey(message: types.Message):
    await Survey.Question.set()
    await message.answer("Привет! Давай пройдем опрос.")
    await show_next_question(message)

async def show_next_question(message: types.Message):
    current_question_index = await bot.get_data(message)['current_question_index']
    if current_question_index < len(js_arr):
        question_data = js_arr[current_question_index]
        keyboard = await generate_question_keyboard(question_data)
        await message.answer("Вопрос:")
        await message.answer("Варианты ответа:", reply_markup=keyboard)
    else:
        await message.answer("Это был последний вопрос.")

@dp.callback_query_handler(lambda c: c.data.startswith('answer_'), state=Survey.Question)
async def process_answer_callback(callback_query: types.CallbackQuery, state: FSMContext):
    answer = callback_query.data.split('_')[1]  # Извлекаем ответ из callback_data
    await state.update_data(answer=answer)
    await Survey.Answer.set()
    await callback_query.message.answer("Ответ сохранен. Пожалуйста, ожидайте следующий вопрос.")
    await show_next_question(callback_query.message)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
