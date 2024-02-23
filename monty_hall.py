import random
from pprint import pprint


class MontyHallGame:
    def __init__(self):
        self.door_with_car = -1
        self.door_picked_by_player = -1

    def reset(self):
        self.door_with_car = random.randint(0, 2)

    def pick_first_door(self):
        self.door_picked_by_player = random.randint(0, 2)

    def game_result(self, strategy) -> bool:
        if strategy == "stay":
            return self.door_picked_by_player == self.door_with_car
        elif strategy == "switch":
            new_door = -1
            while new_door != self.door_picked_by_player and new_door != self.door_with_car:
                new_door = random.randint(0, 2)
            return new_door == self.door_with_car
        else:
            return False


monty_hall_game = MontyHallGame()

wins = {"stay": 0, "switch": 0}

for strategy in ["stay", "switch"]:
    for i in range(1000000):
        monty_hall_game.reset()
        won = monty_hall_game.pick_first_door()
        if won:
            wins[strategy] += 1
        else:
            won = monty_hall_game.game_result(strategy)
            if won:
                wins[strategy] += 1


pprint(wins)
