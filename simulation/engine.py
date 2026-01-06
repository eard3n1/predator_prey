import random
from simulation.entities import Prey, Predator
from simulation.grid import Grid
from config import *

class Simulation:
    def __init__(self, grid_size=GRID_SIZE,
                 initial_prey=INITIAL_PREY,
                 initial_predators=INITIAL_PREDATORS,
                 prey_reproduce=PREY_REPRODUCE,
                 predator_reproduce=PREDATOR_REPRODUCE,
                 predator_starve=PREDATOR_STARVE,
                 carrying_capacity=CARRYING_CAPACITY):

        self.grid = Grid()
        self.prey_list = []
        self.predator_list = []

        self.grid_size = grid_size
        self.prey_reproduce = prey_reproduce
        self.predator_reproduce = predator_reproduce
        self.predator_starve = predator_starve
        self.carrying_capacity = carrying_capacity

        for _ in range(initial_prey):
            x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
            prey = Prey(x, y)
            self.prey_list.append(prey)
            self.grid.add_entity(prey)

        for _ in range(initial_predators):
            x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
            predator = Predator(x, y)
            self.predator_list.append(predator)
            self.grid.add_entity(predator)

    def update(self):
        for prey in list(self.prey_list):
            adj = self.grid.adjacent_position(prey.x, prey.y)
            new_x, new_y = random.choice(adj)
            self.grid.move_entity(prey, new_x, new_y)

            local_prey = self.grid.local_count(prey.x, prey.y)
            if local_prey <= self.carrying_capacity:
                if self.prey_reproduce >= random.random():
                    new_prey = Prey(prey.x, prey.y)
                    self.prey_list.append(new_prey)
                    self.grid.add_entity(new_prey)
                    prey.hunger += 1
            
            if local_prey >= self.carrying_capacity:
                prey.hunger += 1
            elif local_prey <= 1:
                prey.hunger -= 1

            if (prey.hunger >= self.carrying_capacity) or (prey.age >= 10 and random.randint(1, 10) == 1):
                self.prey_list.remove(prey)
                self.grid.cells[prey.y][prey.x].remove(prey)
            prey.age += 1

        for predator in list(self.predator_list):
            adj = self.grid.adjacent_position(predator.x, predator.y)
            prey_targets = []
            for nx, ny in adj:
                prey_targets.extend([e for e in self.grid.get_entity(nx, ny) if isinstance(e, Prey)])

            if prey_targets:
                target = random.choice(prey_targets)
                self.grid.move_entity(predator, target.x, target.y)
                self.prey_list.remove(target)
                self.grid.cells[target.y][target.x].remove(target)
                predator.hunger -= 1
            else:
                new_x, new_y = random.choice(adj)
                self.grid.move_entity(predator, new_x, new_y)
                predator.hunger += 1

            local_predator = self.grid.local_count(predator.x, predator.y)   
            if local_predator <= self.carrying_capacity:
                if self.predator_reproduce >= random.random(): 
                    new_pred = Predator(predator.x, predator.y)
                    self.predator_list.append(new_pred)
                    self.grid.add_entity(new_pred)
                    predator.hunger += 1

            if (predator.hunger >= self.predator_starve) or (predator.age >= 10 and random.randint(1, 10) == 1):
                self.predator_list.remove(predator)
                self.grid.cells[predator.y][predator.x].remove(predator)
            predator.age += 1

    def grid_state(self):
        state = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for prey in self.prey_list:
            state[prey.y][prey.x] = 1
        for pred in self.predator_list:
            state[pred.y][pred.x] = 2
        return state # 0: empty, 1: prey, 2: predator