from config import GRID_SIZE

class Grid:
    def __init__(self):
        self.cells = [[[] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def add_entity(self, entity):
        self.cells[entity.y][entity.x].append(entity)

    def move_entity(self, entity, new_x, new_y):
        self.cells[entity.y][entity.x].remove(entity)
        entity.x = new_x % GRID_SIZE
        entity.y = new_y % GRID_SIZE
        self.cells[entity.y][entity.x].append(entity)

    def get_adjacent_positions(self, x, y):
        positions = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % GRID_SIZE
                ny = (y + dy) % GRID_SIZE
                positions.append((nx, ny))
        return positions

    def get_entities_at(self, x, y):
        return self.cells[y][x]

    def local_count(self, x, y):
        count = 0
        for nx, ny in self.get_adjacent_positions(x, y) + [(x, y)]:
            count += sum(1 for e in self.cells[ny][nx] if e.__class__.__name__ == "Prey" or e.__class__.__name__ == "Predator")
        return count
