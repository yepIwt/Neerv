#!/usr/bin/python
from aiogram import Bot, types, executor, Dispatcher
import asyncio

TOKEN = ""

bot = Bot(token = TOKEN)

class StatusBar(object):

	def __init__(self, bot: Bot, chat_id: int):
		self.bot = bot
		self.chat_id = chat_id

	async def pin(self):
		await self.bot.pin_chat_message(
			chat_id = self.chat_id,
			message_id = self.message_id,
			disable_notification = True
		)

	async def send_first_message(self):
		result = await bot.send_message(
			chat_id = self.chat_id,
			text = 'Статус бар инцидент'
		)
		self.message_id = result.message_id
		await self.pin()
	
	async def state(self, text: str):
		await bot.edit_message_text(
			chat_id = self.chat_id, 
			message_id = self.message_id,
			text = text
		)
	async def unpin(self):
		await self.bot.unpin_chat_message(
			chat_id = self.chat_id,
			message_id = self.message_id,
		)

async def main():
	statusbar = StatusBar(bot, moi_tg_id)
	await statusbar.send_first_message()
	await statusbar.pin()
	await statusbar.state('Статус бар: темплейт')
	await statusbar.unpin()

asyncio.run(main())