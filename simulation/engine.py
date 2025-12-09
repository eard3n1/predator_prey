import random
from simulation.entities import Prey, Predator
from simulation.grid import Grid
import config

class Simulation:
    def __init__(self, grid_size=config.GRID_SIZE,
                 initial_prey=config.INITIAL_PREY,
                 initial_predators=config.INITIAL_PREDATORS):

        self.grid = Grid()
        self.prey_list = []
        self.predator_list = []

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
            adj = self.grid.get_adjacent_positions(prey.x, prey.y)
            new_x, new_y = random.choice(adj)
            self.grid.move_entity(prey, new_x, new_y)

            if self.grid.local_prey_count(prey.x, prey.y) <= config.CARRYING_CAPACITY:
                if random.random() <= config.PREY_REPRODUCE:
                    new_prey = Prey(prey.x, prey.y)
                    self.prey_list.append(new_prey)
                    self.grid.add_entity(new_prey)

            local_prey_count = self.grid.local_prey_count(prey.x, prey.y)
            if local_prey_count >= config.CARRYING_CAPACITY - 1:
                prey.food_scarcity += 1
            elif local_prey_count <= 1:
                prey.food_scarcity = max(-2, prey.food_scarcity - 1)

            if prey.food_scarcity >= (config.CARRYING_CAPACITY - 1):
                self.prey_list.remove(prey)
                self.grid.cells[prey.y][prey.x].remove(prey)

        for predator in list(self.predator_list):
            adj = self.grid.get_adjacent_positions(predator.x, predator.y)
            prey_targets = []
            for nx, ny in adj:
                prey_targets.extend([e for e in self.grid.get_entities_at(nx, ny) if isinstance(e, Prey)])

            if prey_targets:
                target = random.choice(prey_targets)
                self.grid.move_entity(predator, target.x, target.y)
                self.prey_list.remove(target)
                self.grid.cells[target.y][target.x].remove(target)
                predator.starve_time = max(-2, predator.starve_time - 1)
            else:
                new_x, new_y = random.choice(adj)
                self.grid.move_entity(predator, new_x, new_y)
                predator.starve_time += 1

            if random.random() <= config.PREDATOR_REPRODUCE:
                new_pred = Predator(predator.x, predator.y)
                self.predator_list.append(new_pred)
                self.grid.add_entity(new_pred)

            if predator.starve_time >= config.PREDATOR_STARVE:
                self.predator_list.remove(predator)
                self.grid.cells[predator.y][predator.x].remove(predator)

    def get_grid_state(self):
        state = [[0 for _ in range(config.GRID_SIZE)] for _ in range(config.GRID_SIZE)]
        for prey in self.prey_list:
            state[prey.y][prey.x] = 1
        for pred in self.predator_list:
            state[pred.y][pred.x] = 2
        return state