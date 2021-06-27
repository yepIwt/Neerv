"""
	This is GameBar for gaming core.
	Neerv, 2021. yepIwt
"""

ACTIONS = [
	'ожидает...',
	'фолдит...',
	'беттит ',
	'коллирует', 
	'олл-ин',
	'ожидает',
	'ставит малый блайнд',
	'ставит большой блайнд'
]

class GameBar(object):

	async def setup(self, ClassUpper, chat_id, bot):
		ClassUpper.gamebar.chat_id = chat_id
		ClassUpper.gamebar.api = bot
		self.ghost_class = ClassUpper

		result = await self.ghost_class.gamebar.api.send_message(
			chat_id = chat_id,
			text = 'ГеймБар инцидент'
		)

		ClassUpper.gamebar.message_id = result.message_id
		ClassUpper.gamebar.draw = self.draw
	
	def get_text_action(self,act,i):
		global ACTIONS
		if i == self.ghost_class.cursor:
			return "думает..."
		return ACTIONS[act]

	async def draw(self):
		pretty_text = "Игровой бар:\n"
		for i in range(len(self.ghost_class.players)):
			if self.ghost_class.cursor == i:
				pretty_text += "🔴"
			else:
				pretty_text += "⚪️"

			if self.ghost_class.small_blind_player == i:
				pretty_text += " (sb)"
			elif self.ghost_class.big_blind_player == i:
				pretty_text += " (bb)"
			elif self.ghost_class.button_player == i:
				pretty_text += " (DL)"
			pretty_text += f" @{self.ghost_class.players[i].nickname} "
			pretty_text += f"[{self.ghost_class.bets[i]}$]: "
			pretty_text += f"{self.get_text_action(self.ghost_class.players_actions[i],i)}\n"

		pretty_text += f"\nПоследняя ставка: {self.ghost_class.player_bet}$\n"
		pretty_text += f"Банк раздачи (POT): {self.ghost_class.calc_pot()}$"	

		await self.ghost_class.gamebar.api.edit_message_text(
			chat_id = self.ghost_class.gamebar.chat_id,
			message_id = self.ghost_class.gamebar.message_id,
			text = pretty_text
		)