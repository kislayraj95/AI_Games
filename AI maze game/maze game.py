from __future__ import annotations
from re import I
from typing import Optional
from a2_support import UserInterface, TextInterface
from constants import *


# Uncomment this function when you have completed the Level class and are ready
# to attempt the Model class.

def load_game(filename: str) -> list['Level']:
    """ Reads a game file and creates a list of all the levels in order.
    
    Parameters:
        filename: The path to the game file
    
    Returns:
        A list of all Level instances to play in the game
    """
    levels = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Maze'):
                _, _, dimensions = line[5:].partition(' - ')
                dimensions = [int(item) for item in dimensions.split()]
                levels.append(Level(dimensions))
            elif len(line) > 0 and len(levels) > 0:
                levels[-1].add_row(line)
    return levels


# Write your classes here

class Tile:
    """ Represpents the floor for a (row, column) position"""
    
    def __init__(self) -> None:
        self.blocking = False
        self.damages = 0
        self.id = ABSTRACT_TILE


    def is_blocking(self) -> bool:
        """Returns True iﬀ the tile is blocking. 
        A tile is blocking if a player would not be allowed to move onto the position it occupies.
        By default, tile’s are not blocking."""
        return self.blocking
    
    def damage(self) -> int:
        """Returns the damage done to a player if they step on this tile. 
        For instance, if a tile has a damage of 3, the player’s HP would be reduced by 3 if they step onto the tile. 
        By default, tile’s should do no damage to a player."""
        return self.damages
    
    def get_id(self) -> str:
        """Returns the ID of the tile. For non-abstract subclasses, the ID should be a single character representing the type of Tile it is. 
        See constants.py for the ID value of all tiles and entities."""
        return self.id

    def __str__(self) -> str:
        """Returns the string representation for this Tile."""
        #直接返回Tile ID
        return self.id

    def __repr__(self) -> str:
        """Returns the text that would be required to create a new instance of this class."""
        return 'Tile()'

class Wall(Tile):
    """Wall is a type of Tile that is blocking."""
    def __init__(self):
        super().__init__()
        self.blocking = True
        self.id = WALL

    def __repr__(self) -> str:
        return 'Wall()'

class Empty(Tile):
    """Empty is a type of Tile that does not contain anything special. A player can move freely over empty tiles without taking any damage. 
    Note that the ID for an empty tile is a single space (not an empty string)."""
    def __init__(self) -> None:
        super().__init__()
        self.id = EMPTY

    def __repr__(self) -> str:
        return 'Empty()'

class Lava(Tile):
    """Lava is a type of Tile that is not blocking, but does a damage of 5 to the player’s HP when stepped on."""
    def __init__(self) -> None:
        super().__init__()
        self.damages = LAVA_DAMAGE
        self.id = LAVA
    
    def __repr__(self) -> str:
        return 'Lava()'

class Door(Tile):
    """Door is a type of Tile that starts as locked (blocking). Once the player has collected all coins in a given maze, 
    the door is ‘unlocked’ (becomes non-blocking and has its ID change to that of an empty tile), 
    and the player can move through the square containing the unlocked door to complete the level. 
    In order to facilitate this functionality in later classes, 
    the Door class must provide a method through which to ‘unlock’ a door."""

    """ 通過一個狀態(Flag)表示門是否上鎖, is blocking和get id都要判斷這個狀態
    從而返回不同的結果"""
    def __init__(self) -> None:
        super().__init__()
        self.blocking = True
        self.id = DOOR

    def unlock(self) -> None:
        """Unlocks the door."""
        self.blocking = False
        self.id = ' '
    
    def __repr__(self) -> str:
        return 'Door()'


class Entity:
    def __init__(self, position) -> None:
        self.position = position
        self.name = 'Entity'
        self.id = 'E'

    def get_position(self) -> tuple:
        """Returns the position of the entity."""
        return self.position

    def get_name(self) -> str:
        """Returns the name of the class."""
        return self.name

    def get_id(self) -> str:
        """Returns the ID of the entity. For non-abstract subclasses, the ID should be a single character representing the type of the Entity"""
        return self.id
    
    def __str__(self) -> str:
        """Returns the string representation for this Entity (the ID)."""
        return self.id

    def __repr__(self) -> str:
        """Returns the text that would be required to create a new instance of this class that looks identical (where possible) to self."""
        return f'Entity({self.position})'

class DynamicEntity(Entity):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.name = 'DynamicEntity'
        self.id = DYNAMIC_ENTITY

    def set_position(self, new_position: tuple) -> None:
        """updates the DynamicEntity's position to the new_position, assuming it is a valid position"""
        self.position = new_position
    
    def __repr__(self) -> str:
        return f'DynamicEntity({self.position})'

