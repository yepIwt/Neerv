"""
	This is StatusBar for gaming core.
	Neerv, 2021. yepIwt
"""

class StatusBar(object):

	async def setup(self, ClassUpper):
		self.ghost_class = ClassUpper
		#initialize
		result = await self.ghost_class.gamebar.api.send_message(
			chat_id = self.ghost_class.gamebar.chat_id,
			reply_to_message_id = self.ghost_class.gamebar.message_id,
			text = 'Статус бар инцидент'
		)
		ClassUpper.statusbar.message_id = result.message_id
		ClassUpper.statusbar.state = self.state
		self.ghost_class.statusbar.prev_state = None
		await self.pin()

	async def pin(self):
		await self.ghost_class.gamebar.api.pin_chat_message(
			chat_id = self.ghost_class.gamebar.chat_id,
			message_id = self.ghost_class.statusbar.message_id,
			disable_notification = True
		)

	async def state(self, text: str):
		await self.ghost_class.gamebar.api.edit_message_text(
			chat_id = self.ghost_class.gamebar.chat_id, 
			message_id = self.ghost_class.statusbar.message_id,
			text = text
		)
		self.ghost_class.statusbar.prev_state = text

	async def unpin(self):
		await self.ghost_class.gamebar.api.unpin_chat_message(
			chat_id = self.ghost_class.gamebar.chat_id,
			message_id = self.ghost_class.statusbar.message_id,
		)