from random import randint

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.hunger = randint(-2, 2) 

class Prey(Entity):
    pass

class Predator(Entity):
    pass