class Player(DynamicEntity):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.name = 'Player'
        self.id = PLAYER
        self.health = MAX_HEALTH
        self.hunger = 0
        self.thirst = 0
        self.inventory = Inventory()

    def get_hunger(self) -> int:
        """Returns the hunger of the player."""
        return self.hunger

    def get_thirst(self) -> int:
        """Returns the thirst of the player."""
        return self.thirst

    def get_health(self) -> int:
        """Returns the player's current health."""
        return self.health

    def change_hunger(self, amount) -> None:
        """Increases the player's hunger by amount."""
        if self.hunger + amount < 0:
            self.hunger = 0
        elif self.hunger + amount > MAX_HUNGER:
            self.hunger = MAX_HUNGER
        else:
            self.hunger += amount

    def change_thirst(self, amount) -> None:
        """Increases the player's thirst by amount."""
        if self.thirst + amount < 0:
            self.thirst = 0
        elif self.thirst + amount > MAX_THIRST:
            self.thirst = MAX_HUNGER
        else:
            self.thirst += amount

    def change_health(self, amount) -> None:
        """Increases the player's health by amount."""
        if self.health + amount < 0:
            self.health = 0
        elif self.health + amount > 100:
            self.health = 100
        else:
            self.health += amount

    def get_inventory(self):
        return self.inventory

    def add_item(self, item):
        return self.inventory.add_item(item)

    def __repr__(self) -> str:
        return f'Player({self.position})'

