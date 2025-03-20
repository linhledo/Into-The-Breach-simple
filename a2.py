# DO NOT modify or add any import statements
from a2_support import *
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional, Callable

# Name: Do Thuy Linh Le
# Student Number: 48625610
# ----------------

# Write your classes and functions here

WIN_MESSAGE = 'You Win!'
LOST_MESSAGE = 'You Lost!'

class Tile():
    """Abstract class that all tiles inherit, provides default tile behaviour
    """

    def __init__(self) -> None:
        """Constructor of Tile
        """
        self._repr = f'{TILE_NAME}()'
        self._str = TILE_SYMBOL
        self._is_blocking = False
        self._name = TILE_NAME
        

    def __repr__(self) -> str:
        """Returns machine readable string of instance Tile
        """
        return self._repr

    def __str__(self) -> str:
        """Returns character representating type of the tile
        """
        return self._str

    def get_tile_name(self) -> str:
        """Returns name of type of tile
        """
        return self._name

    def is_blocking(self) -> bool:
        """Returns:
                True if tile is blocking
                False if not
        """
        return self._is_blocking


class Ground(Tile):
    """Represents walkable ground
    """

    def __init__(self) -> None:
        self._repr = f'{GROUND_NAME}()'
        self._str = GROUND_SYMBOL
        self._is_blocking = False
        self._name = GROUND_NAME
    

class Mountain(Tile):
    """Represents unpassable terrain
    """
    
    def __init__(self) -> None:
        self._repr = f'{MOUNTAIN_NAME}()'
        self._str = MOUNTAIN_SYMBOL
        self._is_blocking = True
        self._name = MOUNTAIN_NAME


class Building(Tile):
    """Buildings that the player must protect from enemies
    """

    def __init__(self, initial_health: int) -> None:
        """
        Parameters:
                initial_health = default health of the Building instance

        Precondition:
            0 > initial_health >= MAX_BUILDING_HEALTH
        """
        self._health = initial_health
        self._name = BUILDING_NAME
        
    def __str__(self) -> str:
        return f'{self._health}'

    def __repr__(self) -> str:
        return f'{BUILDING_NAME}({self._health})'

    def is_blocking(self) -> bool:
        """Returns:
                True if building is blocking (still has health)
                False if not
        """
        return self._health != 0

    def is_destroyed(self) -> bool:
        """Returns:
                True if building is destroyed (health drops to 0)
                False if not
        """

        return self._health == 0

    def damage(self, damage: int) -> None:
        """Reduces health of building by amount (damage) specified
        """
        
        if self._health != 0: #does not operate if building is already destroyed
            self._health -= damage

            # keeping building health between 0 and MAX_BUILDING_HEALTH
            if self._health < 0:
                self._health = 0
            elif self._health > MAX_BUILDING_HEALTH:
                self._health = MAX_BUILDING_HEALTH


class Board():
    """Represents a structured set of tiles in a rectangular grid where each
    tile has an associated (row, column) position
    """

    def __init__(self, board: list[list[str]]) -> None:
        """Constructor of the board on which the game is played on

        Parameters:
                board = representation of the board state

        Preconditions:
                - Each list in board will have the same length
                - board contains at least 1 list
                - Each character is the str representation of one of the tile
                  subclasses
        """
        self._board = []

        for row in board:
            row_list = []

            for tile in row:
                if tile == MOUNTAIN_SYMBOL:
                    row_list.append(Mountain())
                elif tile == GROUND_SYMBOL:
                    row_list.append(Ground())
                else:
                    row_list.append(Building(int(tile)))

            self._board.append(row_list)

    def __repr__(self) -> str:
        return f'Board({[[str(tile) for tile in row] for row in self._board]})'

    def __str__(self) -> str:
        rows = []

        for list in [[str(tile) for tile in row] for row in self._board]:
            rows.append(''.join(list))

        return '\n'.join(rows)

    def get_dimensions(self) -> tuple[int, int]:
        """Returns amount of rows and column in the board in the form
        (rows, columns)
        """
        return (len(self._board), len(self._board[0]))

    def get_tile(self, position: tuple[int, int]) -> Tile:
        """Returns Tile instance at given position

        Preconditions:
                (0,0) <= position < self.get_dimensions()
        """
        
        return self._board[position[0]][position[1]]

    def get_buildings(self) -> dict[tuple[int, int], Building]:
        """Returns all buildings on the board as a dictionary

        Key = location (row, column)
        Value = instance of Building   
        """

        result = {}

        for row_number, row in enumerate(self._board):
            for column_number, tile in enumerate(row):
                if tile.get_tile_name() == BUILDING_NAME:
                    result[(row_number, column_number)] = tile

        return result


