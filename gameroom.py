from game import Game

class Room:

	def __init__(self, telegram_chat_id: int):
		self.room_chat_id = telegram_chat_id
		self.ready_players = []
		self.active = False

		self.asyncio_event_to_ask = None
		self.asyncio_event_to_bet = None

		self.locked_act = None
		self.locked_bet = None

	async def asynclock_act(self) -> int:
		self.asyncio_event_to_ask = asyncio.Event()
		stop = asyncio.create_task(self.asyncio_event_to_ask.wait())
		await stop

		return self.locked_act

	async def asynclock_act(self) -> int:
		self.asyncio_event_to_bet = asyncio.Event()
		stop = asyncio.create_task(self.asyncio_event_to_bet.wait())
		await stop

		return self.locked_bet

	async def player_just_bet(self, bet_val: int):
		pass

	def join_room(self, username: str) -> bool:
		if len(self.ready_players) < 10 and username not in self.ready_players:
			self.ready_players.append(username)
			return True
		return False

	def start_the_game(self, func_to_log) -> bool:

		if self.active:
			return False

		if len(self.ready_players) >= 2:
			self.active = True

			self.gamecore = Game()
			self.gamecore.give_func_to_ask(self.asynclock_act)
			self.gamecore.give_func_to_bet(func_to_wait_bet)
			self.gamecore.give_func_to_print(func_to_log)

			for pl_name in self.ready_players:
				self.gamecore.add_player(pl_name,10000)

			self.ready_players = []
			return True
		return False