class Item(Entity):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.name = ITEM
        self.id = 'I'
    
    def apply(self, player: Player) -> None:
        """Applies the items effect, if any, to the given player."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f'Item({self.position})'

class Potion(Item):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.name = 'Potion'
        self.id = POTION

    def apply(self, player: Player) -> None:
        """Applies the items effect, if any, to the given player."""
        player.change_health(20)

    def __repr__(self) -> str:
        return f'Potion({self.position})'

class Coin(Item):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.name = 'Coin'
        self.id = COIN

    def apply(self, player: Player) -> None:
        pass

    def __repr__(self) -> str:
        return f'Coin({self.position})'

class Water(Item):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.name = 'Water'
        self.id = WATER

    def apply(self, player: Player) -> None:
        """Applies the items effect, if any, to the given player."""
        player.change_thirst(WATER_AMOUNT)

    def __repr__(self) -> str:
        return f'Water({self.position})'

class Food(Item):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.name = 'Food'
        self.id = FOOD

    def apply(self, player: Player) -> None:
        """Applies the items effect, if any, to the given player."""
        pass

    def __repr__(self) -> str:
        return f'Food({self.position})'

class Apple(Food):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.name = 'Apple'
        self.id = APPLE

    def apply(self, player: Player) -> None:
        """Applies the items effect, if any, to the given player."""
        player.change_hunger(APPLE_AMOUNT)

    def __repr__(self) -> str:
        return f'Apple({self.position})'

class Honey(Food):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.name = 'Honey'
        self.id = HONEY

    def apply(self, player: Player) -> None:
        """Applies the items effect, if any, to the given player."""
        player.change_hunger(HONEY_AMOUNT)

    def __repr__(self) -> str:
        return f'Honey({self.position})'

class Inventory:
    def __init__(self, initial_items = {}) -> None:
        self.items = {}
        if initial_items:
            for item in initial_items:
                if item.get_name() in self.items:
                    self.items[item.get_name()].append(item)
                else:
                    self.items[item.get_name()] = [item]

    def add_item(self, item) -> None:
        """Adds the given item to the inventory."""
        if item.get_name() in self.items:
            self.items[item.get_name()].append(item)
        else:
            self.items[item.get_name()] = [item]

    def get_items(self):
        return self.items

    def remove_item(self, item_name) -> None:
        """Removes the given item from the inventory."""
        if item_name in self.items:
            item = self.items[item_name].pop(0)
            if len(self.items[item.get_name()]) == 0:
                del self.items[item.get_name()]
            return item
        else:
            return None
    
    def __str__(self) -> str:
        quantity = ''
        for item_name, item in self.items.items():
            quantity += f'{item_name}: {len(item)}\n'

        return quantity.strip('\n')

    def __repr__(self) -> str:
        return f'Inventory(initial_items={[item for list_of_items in self.items.values() for item in list_of_items]})'

class Maze:
    def __init__(self, dimensions: tuple(int, int)) -> None:
        self.dimensions = dimensions
        self.maze = tuple()

    def get_dimensions(self) -> tuple(int, int):
        return self.dimensions

    def add_row(self, row: str) -> None:
        row_list = []
        if len(row) == self.dimensions[1] and len(self.maze) != self.dimensions[0]:

            for char in row:
                r = len(self.maze)
                c = len(row_list)

                if char == WALL:
                    row_list.append(Wall())
                elif char == LAVA:
                    row_list.append(Lava())
                elif char == DOOR:
                    row_list.append(Door())
                elif char == COIN:
                    row_list.append(Coin((r, c)))
                elif char == WATER:
                    row_list.append(Water((r, c)))
                elif char == PLAYER:
                    row_list.append(Player((r, c)))
                elif char == APPLE:
                    row_list.append(Apple((r, c)))
                elif char == HONEY:
                    row_list.append(Honey((r, c)))
                elif char == POTION:
                    row_list.append(Potion((r, c)))
                else:
                    row_list.append(Empty())
            self.maze += (row_list,)

    def get_tiles(self):
        return [[tile if isinstance(tile, Tile) else Empty() for tile in tiles] for tiles in self.maze]

    def unlock_door(self):
        for row in self.maze:
            for tile in row:
                if isinstance(tile, Door):
                    tile.unlock()

    def get_tile(self, position: tuple(int, int)) -> Tile:
        tile = self.maze[position[0]][position[1]]
        return tile if isinstance(tile, Tile) else Empty()

    def __str__(self) -> str:
        maze_str = ''
        for row in self.maze:
            for tile in row:
                if isinstance(tile, Tile):
                    maze_str += tile.get_id()
                else:
                    maze_str += ' '
            maze_str += '\n'
        return maze_str.strip('\n')

    def __repr__(self) -> str:
        return f'Maze({self.dimensions})'

class Level:
    def __init__(self, dimensions: tuple(int, int)) -> None:
        self.maze = Maze(dimensions=dimensions)

    def get_maze(self):
        return self.maze
    
    def attempt_unlock_door(self):
        coins = 0
        for row in self.maze.maze:
            for tile in row:
                if isinstance(tile, Coin):
                    coins += 1
        
        if coins == 0:
            self.maze.unlock_door()

    def add_row(self, row: str) -> None:
        self.maze.add_row(row)

    def add_entity(self, position: tuple(int, int), entity_id: str) -> None:
        if entity_id == COIN:
            entity = Coin(position)
        elif entity_id == APPLE:
            entity = Apple(position)
        elif entity_id == HONEY:
            entity = Honey(position)
        elif entity_id == POTION:
            entity = Potion(position)
        elif entity_id == WATER:
            entity = Water(position)

        maze_list = [list(row) for row in self.maze.maze]
        maze_list[position[0]][position[1]] = entity
        self.maze.maze = tuple(tuple(row) for row in maze_list)

    def get_dimensions(self) -> tuple(int, int):
        return self.maze.get_dimensions()

    def get_items(self) -> dict(tuple(int, int), Item):
        items = {}
        for row in self.maze.maze:
            for tile in row:
                if isinstance(tile, Item) or isinstance(tile, Food):
                    items[tile.get_position()] = tile
        return items

    def remove_item(self, position: tuple(int, int)) -> None:
        maze_list = [list(row) for row in self.maze.maze]
        if isinstance(maze_list[position[0]][position[1]], Item) or isinstance(maze_list[position[0]][position[1]], Food):
            maze_list[position[0]][position[1]] = Empty()
        self.maze.maze = tuple(tuple(row) for row in maze_list)
    
    def add_player_start(self, position: tuple(int, int)) -> None:
        self.maze.add_entity(position, PLAYER)
    
    def get_player_start(self):
        for row in self.maze.maze:
            for tile in row:
                if isinstance(tile, Player):
                    return tile.get_position()
        return None

    def __str__(self) -> str:
        return f"Maze: {self.maze.__str__()}\nItems: {self.get_items()}\nPlayer Start: {self.get_player_start()}"

    def __repr__(self) -> str:
        return f'Level({self.get_dimensions()})'

class Model:
    def __init__(self, game_file: str) -> None:
        self.levels = load_game(game_file)
        self.current_level = self.levels[0]
        self.player = Player(self.current_level.get_player_start())
        self.moves = 0
        self.level_pass = False
        self.game_file = game_file

    def has_won(self) -> bool:
        door = tuple()
        last_level = self.levels[-1].get_maze().maze
        for row in range(len(last_level)):
            for column in range(len(last_level[row])):
                if isinstance(last_level[row][column], Door):
                    door = (row, column)

        if "D" not in str(self.levels[-1]) and self.player.get_position() == door:
            return True
        return False

    def has_lost(self) -> bool:
        if self.player.get_health() <= 0 or self.player.get_hunger() >= 10 or self.player.get_thirst() >= 10:
            return True
        return False

    def get_level(self):
        return self.current_level

    def level_up(self):
        self.level_pass = True
        self.current_level = self.levels[self.levels.index(self.current_level) + 1]

    def did_level_up(self):
        return self.level_pass

    def move_player(self, delta: tuple(int, int)):
        self.level_pass = False
        self.moved = False
        player_position = self.player.get_position()
        next_move = (player_position[0] + delta[0], player_position[1] + delta[1])
        try:
            tile = self.current_level.get_maze().maze[next_move[0]][next_move[1]]
        except IndexError:
            pass

        if isinstance(self.current_level.get_maze().maze[player_position[0]][player_position[1]], Door):
            self.level_up()
            self.player.set_position(self.current_level.get_player_start())
        
        elif isinstance(tile, Door) and str(tile) == " ":
            self.player.change_health(-1)
            self.player.set_position(next_move)
            self.moves+=1
            self.moved = True

        elif isinstance(tile, Lava):
            self.player.change_health(-tile.damage())
            self.player.change_health(-1)
            self.player.set_position(next_move)
            self.moves+=1
            self.moved = True

        elif isinstance(tile, Empty):
            self.player.change_health(-1)
            self.player.set_position(next_move)
            self.moves+=1
            self.moved = True

        elif isinstance(tile, Item):
            self.player.change_health(-1)
            self.attempt_collect_item(next_move)
            self.player.set_position(next_move)
            self.moves+=1
            self.moved = True
        else:
            pass

        if self.moved and self.moves % 5 == 0:
            self.player.change_hunger(1)
            self.player.change_thirst(1)
        self.current_level.attempt_unlock_door()
        self.moved = False
        

    def attempt_collect_item(self, position: tuple(int, int)):
        tile = self.current_level.get_maze().maze[position[0]][position[1]]
        self.player.add_item(tile)
        self.current_level.remove_item(position)
        self.current_level.attempt_unlock_door()

    def get_player(self):
        return self.player

    def get_player_stats(self) -> tuple(int, int):
        return(self.player.get_health(), self.player.get_hunger(), self.player.get_thirst())

    def get_player_inventory(self):
        return self.player.get_inventory()

    def get_current_maze(self):
        return self.current_level.get_maze()

    def get_current_items(self):
        return self.current_level.get_items()

    def __str__(self) -> str:
        return f"Model('{self.game_file}')"

    def __repr__(self) -> str:
        return f"Model('{self.game_file}')"

class MazeRunner:
    def __init__(self, game_file: str, view: UserInterface) -> None:
        self.model = Model(game_file)
        self.view = view


    def play(self):

        while True:
            self.maze = self.model.get_level().get_maze()
            self.items = self.model.get_level().get_items()
            self.player_position = self.model.get_player().get_position()
            self.player = self.model.get_player()
            self.inventory = self.model.get_player_inventory().get_items()
            self.view._draw_level(self.maze, self.items, self.player_position)
            self.view._draw_inventory(self.model.get_player_inventory())
            self.view._draw_player_stats(self.model.get_player_stats())


            user_input = input("Enter a move: ")

            if user_input.startswith('i'):
                user_input = user_input.split()
                if user_input[1] in self.inventory:
                    self.get_item(user_input[1]).apply(self.player)
                else:
                    print(ITEM_UNAVAILABLE_MESSAGE)
        
            elif user_input == UP:
                self.model.move_player(MOVE_DELTAS[UP])
            elif user_input == DOWN:
                self.model.move_player(MOVE_DELTAS[DOWN])
            elif user_input == LEFT:
                self.model.move_player(MOVE_DELTAS[LEFT])
            elif user_input == RIGHT:
                self.model.move_player(MOVE_DELTAS[RIGHT])

            if self.model.has_won():
                self.maze = self.model.get_level().get_maze()
                self.items = self.model.get_level().get_items()
                self.player_position = self.model.get_player().get_position()
                self.view._draw_level(self.maze, self.items, self.player_position)
                self.view._draw_inventory(self.model.get_player_inventory())
                self.view._draw_player_stats(self.model.get_player_stats())
                print(WIN_MESSAGE)
                break
            if self.model.has_lost():
                print(LOSS_MESSAGE)
                break          

    def get_item(self, item_name):
        item = []
        for key, value in self.inventory.items():
            if key == item_name:
                item = value.copy()
                self.model.get_player_inventory().remove_item(key)
                return item[0]

        

def main():
    game_file = input("Enter game file: ")
    maze_runner = MazeRunner(game_file, TextInterface())
    maze_runner.play()

if __name__ == '__main__':
    main()
