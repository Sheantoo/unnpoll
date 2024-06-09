from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import os


storag=MemoryStorage()
bot = Bot(token ="6458503910:AAGORHNT4np02C_8kp8EaYyTBrdiLxmUnVs")
dp = Dispatcher(bot, storage=storag)