class Entity():
    """Abstract class that all types of entities inherit. Provides default
    entity behaviour
    """

    def __init__(self, position: tuple[int, int], initial_health: int,
                 speed: int, strength: int) -> None:
        """Constructor of the Entity object

        Parameters:
                position = initial position of the entity on the board
                initial_health = initial health of entity
                speed = speed of entity (what distance it can travel)
                strength = strength of entity (how much damage it deals)
        """

        self._position = position
        self._health = initial_health
        self._speed = speed
        self._strength = strength
        self._symbol = ENTITY_SYMBOL
        self._friendly = False
        self._name = ENTITY_NAME

    def __repr__(self) -> str:
        return f'{self.get_name()}({self._position}, {self._health}, {self._speed}, \
{self._strength})'

    def __str__(self) -> str:
        return f'{self._symbol},{self._position[0]},{self._position[1]},\
{self._health},{self._speed},{self._strength}'

    def get_symbol(self) -> str:
        """Return character that represents the entity type
        """
        return self._symbol

    def get_name(self) -> str:
        """Returns name of the type of entity
        """
        return self._name

    def get_position(self) -> tuple[int, int]:
        """Returns the current position (row, column) of the entity
        """
        return self._position

    def set_position(self, position: tuple[int, int]) -> None:
        """Moves the entity to the specified position
        """
        self._position = position

    def get_health(self) -> int:
        """Returns the current health of the entity
        """
        return self._health

    def get_speed(self) -> int:
        """Returns the speed of the entity
        """
        return self._speed

    def get_strength(self) -> int:
        """Returns the strength of the entity
        """
        return self._strength

    def damage(self, damage: int) -> None:
        """Reduces the health of the entity by amount specified
        """
        if self._health != 0:
            self._health -= damage

            if self._health < 0:
                self._health = 0

    def is_alive(self) -> bool:
        """Return:
                True if entity is not destroyed
                False if it is
        """
        return self._health != 0

    def is_friendly(self) -> bool:
        """Returns:
                True if entity can be controlled by the player
                False if entity is working against the player
        """

        return self._friendly

    def get_targets(self) -> list[tuple[int, int]]:
        """Returns all positions that entity could attack during combat phase
        """

        current_row, current_column = self.get_position()

        return [(current_row + 1, current_column),
                (current_row -1, current_column),
                (current_row, current_column + 1),
                (current_row, current_column - 1)]

    def attack(self, entity: "Entity") -> None:
        """Apply the entity's effects (heal or damage)

        Parameters:
                entity = secondary entity that receives the effects
        """
        entity.damage(self.get_strength())


class Mech(Entity):
    """Abstract class that all mechs inherit. Mechs are friendly entities that
    the player can control
    """

    
    def __init__(self, position: tuple[int, int], initial_health: int,
                 speed: int, strength: int) -> None:
        super().__init__(position, initial_health, speed, strength)
        
        self._symbol = MECH_SYMBOL
        self._friendly = True
        self._active = True
        self._name = MECH_NAME
        
    def enable(self) -> None:
        """Activates the mech
        """
        self._active = True

    def disable(self) -> None:
        """Deactivates the mech
        """
        self._active = False

    def is_active(self) -> bool:
        """Returns:
                True if mech is active
                False if not
        """
        return self._active

    def set_position(self, position: tuple[int, int]) -> None:
        """Sets location of the mech to specified position
        """
        self._position = position
        

class TankMech(Mech):
    """A type of mech that attacks all entities and buildings
    """

    def __init__(self, position: tuple[int, int], initial_health: int,
                 speed: int, strength: int) -> None:
        super().__init__(position, initial_health, speed, strength)
        
        self._symbol = TANK_SYMBOL
        self._name = TANK_NAME

    def get_targets(self) -> list[tuple[int, int]]:

        total = []
        current_row, current_column = self.get_position()

        for column in range(1, TANK_RANGE + 1): #range does not include last int
            total.extend([(current_row, current_column + column),
                         (current_row, current_column - column)])

        return total


