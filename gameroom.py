from game import Game

class Room:

	def __init__(self, telegram_chat_id: int):
		self.room_chat_id = telegram_chat_id
		self.ready_players = []
		self.active = False

	def join_room(self, username: str) -> bool:
		if len(self.ready_players) < 10:
			self.ready_players.append(username)
			return True
		return False

	async def start_the_game(
			self, 
			func_to_wait_action,
			func_to_wait_bet,
			func_to_log
		) -> bool:

		if self.active:
			return False

		if len(self.ready_players) >= 2:
			self.active = True

			self.gamecore = Game()
			self.gamecore.give_func_to_ask(func_to_wait_action)
			self.gamecore.give_func_to_bet(func_to_wait_bet)
			self.gamecore.give_func_to_print(func_to_log)

			for pl_name in self.ready_players:
				self.gamecore.add_player(pl_name,10000)
			return True
		return False