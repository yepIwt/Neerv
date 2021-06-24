#!/usr/bin/python

from aiogram import Bot, types, executor, Dispatcher

import asyncio
import game

TOKEN = ""
CHAT_ID = None

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

poker = None
action = None
bet = None
event_to_action = None
event_to_bet = None

async def ask_action():
	global event_to_action, action
	event_to_action = asyncio.Event()
	otvet = asyncio.create_task(event_to_action.wait())
	await otvet
	return action

async def ask_bet():
	global event_to_bet,bet
	event_to_bet = asyncio.Event()
	otvet = asyncio.create_task(event_to_bet.wait())
	await otvet
	return bet

async def send_info_to_tg(text):
	global CHAT_ID
	await bot.send_message(CHAT_ID, text)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.answer("Привет\nЭтот бот умеет играть в покер\nИспользуйте /create_game для старта игры")

@dp.message_handler(commands=['create_game'])
async def create_game(message: types.Message):
	global CHAT_ID, poker
	CHAT_ID = message.chat.id

	poker = game.Game()
	poker.give_func_to_ask(ask_action)
	poker.give_func_to_bet(ask_bet)
	poker.give_func_to_print(send_info_to_tg)

	await send_info_to_tg("Neerv - это нервная игра в покер в Телеграме. Берегите свои нервы!")
	poker.add_player("Max",1000)
	poker.add_player("Tim", 2000)
	poker.add_player("Uli", 3000)
	poker.add_player("Nick", 4000)
	poker.add_player("Dim", 5000)

	await send_info_to_tg("Игра начинается... ")

	poker.choose_dealer()
	poker.choose_blinds_players()
	
	button_nick = poker.players[poker.button_player].nickname
	await send_info_to_tg(f"Диллер раздачи: {button_nick}")
	
	await poker.preflop()
	await poker.flop()
	await poker.turn()

@dp.message_handler(commands=['action'])
async def get_action(message: types.Message):
	global event_to_action, action, poker
	args = message.text.split()

	try:
		action = int(args[1])
	except Exception:
		await message.answer("Нихера не понял")
		return

	if action not in poker.avaliable_player_actions():
		await message.answer(f"Это действие вам не доступно. Доступные действия: {poker.avaliable_player_actions()}")
	else:
		event_to_action.set()
	#await message.reply("", reply=False)

@dp.message_handler(commands=['bet'])
async def get_bet(message: types.Message):
	global event_to_bet, bet, poker

	args = message.text.split()
	bet = int(args[1])

	if bet > poker.curr_player().money:
		await message.answer("Твоя ставка больше, чем твой стек")
	elif poker.player_bet > bet:
		await message.answer("Твоя ставка меньше, чем предыдущего игрока")
	else:
		event_to_bet.set()
		await message.reply("Ставка сделана!", reply=False)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)