class HealMech(Mech):
    """Mech that heals friendly units and buildings
    """

    def __init__(self, position: tuple[int, int], initial_health: int,
                 speed: int, strength: int) -> None:
        super().__init__(position, initial_health, speed, strength)
        
        self._symbol = HEAL_SYMBOL
        self._strength = strength
        self._name = HEAL_NAME

    def get_strength(self) -> int:
        """Returns the negative of its strength 
        """
        return -self._strength

    def attack(self, entity: Entity) -> None:
        """Deals negative damage which equates to healing, and only 'attacks'
        friendly entities or buildings
        """
        if entity.is_friendly():
            entity.damage(self.get_strength())

class Enemy(Entity):
    """Abstract class that all types of enemies inherit. Enemies are not
    friendly and work against the player 
    """

    def __init__(self, position: tuple[int, int], initial_health: int,
                 speed: int, strength: int):
        super().__init__(position, initial_health, speed, strength)
        
        self._symbol = ENEMY_SYMBOL
        self._objective = position
        self._name = ENEMY_NAME

    def get_objective(self) -> tuple[int, int]:
        """Returns location (row, column) of the current objective of the enemy 
        """
        return self._objective

    def update_objective(self, entities: list[Entity],
                         buildings: dict[tuple[int, int], Building]) -> None:

        """Updates the location of the objective of the enemy

        Parameters:
                entities = list of entities on the current board
                buildings = dictionary of buildings on the current board with
                key: location (row, column) and value: Building instance

        Precondition:
                entities is sorted in descending priority e.g. the first
                entity in the list has highest priority 
        """
        self._objective = self.get_position()


class Scorpion(Enemy):
    """Represents a type of enemy that attacks all entities and buildings, but
    targets mechs with the highest health
    """

    def __init__(self, position: tuple[int, int], initial_health: int,
                 speed: int, strength: int):
        super().__init__(position, initial_health, speed, strength)
        
        self._symbol = SCORPION_SYMBOL
        self._name = SCORPION_NAME

    def get_targets(self) -> list[tuple[int, int]]:

        total = []
        current_row, current_column = self.get_position()

        for tile in range(1, SCORPION_RANGE + 1):
            total.extend([(current_row, current_column - tile),
                          (current_row, current_column + tile),
                          (current_row - tile, current_column),
                          (current_row + tile, current_column)])

        return total

    def update_objective(self, entities: list[Entity],
                         buildings: dict[tuple[int, int], Building]) -> None:
        health = 0

        for entity in entities:
            if entity.get_health() > health and entity.is_friendly():
                self._objective = entity.get_position()
                health = entity.get_health()


class Firefly(Enemy):
    """Represents a type of enemy that attacks all entities and buildings, but
    targets buildings with the lowest health
    """
    
    def __init__(self, position: tuple[int, int], initial_health: int,
                 speed: int, strength: int):
        super().__init__(position, initial_health, speed, strength)
        
        self._symbol = FIREFLY_SYMBOL
        self._name = FIREFLY_NAME

    
    def get_targets(self) -> list[tuple[int, int]]:

        total = []
        current_row, current_column = self.get_position()

        for row in range(1, FIREFLY_RANGE + 1):
            total.extend([(current_row + row, current_column),
                          (current_row - row, current_column)])

        return total

    def update_objective(self, entities: list[Entity],
                         buildings: dict[tuple[int, int], Building]) -> None:

        # initial values to be overriden
        health = 10
        row = -1
        column = -1

        for location in buildings:
            building_health = int(str(buildings.get(location)))

            if building_health != 0 and building_health < health:
                health = building_health
                self._objective = location

            elif building_health != 0 and building_health == health:

                # prioritising buildings on lower rows for ties in health
                if location[0] > row:                    
                    self._objective = location
                    row = location[0]

                # prioritising buildings on rightmost columns
                elif location[0] == row and location[1] > column:
                    self._objective = location
                    column = location[1]
                    
                
