from aiogram import Bot, types, executor, Dispatcher

import asyncio
import game

TOKEN = "1884944303:AAGXIRtXknkXcIHUaF65sr2kQGl_7JEomP8"
CHAT_ID = None

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

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
	global CHAT_ID
	CHAT_ID = message.chat.id

	poker = game.Game()
	poker.give_func_to_ask(ask_action)
	poker.give_func_to_bet(ask_bet)
	poker.give_func_to_print(send_info_to_tg)

	await send_info_to_tg("Neerv is a nervous poker game. Take care of your nerves!")
	poker.add_player("Max",1000)
	poker.add_player("Tim", 2000)
	poker.add_player("Uli", 3000)
	poker.add_player("Nick", 4000)
	poker.add_player("Dim", 5000)

	await send_info_to_tg("OK. Let's start our game... ")

	poker.choose_dealer()
	poker.choose_blinds_players()
	
	button_nick = poker.players[poker.button_player].nickname
	await send_info_to_tg(f"Button: {button_nick}")

	# раздача карт
	
	poker.make_zero_bets()
	
	await send_info_to_tg(f"{poker.bet_small_blind()} posts the small blind...")
	await send_info_to_tg(f"{poker.bet_big_blind()} posts the big blind...")

	await poker.makeBets()

@dp.message_handler(commands=['action'])
async def get_action(message: types.Message):
	global event_to_action, action
	args = message.text.split()
	action = int(args[1])
	event_to_action.set()
	await message.reply("Registered an action!", reply=False)

@dp.message_handler(commands=['bet'])
async def get_bet(message: types.Message):
	global event_to_bet, bet
	args = message.text.split()
	bet = int(args[1])
	event_to_bet.set()
	await message.reply("Registered bet!", reply=False)



if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)