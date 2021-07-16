"""
	This is telegam bot core.
	Neerv, 2021. yepIwt
"""

import os

import asyncio
from aiogram import Bot, types, executor, Dispatcher

from gameroom import Room

TOKEN = os.getenv("TELEGRAM_API_TOKEN")

class NeervBot:

	def __init__(self, telegram_token):
		self.bot = Bot(token = telegram_token)
		self.rooms = {}

	def get_room(self, telegram_chat_id: int) -> dict or bool:
		there_is_room = self.rooms.get(str(telegram_chat_id))
		if there_is_room:
			return there_is_room
		else:
			self.rooms.setdefault(str(telegram_chat_id), Room(telegram_chat_id))
			return self.rooms.get(str(telegram_chat_id))

	async def log_into_telegram(self, text: str, room_chat_id: int):
		await self.bot.send_message(room_chat_id, text)

	async def send_welcome(self, message: types.Message):
		print(message.chat.id)
		room = self.get_room(message.chat.id)
		await message.answer("Привет\nЭтот бот умеет играть в покер\nДля начала вам нужно присоединиться /join")

	async def join_the_game(self, message: types.Message):
		r = self.get_room(message.from_user.username)
		if r.join_room(message.from_user.username):
			await message.answer("Да, это сработает")
		else:
			await message.answer("Нет, это не сработает")

	async def players_starts_game(self, message: types.Message):
		r = self.get_room(message.from_user.username)
		game_started = r.start_the_game(self.log_into_telegram)
		if game_started:
			await message.answer('11')
		else:
			await message.answer('ne robit')

	def start(self):
		dp = Dispatcher(self.bot)
		dp.register_message_handler(self.send_welcome, commands = ['start'])
		dp.register_message_handler(self.join_the_game, commands = ['join'])
		dp.register_message_handler(self.players_starts_game, commands = ['start_game'])

		executor.start_polling(dp, skip_updates = True)

if __name__ == '__main__':
	b = NeervBot(TOKEN)
	b.start()