class BreachModel():
    """Models the logical state of a game of Into The Breach
    """

    def __init__(self, board: Board, entities: list[Entity]) -> None:
        """Instantiates a new model class

        Precondition:
                entities is in descending priority order

        Parameters:
                board = Board object
                entities = all initial entities on the board
        """

        self._board = board
        self._entities = entities
        
    def __str__(self):

        total = ''

        for entity in self._entities:
            total += f'\n{str(entity)}'
        
        return f'{str(self.get_board())}\n{total}'

    def get_board(self) -> Board:
        """Returns board instance
        """
        return self._board

    def get_entities(self) -> list[Entity]:
        """Returns list of entities on the current board
        """
        return self._entities

    def has_won(self) -> bool:
        """Returns:
                True if game is in a win state (all enemies destroyed and at
                least one mech and one building not destroyed)

                False if not
        """

        buildings = (self._board).get_buildings()
        alive_building = False
        alive_mech = False
        all_enemies_destroyed = True #False if at least 1 enemy still has health

        for key in buildings:
            if not buildings.get(key).is_destroyed():
                alive_building = True

        for entity in self._entities:
            if entity.get_health() > 0 and entity.is_friendly():
                alive_mech = True

            elif entity.get_health() > 0 and not entity.is_friendly():
            # checking if at least 1 enemy has health > 0
                
                all_enemies_destroyed = False

        return alive_building and alive_mech and all_enemies_destroyed

    def has_lost(self) -> bool:
        """Returns:
                True if game is in a loss state (all buildings are destroyed
                or all mechs are destroyed)

                False if not
        """

        buildings = (self._board).get_buildings()
        buildings_destroyed = True 
        mechs_destroyed = True

        for key in buildings:
            if not buildings.get(key).is_destroyed():
            # checking if at least 1 building has health > 0

                buildings_destroyed = False

        for entity in self._entities:
            if entity.get_health() > 0 and entity.is_friendly():
            # checking if at least 1 mech has health > 0

                mechs_destroyed = False

        return buildings_destroyed or mechs_destroyed

    def entity_positions(self) -> dict[tuple[int, int], Entity]:
        """Returns dictionary of all entities on the board

        Key: Entity position (row, column)
        Value: instance of Entity
        """
        
        result = {}

        for entity in self._entities:
            result[entity.get_position()] = entity

        return result

    def get_valid_movement_positions(self,
                                     entity: Entity) -> list[tuple[int,int]]:
        """Returns positions entity could move to during movement phase
        """

        speed = entity.get_speed()
        position = entity.get_position()
        valid_movements = []
        no_of_rows, no_of_columns = (self._board).get_dimensions()

        # checking for empty tiles that is traversable with entity's speed
        for row_number in range(no_of_rows):
            for column_number in range(no_of_columns):
                if 0 < get_distance(self, position,
                                    (row_number, column_number)) <= speed:
                
                    valid_movements.append((row_number, column_number))

        buildings = (self._board).get_buildings()

        # checking for traversable non-blocking buildings
        for location in buildings:
            if not buildings.get(location).is_blocking() and \
               0 < get_distance(self, position, location) <= speed:
        
                valid_movements.append(location)

        return valid_movements

    def attempt_move(self, entity: Entity, position: tuple[int, int]) -> None:
        """Moves entity to the specified position if it is friendly, active,
        and position is valid
        """

        valid_movements = self.get_valid_movement_positions(entity)

        if entity.is_friendly() and entity.is_active \
           and position in valid_movements:

            entity.set_position(position)
            entity.disable()

    def ready_to_save(self) -> bool:
        """Returns:
                True if no move has been made since the last call to end turn
                (all mechs are activated)
                False if there has (one or more mech is disabled)
        """

        all_mechs_active = True

        for entity in self._entities:
            if entity.is_friendly() and not entity.is_active():
                all_mechs_active = False

        return all_mechs_active

    def assign_objectives(self) -> None:
        """Updates objectives of all enemies based on current game state
        """

        buildings = (self._board).get_buildings()

        for entity in self._entities:
            if not entity.is_friendly():
                entity.update_objective(self._entities, buildings)


    def move_enemies(self) -> None:
        """Moves each enemy to position of shortest distance between itself and
        its objective 
        """

        for entity in self._entities:
            if not entity.is_friendly():
                    
                current_distance = 200 #initial number that is definitely bigger
                                       #than the first location distance
                row = -1
                column = -1
                objective_location = entity.get_objective()
                valid_movements = self.get_valid_movement_positions(entity)

                for position in valid_movements:
                    distance = get_distance(self, objective_location, position)
                    
                    if 0 < distance < current_distance:
                        entity.set_position(position)
                        current_distance = distance

                    elif distance == current_distance:
                        if position[0] > row:
                            entity.set_position(position)
                            row = position[0]

                        elif position[0] == row and position[1] > column:
                            entity.set_position(position)
                            column = position[1]

    def make_attack(self, entity: Entity) -> None:
        """Makes the entity attack every tile that currently is its target
        """

        buildings = (self._board).get_buildings()
        entities = self.entity_positions()
        strength = entity.get_strength()

        for target in entity.get_targets():
            if target in buildings:
                building = buildings.get(target)
                building.damage(strength)

            elif target in entities:
                target_entity = entities.get(target)
                target_entity.damage(strength)

    def end_turn(self) -> None:
        """Executes the attack and enemy movement phases, then sets all mechs
        to be active
        """

        for entity in self._entities:
            if entity.is_alive():
                self.make_attack(entity)

                if entity.is_friendly():
                    entity.enable()
                    
        # filtering entities that were killed by a lower priority entity
        updated_entities = []
        updated_entities = [entity for entity in self._entities if \
                            entity.is_alive()]
        self._entities = updated_entities
        
        self.assign_objectives()
        self.move_enemies()


