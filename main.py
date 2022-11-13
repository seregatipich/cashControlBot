import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
storage = MemoryStorage()

bot = Bot(token=token)  # bot object creation
dp = Dispatcher(bot=bot, storage=storage)  # dispatcher object creation


class expense(StatesGroup):
    amount = State()
    date = State()
    desc = State()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message) -> None:
    await message.reply(text="Hi! My name is cashControlBot!\nI was made by @tk104 to assist you with your cash spendings")
    button1 = KeyboardButton('Add expense')
    button2 = KeyboardButton('My expenses')
    button3 = KeyboardButton('Help')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button1, button2, button3)
    await message.answer(text="Choose one of the following options", reply_markup=keyboard)


@dp.message_handler(Text(equals=('Add expense'), ignore_case=True), state=None)
async def add_expense(message: types.Message) -> None:
    await expense.amount.set()
    await bot.send_message('Enter expense amount')


@dp.message_handler(content_types=['text'], state=expense.amount)
async def save_expense_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["amount"] = message.text
    await expense.set()
    await message.reply(text='Now, enter expense date')


@dp.message_handler(content_types=['text'], state=expense.date)
async def save_expense_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["date"] = message.text
    await expense.set()
    await message.reply(text='In the end, enter expence description')


@dp.message_handler(content_types=['text'], state=expense.desc)
async def save_expense_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["desc"] = message.text
    await state.finish()
    
    await message.reply(text='Expense saved!')


@dp.message_handler(commands=['cancel'])
async def cancel(message: types.Message, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return

    await message.reply(text='action canceled')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
