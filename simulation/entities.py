import random

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Prey(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.food_scarcity = random.randint(-2, 2)

class Predator(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.starve_time = random.randint(-2, 2)