class GameGrid(AbstractGrid):
    """View component of the game board displaying Tiles and Entities
    """

    def __init__(self, master: tk.Tk, dimensions: tuple[int, int], size:
                 tuple[int, int]):
        """Constructor of GameGrid

        Parameters:
                master = window where the widget lies in
                dimensions = the amount of cells in the form
                             (rows, columns)
                size = pixel size of the widget in the form (width, height)

        """       
        super().__init__(master, dimensions, size)
        self._dimensions = dimensions

    def redraw(self, board: Board, entities: list[Entity],
               highlighted: list[tuple[int, int]] = None,
               movement: bool = False) -> None:
        """Clears the game grid, then reconstructs the view with information
        from provided parameters

        Parameters:
                board = Board object
                entities = list of entities on the current board state
                highlighted = (Optional) tiles that are highlighted to indicate
                              possible movement or possible attacks
                movement = True if entity is currently in its movement phase,
                           False if it is in its attacking phase
        """
        
        self.clear()
        rows, columns = self._dimensions
        buildings = board.get_buildings()

        for row in range(rows):
            for column in range(columns):
                
                # highlighting movement or attacking tiles
                if highlighted is not None and (row, column) in highlighted:
                    if movement:
                        self.color_cell((row, column), MOVE_COLOR)
                    else:
                        self.color_cell((row, column), ATTACK_COLOR)
                        
                # colouring mountain, ground or building tiles
                else:
                    if board.get_tile((row, column)).get_tile_name() \
                       == MOUNTAIN_NAME:
                        self.color_cell((row, column), MOUNTAIN_COLOR)

                    elif board.get_tile((row, column)).get_tile_name() \
                         == GROUND_NAME:
                        self.color_cell((row, column), GROUND_COLOR)

                    else:
                        if board.get_tile((row, column)).is_destroyed():
                            self.color_cell((row, column), DESTROYED_COLOR)
                        else:
                            self.color_cell((row, column), BUILDING_COLOR)

        # annotating building health
        for location in buildings:
            if not buildings.get(location).is_destroyed():
                self.annotate_position(location, str(buildings.get(location)),
                                       ENTITY_FONT)

        # annotating entity symbol
        for entity in entities:
            if entity.get_name() == TANK_NAME:
                self.annotate_position(entity.get_position(), TANK_DISPLAY,
                                       ENTITY_FONT)
            elif entity.get_name() == HEAL_NAME:
                self.annotate_position(entity.get_position(), HEAL_DISPLAY,
                                       ENTITY_FONT)
            elif entity.get_name() == SCORPION_NAME:
                self.annotate_position(entity.get_position(), SCORPION_DISPLAY,
                                       ENTITY_FONT)
            else:
                self.annotate_position(entity.get_position(), FIREFLY_DISPLAY,
                                       ENTITY_FONT)

    def bind_click_callback(self,
                            click_callback: Callable[[tuple[int, int]],
                                                         None]) -> None:
        """Binds Button-1 (left click) and Button-2 (middle click) events on
        itself to the function click_callback
        """
        
        self.bind('<Button-1>', lambda event: click_callback(
            self.pixel_to_cell(event.x, event.y)))
        
        self.bind('<Button-2>', lambda event: click_callback(
            self.pixel_to_cell(event.x, event.y)))


