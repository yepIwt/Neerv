#!/usr/bin/python

from aiogram import Bot, types, executor, Dispatcher
from status import StatusBar
import asyncio
import game

import os
import hashlib

TOKEN = os.getenv("TELEGRAM_API_TOKEN")

class NeervBot(object):

	def __init__(self, tg_token: str):
		self.bot = Bot(token = tg_token)

		self.ready_players = ["codeyouth","fuckinyouth"]
		self.CHAT_ID = None

		self.event_to_bet = None
		self.bet = 0
		self.event_to_action = None
		self.action = 0

	async def send_info_to_tg(self, text: str):
		await self.bot.send_message(self.CHAT_ID, text)

	async def ask_bet(self):
		self.event_to_bet = asyncio.Event()
		otvet = asyncio.create_task(self.event_to_bet.wait())
		await otvet

		return self.bet

	async def ask_action(self):
		self.event_to_action = asyncio.Event()
		otvet = asyncio.create_task(self.event_to_action.wait())
		await otvet

		return self.action

	async def get_action(self, message: types.Message):
		args = message.text.split()
		try:
			self.action = int(args[1])
		except Exception:
			await message.answer("Нихера не понял")
			return

		if self.action not in self.poker.avaliable_player_actions():
			await message.answer(f"Это действие вам не доступно. Доступные действия: {poker.avaliable_player_actions()}")
		else:
			self.event_to_action.set()

	async def get_bet(self, message: types.Message):
		args = message.text.split()
		self.bet = int(args[1])
		if self.bet > self.poker.curr_player().money:
			await message.answer("Твоя ставка больше, чем твой стек")
		elif self.poker.player_bet > self.bet:
			await message.answer("Твоя ставка меньше, чем предыдущего игрока")
		else:
			self.event_to_bet.set()
			await message.reply("Ставка сделана!", reply=False)

	async def send_welcome(self, message: types.Message):
		self.CHAT_ID = message.chat.id
		await message.answer("Привет\nЭтот бот умеет играть в покер\nДля начала вам нужно присоединиться /join")

	async def join_the_game(self, message: types.Message):
		if message.from_user.username not in self.ready_players:
			self.ready_players.append(message.from_user.username)
			await message.answer('Игрок зарегистрирован')
		else:
			await message.answer('Вы уже в игре')

	async def create_game(self, message: types.Message):
		self.CHAT_ID = message.chat.id
		if len(self.ready_players) > 1:
			self.poker = game.Game()
			self.poker.give_func_to_ask(self.ask_action)
			self.poker.give_func_to_bet(self.ask_bet)
			self.poker.give_func_to_print(self.send_info_to_tg)

			for player in self.ready_players:
				self.poker.add_player(player,10000)

			await self.poker.install_gamebar(self.CHAT_ID, self.bot)
			await self.poker.install_statusbar(self.CHAT_ID, self.bot)

			await self.send_info_to_tg("Игра начинается... ")

			self.poker.choose_dealer()
			self.poker.choose_blinds_players()

			await self.poker.preflop()
			await self.poker.flop()
			await self.poker.turn()
			await self.poker.river()

			await self.poker.end_game()
		else:
			await message.answer("Мало игроков")

	def actions_in_stickers(self, actions_list: list, return_names_of_actions = None):
		fold_button = types.InlineQueryResultCachedSticker(
			id = hashlib.md5("Fold".encode()).hexdigest(),
			sticker_file_id = "CAACAgIAAxkBAAM5YOiAQnbP9nf49ch8jAJmR7U9k8MAAlcAAzIFORiWLzoki4sveiAE",
			input_message_content = types.InputTextMessageContent("I'm fold"),
		)

		bet_button = types.InlineQueryResultCachedSticker(
			id = hashlib.md5("Bet".encode()).hexdigest(),
			sticker_file_id = "CAACAgIAAxkBAAM9YOiAX5lhR6YbIlWMv_HrSEGTxh0AAlIAAzIFORj7OKABGnVZAyAE",
			input_message_content = types.InputTextMessageContent("I'm bet"),
		)

		call_button = types.InlineQueryResultCachedSticker(
			id = hashlib.md5("Call".encode()).hexdigest(),
			sticker_file_id = "CAACAgIAAxkBAAM7YOiAUjpix9IimUI8qLoVtVbSX3AAAlAAAzIFORh2dTnvg4QZTiAE",
			input_message_content = types.InputTextMessageContent("I'm call"),
		)

		all_in_button = types.InlineQueryResultCachedSticker(
			id = hashlib.md5("All-in".encode()).hexdigest(),
			sticker_file_id = "CAACAgIAAxkBAAM_YOiAbXMziu3V-qvBWv7UY28Oq2sAAkYAAzIFORg9xud64l5qyiAE",
			input_message_content = types.InputTextMessageContent("I'm all-in"),
		)

		check_button = types.InlineQueryResultCachedSticker(
			id = hashlib.md5("Check".encode()).hexdigest(),
			sticker_file_id = "CAACAgIAAxkBAANDYOjGJo7779HJTT2R6FdWfKx-2i8AAlUAAzIFORjP7OBQVLWSwyAE",
			input_message_content = types.InputTextMessageContent("I'm check"),
		)

		if actions_list == [1,4]:
			return [fold_button, all_in_button]
		elif actions_list == [1,3]:
			return [fold_button, call_button]
		elif actions_list == [1,2,4,5]:
			return [fold_button, bet_button, all_in_button, check_button]
		elif actions_list == [1,2,3,4]:
			return [fold_button, bet_button, call_button, all_in_button ]

	async def inline_process(self, inline_query):
		if self.poker:
			if inline_query.from_user.username == self.poker.curr_player().nickname:
				await self.bot.answer_inline_query(
					inline_query.id,
					is_personal = True,
					results = self.actions_in_stickers(self.poker.avaliable_player_actions()),
					cache_time = 1
				)
			else:
				await self.bot.answer_inline_query(
					inline_query.id,
					is_personal = True,
					results = [],
					cache_time = 1
				)


	async def catch_all_messages(self, message: types.Message):
		
		if self.poker.curr_player().nickname == message.from_user.username:
			if message.text == "I'm fold":
				self.action = 1
			elif message.text == "I'm bet":
				self.action = 2
			elif message.text == "I'm call":
				self.action = 3
			elif message.text == "I'm all-in":
				self.action = 4
			elif message.text == "I'm check":
				self.action = 5
			else:
				return

		if self.action in self.poker.avaliable_player_actions():
			self.event_to_action.set()
		else:
			await message.answer("Сукин сын! Играй по правилам! Используй инлайн, а если не используешь, то выбирай правильные действия")

	def start(self):
		dp = Dispatcher(self.bot)
		dp.register_message_handler(self.send_welcome, commands = ['start'])
		dp.register_message_handler(self.join_the_game, commands = ['join'])
		dp.register_message_handler(self.get_action, commands = ['action'])
		dp.register_message_handler(self.get_bet, commands = ['bet'])
		dp.register_message_handler(self.create_game, commands = ['create_game'])
		dp.register_message_handler(self.catch_all_messages, content_types = ['text'])
		dp.register_inline_handler(self.inline_process)

		executor.start_polling(dp, skip_updates = True)

if __name__ == '__main__':
	n = NeervBot(TOKEN)
	n.start()