class SideBar(AbstractGrid):
    """View component that displays properties of each entity
    """

    def __init__(self, master: tk.Widget, dimensions: tuple[int, int],
                 size: tuple[int, int]) -> None:
        super().__init__(master, dimensions, size)
    
    def display(self, entities: list[Entity]) -> None:
        """Clears the side bar, then redraws the sidebar headings along with the
        with the properties of each entity in the list entities

        Preconditions:
                entities is sorted in descending priority order
        """
        self.clear()
        self.set_dimensions((len(entities) + 1,#+1 accounts for sidebar headings
                             len(SIDEBAR_HEADINGS)))

        for column, heading in enumerate(SIDEBAR_HEADINGS):
            self.annotate_position((0, column), heading, SIDEBAR_FONT)

        for index, entity in enumerate(entities):
            if entity.get_name() == TANK_NAME:
                display = TANK_DISPLAY
            elif entity.get_name() == HEAL_NAME:
                display = HEAL_DISPLAY
            elif entity.get_name() == SCORPION_NAME:
                display = SCORPION_DISPLAY
            else:
                display = FIREFLY_DISPLAY
            
            self.annotate_position((index + 1, 0), display, ENTITY_FONT)
            self.annotate_position((index + 1, 1), f'{entity.get_position()}')
            self.annotate_position((index + 1, 2), f'{entity.get_health()}')
            self.annotate_position((index + 1, 3), f'{entity.get_strength()}')
        

class ControlBar(tk.Frame):
    """View component containing a save, load and end turn button to allow the
    user to perform administration actions
    """

    def __init__(self, master: tk.Widget,
                 save_callback: Optional[Callable[[], None]] = None,
                 load_callback: Optional[Callable[[], None]] = None,
                 turn_callback: Optional[Callable[[], None]] = None,
                 **kwargs) -> None:
        """Constructor of ControlBar

        Parameters:
                master = window the frame lies in
                save_callback = function that is called when user clicks the
                                save game button
                load_callback = function called for load game button
                turn_callback = function called for end turn button
        """
        super().__init__(master, **kwargs)

        save = tk.Button(self, text = SAVE_TEXT, command = save_callback)
        save.pack(expand = tk.TRUE, side = tk.LEFT)

        load = tk.Button(self, text = LOAD_TEXT, command = load_callback)
        load.pack(expand = tk.TRUE, side = tk.LEFT)

        end_turn = tk.Button(self, text = TURN_TEXT, command = turn_callback)
        end_turn.pack(expand = tk.TRUE, side = tk.LEFT)


class BreachView():
    """Combines GameGrid, SideBar and ControlBar into a single view interface
    """

    def __init__(self, root: tk.Tk, board_dims: tuple[int, int],
                 save_callback: Optional[Callable[[], None]] = None,
                 load_callback: Optional[Callable[[], None]] = None,
                 turn_callback: Optional[Callable[[], None]] = None) -> None:
        """Constructor for BreachView

        Parameters:
                root = window that widgets lie in
                board_dims = dimensions of the board (GameGrid)
                save_callback = function called for save game button
                load_callback = function called for load game button
                turn_callback = function called for end turn button
        """

        root.title(BANNER_TEXT)

        self._banner = tk.Label(root, text = BANNER_TEXT, font = BANNER_FONT)
        self._banner.pack()

        self._game_and_side = tk.Frame(root)
        self._game_and_side.pack()

        self._game = GameGrid(self._game_and_side, board_dims,
                              (GRID_SIZE, GRID_SIZE))
        self._game.pack(side=tk.LEFT)

        self._side = SideBar(self._game_and_side,
                             (0,0), # default sidebar dimensions
                             (SIDEBAR_WIDTH, GRID_SIZE))
        self._side.pack(side=tk.LEFT)

        self._control_bar = ControlBar(root, save_callback, load_callback,
                                 turn_callback)
        self._control_bar.pack(expand = tk.TRUE, fill = tk.X)

    def get_components(self) -> list[tk.Label, GameGrid, SideBar, ControlBar,
                                     tk.Frame]:
        """Returns all the widgets on the window 
        """
        return [self._banner, self._game, self._side, self._control_bar,
                self._game_and_side]
        

    def bind_click_callback(self,
                            click_callback: Callable[[tuple[int, int]], None]
                            ) -> None:
        """Binds click event handler to instantiated GameGrid based on function
        click_callback
        """

        self._game.bind_click_callback(click_callback)

    def redraw(self, board: Board, entities: list[Entity],
               highlighted: list[tuple[int, int]] = None,
               movement: bool = False) -> None:
        """Redraws the instantiated GameGrid and SideBar based on the given
        board, list of entities, and tile highlight information
        """

        self._game.redraw(board, entities, highlighted, movement)
        self._side.display(entities)


class IntoTheBreach():
    """Controller class for the overall game
    """

    def __init__(self, root: tk.Tk, game_file: str) -> None:
        """Constructor for IntoTheBreach

        Parameters:
                root = window that all widgets lie in
                game_file = file that contains the string representations of
                            the board and entities
        """
        
        board = []
        entities = []

        with open(game_file, 'r') as level:
            data = level.readlines()
            for index, string in enumerate(data):
                if string == '\n':
                    
                    # implementing board
                    board = [[tile for tile in string.removesuffix('\n')] \
                             for string in data[:index]]

                    # implementing entities
                    for entity in data[index + 1:]:
                        entity = entity.strip().split(',')
                        location = (int(entity[1]), int(entity[2]))
                        health = int(entity[3])
                        speed = int(entity[4])
                        strength = int(entity[5])

                        if entity[0] == TANK_SYMBOL:
                            entities.append(
                                TankMech(location, health, speed, strength))
                            
                        elif entity[0] == HEAL_SYMBOL:
                            entities.append(
                                HealMech(location, health, speed, strength))
                                                  
                        elif entity[0] == FIREFLY_SYMBOL:
                            entities.append(
                                Firefly(location, health, speed, strength))

                        else:
                            entities.append(
                                Scorpion(location, health, speed, strength))
        
        game_board = Board(board)
        self._model = BreachModel(game_board, entities)
        dimensions = game_board.get_dimensions()

        self._view = BreachView(root, dimensions, self._save_game,
                                self._load_game, self._end_turn)
        self._view.redraw(game_board, entities)
        self._view.bind_click_callback(self._handle_click)

        self._focussed_entity = None
        self._root = root
        self._game_file = game_file

    def redraw(self) -> None:
        """Redraws the view based on the state of BreachModel and the current
        focussed entity
        """

        board = self._model.get_board()
        entities = self._model.get_entities()
        
        # highlighting movement tiles
        if self._focussed_entity is not None and \
           self._focussed_entity.is_friendly() and \
           self._focussed_entity.is_active():
            
            self._view.redraw(board, entities,
                              self._model.get_valid_movement_positions(
                                  self._focussed_entity), True)

        # highlighting attacking tiles
        elif self._focussed_entity is not None:
            self._view.redraw(board, entities,
                              self._focussed_entity.get_targets())

        # no highlights
        else:
            self._view.redraw(board, entities)

    def set_focussed_entity(self, entity: Optional[Entity] = None) -> None:
        """Sets entity as focussed entity. If none is given, sets focussed
        entity to None
        """

        if entity is not None:
            self._focussed_entity = entity
        else:
            self._focussed_entity = None

    def make_move(self, position: tuple[int, int]) -> None:
        """Attempts to move the focussed entity, then sets focussed
        entity as None

        Parameters:
                position = (row, column) where the focussed entity is moved to
        """

        self._model.attempt_move(self._focussed_entity, position)       
        self.set_focussed_entity()

    def load_model(self, file_path: str) -> None:
        """Replaces game state with a new state based on file_path

        Parameters:
                file_path = file containing representation of the new game state 

        Precondition:
                If file_path opens, then it will contain exactly the string
                representation of BreachModel
        """

        if not file_path:
            return # no error displayed if user presses 'cancel'

        try:
            self._game_file = file_path
            board = []
            entities = []

            with open(file_path, 'r') as level:
                data = level.readlines()
                for index, string in enumerate(data):
                    if string == '\n':

                        board = [[tile for tile in string.removesuffix('\n')] \
                                 for string in data[:index]]

                        for entity in data[index + 1:]:
                            entity = entity.strip().split(',')
                            location = (int(entity[1]), int(entity[2]))
                            health = int(entity[3])
                            speed = int(entity[4])
                            strength = int(entity[5])

                            if entity[0] == TANK_SYMBOL:
                                entities.append(
                                    TankMech(location, health, speed, strength))
                                
                            elif entity[0] == HEAL_SYMBOL:
                                entities.append(
                                    HealMech(location, health, speed, strength))
                                                      
                            elif entity[0] == FIREFLY_SYMBOL:
                                entities.append(
                                    Firefly(location, health, speed, strength))

                            else:
                                entities.append(
                                    Scorpion(location, health, speed, strength))

            for component in self._view.get_components():
                component.destroy()

            game_board = Board(board)
            dimensions = game_board.get_dimensions()
            
            self._model = BreachModel(game_board, entities)
            self._view = BreachView(self._root, dimensions, self._save_game,
                                self._load_game, self._end_turn)
            self._view.bind_click_callback(self._handle_click)

            self.redraw()

        except Exception as error:
            tk.messagebox.showerror(message = f'{IO_ERROR_MESSAGE} {error}',
                                    title = IO_ERROR_TITLE)
    def _save_game(self) -> None:
        """Saves current game state to a specified file
        """

        if self._model.ready_to_save():
            save_name = filedialog.asksaveasfilename()
            with open(save_name, 'w') as save_file:  
                save_file.write(str(self._model))

                
        else:
            tk.messagebox.showerror(message = INVALID_SAVE_MESSAGE,
                                    title = INVALID_SAVE_TITLE)
            

    def _load_game(self) -> None:
        """Loads in a new game state based on the specified file 
        """
        self.load_model(filedialog.askopenfilename())

    def _end_turn(self) -> None:
        """Executes attack phase, enemy movement phase and termination checking
        """
        
        self._model.end_turn()
        self.set_focussed_entity() # highlights disappear when end turn is
                                                                     # pressed
        self.redraw()
        answer = ''
        
        if self._model.has_won():
            answer = tk.messagebox.askquestion(
                message = f'{WIN_MESSAGE} {PLAY_AGAIN_TEXT}',
                title = WIN_MESSAGE)

        elif self._model.has_lost():
            answer = tk.messagebox.askquestion(
                message = f'{LOST_MESSAGE} {PLAY_AGAIN_TEXT}',
                                      title = LOST_MESSAGE)

        # restarts game if user decides to play again
        if answer == 'yes':
            self.load_model(self._game_file)
                        
        elif answer == 'no':
            self._root.destroy()

    def _handle_click(self, position: tuple[int, int]) -> None:
        """Handler for a click from the user according to game rules

        Parameters:
                position = (row, column) tile where user has clicked
        """

        entity_positions = self._model.entity_positions()

        # tile containing mech that has not moved
        if position in entity_positions and \
           entity_positions.get(position).is_friendly() and \
           entity_positions.get(position).is_active():

            self.set_focussed_entity(entity_positions.get(position))

        # higlighted tile for movement
        elif self._focussed_entity is not None and \
             self._focussed_entity.is_friendly() and \
             self._focussed_entity.is_active() and position in \
             self._model.get_valid_movement_positions(self._focussed_entity):

            self.make_move(position)
            
        # highlighting attacking tiles
        elif position in entity_positions:
            self.set_focussed_entity(entity_positions.get(position))

        # removing highlights when user clicks on non-valid tile
        else:
            self.set_focussed_entity()

        self.redraw()
        
 
def main() -> None:
    """The main function"""
    
    root = tk.Tk()
    play_game(root, 'levels/level3.txt')

def play_game(root: tk.Tk, file_path: str) -> None:
    """Constructs the controller instance using file_path and root

    Parameters:
            root = window that all widgets of the game instance lie in
            file_path = file containing representation of the game state
    """

    game = IntoTheBreach(root, file_path)
    root.mainloop()

if __name__ == "__main__":
    main()

