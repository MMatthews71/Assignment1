from pokemon import *
from battle_mode import *
import random
from typing import List
from aset import *
from data_structures.stack_adt import *
from data_structures.queue_adt import *
from data_structures.sorted_list_adt import *
from data_structures.array_sorted_list import *

class PokeTeam:
    """
    Represents a team of Pokémon that can be assembled manually or randomly,
    regenerated, and managed for battles.

    Unless stated otherwise, all methods in this class are O(1) best/worst case.
    """
    random.seed(20)  # Set the random seed for reproducibility
    TEAM_LIMIT = 6  # Maximum number of Pokémon allowed in the team
    POKE_LIST = get_all_pokemon_types()  # List of all available Pokémon types

    
    def __init__(self):
        """
        Initializes a new instance of the PokeTeam class.

        Attributes:
            team (ArrayR): An array representing the Pokémon team.
            regen_team (ArrayR): An array representing the regenerated Pokémon team.
            reversed (bool): A flag indicating if the team is reversed for the optimise battle special method.
        """
        self.team = None
        self.regen_team = None
        self.reversed = None


    def choose_manually(self):
        """
        Choose Pokemon manually.

        This method allows the user to manually select Pokemon to form the team.

        Variables:
            length (int): The length of the team.
            choice (str): The name of the chosen Pokemon.
            pokemon_class (class): The class of the chosen Pokemon.

        Returns:
            None

        Complexity Analysis: 
            Best and worst case are O(n), where n is the length of the team.
        """
        # Choose Pokemon manually
        length = PokeTeam.TEAM_LIMIT
        # length = int(input(f"How many pokemon will be in this team? (limit {PokeTeam.TEAM_LIMIT})"))
        # The optional method of choosing the length of the team manually
    
        if length > PokeTeam.TEAM_LIMIT:
            print(f"This exceeds the team limit of {PokeTeam.TEAM_LIMIT}")
            self.choose_manually()
        elif length == '' or length == 0:
            print("There needs to be at least one pokemon in this team")
            self.choose_manually()
        else:
            # Initialize team and regen_team arrays
            self.team = ArrayR(length)
            self.regen_team = ArrayR(length)
            for i in range(length):
                choice = input(f"Enter the name of Pokemon {i + 1}")
                pokemon_class = globals().get(choice)
                if pokemon_class in PokeTeam.POKE_LIST:
                    # Add Pokemon to team and regen_team arrays
                    self.team[i] = pokemon_class()
                    self.regen_team[i] = pokemon_class()
                else:
                    print("That Pokemon does not exist")


    def choose_randomly(self):
        """
        Choose Pokemon randomly.

        This method randomly selects Pokemon to form the team.

        Complexity Analysis: 
            Best and worst case are O(n), where n is the length of the team.
        """
        length = PokeTeam.TEAM_LIMIT
        #length = int(input(f"How many pokemon will be in this team? (limit {PokeTeam.TEAM_LIMIT})"))
        #The optional method of choosing the length of the team manually

        if length > PokeTeam.TEAM_LIMIT:
            print(f"This exceeds the team limit of {PokeTeam.TEAM_LIMIT}")
            self.choose_randomly()
        elif length == '' or length == 0:
            print("There needs to be at least one pokemon in this team")
            self.choose_randomly()
        else:
            self.team = ArrayR(length)
            self.regen_team = ArrayR(length)
            for i in range(length):
                random_pokemon = random.choice(PokeTeam.POKE_LIST)
                self.team[i] = random_pokemon()
                self.regen_team[i] = random_pokemon()

      
    def regenerate_team(self, battle_mode, criterion=None) -> None:
        """
        Regenerates the team of Pokemon based on the given battle mode and criterion.

        Args:
            battle_mode: The mode of battle.
            criterion: The criterion for optimizing the team (optional).

        Returns:
            None

        Complexity Analysis: 
            Best and worst case are O(n*m*k), 
            where:
                - n is the size of the team
                - m is the number of different Pokemon
                - k is the maximum length of the evolution line among all Pokemon types
            The method iterates through each Pokémon in the regen team, resulting in a time complexity proportional to the size of the team.
            Within each iteration, it iterates through each Pokémon in the predefined list of Pokémon (PokeTeam.POKE_LIST). 
            This results in a time complexity proportional to the number of different Pokémon types (m).
            For each Pokémon, it checks if the Pokémon in the regenerated team belongs to its evolution line. 
            If it does, it performs evolution operations, which are constant-time operations.
            The overall complexity also considers the maximum length of the evolution line among all Pokémon types (k), as it affects the number of evolution operations performed for each Pokémon.
        """
        for regen_pokemon in self.regen_team:
            # Iterate through each Pokemon in the regenerated team
            for list_pokemon in PokeTeam.POKE_LIST:
                # Iterate through each Pokemon type
                list_pokemon_class = list_pokemon()
                # Create an instance of the Pokemon type
                if regen_pokemon.name in list_pokemon_class.get_evolution():
                    # Check if the Pokemon is in the evolution line of the current Pokemon type
                    health = list_pokemon_class.health
                    # Store the current health
                    evo_multiplier = list_pokemon_class.get_evolution().index(regen_pokemon.name)
                    # Get the evolution multiplier based on the index of the Pokemon in the evolution line
                    if evo_multiplier == 1:
                        # Check if the Pokemon is at the first evolution stage
                        list_pokemon_class._evolve()
                        # Evolve the Pokemon once
                    if evo_multiplier == 2:
                        # Check if the Pokemon is at the second evolution stage
                        list_pokemon_class._evolve()
                        list_pokemon_class._evolve()
                        # Evolve the Pokemon twice
                    regen_pokemon.health = health
                    # Reset the health to the stored value
        
        self.team = self.regen_team
        # Update the team with the regenerated team
        if battle_mode == BattleMode.SET:
            # Assemble the team in 'SET' mode
            self.assemble_team(BattleMode.SET)
        elif battle_mode == BattleMode.ROTATE:
            # Assemble the team in 'ROTATE' mode
            self.assemble_team(BattleMode.ROTATE)
        elif battle_mode == BattleMode.OPTIMISE:
            # Assemble and optimize the team in 'OPTIMISE' mode
            self.assemble_team(BattleMode.OPTIMISE)
            self.assign_team(criterion)
  
    
    def assemble_team(self, battle_mode):
        """
        Assemble the team based on the specified battle mode.

        Args:
            battle_mode (BattleMode): The mode of battle.

        Returns:
            None

        Variables:
            assembled_team (ArrayStack, CircularQueue, ArraySortedList): The data structure used to assemble the team.

        Complexity Analysis: 
            Best and worst case are O(n), where n is the size of the team.
        """
        assembled_team = None
        
        # Use battle mode value to determine the data structure to be used
        if battle_mode.value == 0:   
            # Use ArrayStack for SET mode
            assembled_team = ArrayStack(self.__len__())
        elif battle_mode.value == 1:
            # Use CircularQueue for ROTATE mode
            assembled_team = CircularQueue(self.__len__())
        elif battle_mode.value == 2:
            # Use ArraySortedList for OPTIMISE mode
            assembled_team = ArraySortedList(self.__len__())
        
        # Iterate over the team and add Pokemon to the assembled_team
        for i in range(self.__len__()):
            if self.team[i] is not None:
                if battle_mode.value == 0:
                    # Add Pokemon to ArrayStack
                    assembled_team.push(self.team[i])
                elif battle_mode.value == 1:
                    # Add Pokemon to CircularQueue
                    assembled_team.append(self.team[i])
                elif battle_mode.value == 2:
                    # Add Pokemon to ArraySortedList
                    assembled_team.add(ListItem(self.team[i], i))
            else:
                break
        
        # Update the team with the assembled_team
        self.team = assembled_team

    
    def assign_team(self, criterion):
        """
        Assigns the team based on the given criterion.

        Args:
            criterion (str): The criterion for optimizing the team.

        Returns:
            None

        Complexity Analysis: 
            Best and worst case are O(n), where n is the size of the team.
        """
        # Initialize an ArraySortedList to store the assigned team
        assigned_team = ArraySortedList(self.__len__())
        # Iterate through the team
        for i in range(self.__len__()):
            # Check if the team member is not None
            if not self.team[i] == None:
                # Add Pokemon to the assigned team based on the given criterion
                if criterion == 'health':
                    assigned_team.add(ListItem(self.team.__getitem__(i).value, self.team.__getitem__(i).value.get_health()))
                elif criterion == 'attack':
                    assigned_team.add(ListItem(self.team.__getitem__(i).value, self.team.__getitem__(i).value.get_attack()))
                elif criterion == 'level':
                    assigned_team.add(ListItem(self.team.__getitem__(i).value, self.team.__getitem__(i).value.get_level()))
                elif criterion == 'defence':
                    assigned_team.add(ListItem(self.team.__getitem__(i).value, self.team.__getitem__(i).value.get_defence()))
                elif criterion == 'speed':
                    assigned_team.add(ListItem(self.team.__getitem__(i).value, self.team.__getitem__(i).value.get_speed()))
        # Update the team with the assigned team
        self.team = assigned_team
      
    
    def special(self, battle_mode):
        """
        Performs a special operation on the team based on the given battle mode.

        Args:
            battle_mode: The mode of battle.

        Returns:
            None

        Complexity Analysis: 
            Best case is O(3), and worst case is O(n), where n is the size of the team.
        """
        if battle_mode.value == 0:
            # Perform special operation for battle mode 0
            temp_stack1 = ArrayStack(self.__len__())
            temp_stack2 = ArrayStack(self.__len__())
            if self.__len__() > 3:
                for i in range(3):
                    temp_stack1.push(self.team.pop())
                for i in range(3):
                    temp_stack2.push(temp_stack1.pop())
                for i in range(3):
                    self.team.push(temp_stack2.pop())
            else:
                for i in range(self.__len__()):
                    temp_stack1.push(self.team.pop())
                for i in range(self.__len__()):
                    temp_stack2.push(temp_stack1.pop())
                for i in range(self.__len__()):
                    self.team.push(temp_stack2.pop())
                    
        if battle_mode.value == 1:
            # Perform special operation for battle mode 1
            temp_stack = ArrayStack(self.__len__())
            length = self.__len__()
            if length > 3:
                for i in range(3):
                    item = self.team.serve()
                    self.team.append(item)
                for i in range(length - 3):
                    item = self.team.serve() 
                    temp_stack.push(item)
                for i in range(length - 3):
                    item = temp_stack.pop()
                    self.team.append(item)
            else:
                pass
            
        if battle_mode.value == 2:
            # Perform special operation for battle mode 2
            length = self.__len__()
            temp_stack1 = ArrayStack(length)
            temp_stack2 = ArrayStack(length)
            temp_sortedlist = ArraySortedList(length)
            for i in range(length):
                temp_stack1.push(self.team[i].value)
                temp_stack2.push((self.team[i].key)*(-1))
            for i in range(length):
                temp_sortedlist.add(ListItem(temp_stack1.pop(), temp_stack2.pop()))
            
            self.team = temp_sortedlist
            
        self.reversed = True
     
   
    def __getitem__(self, index: int):
        """
        Retrieves the item at the specified index from the team.

        Args:
            index (int): The index of the item to retrieve.

        Returns:
            Any: The item at the specified index.

        Variables:
            temp_array (ArrayR): Temporary array to store items.
            temp_stack (ArrayStack): Temporary stack for operations.
            item (Any): Current item being processed.

        Complexity Analysis: 
            Best and worst case are O(n), where n is the size of the team.
        """
        temp_array = ArrayR(self.__len__())

        if isinstance(self.team, ArrayStack):
            # If the team is implemented as an ArrayStack
            temp_stack = ArrayStack(self.__len__())
            for i in range(self.__len__()):
                item = self.team.pop()
                temp_array[i] = item
                temp_stack.push(item)
            for i in range(len(temp_stack)):
                item = temp_stack.pop()
                self.team.push(item)
            return temp_array[index]

        elif isinstance(self.team, CircularQueue):
            # If the team is implemented as a CircularQueue
            for i in range(self.__len__()):
                item = self.team.serve()
                temp_array[i] = item
                self.team.append(item)
            return temp_array[index]

        elif isinstance(self.team, ArraySortedList):
            # If the team is implemented as an ArraySortedList
            return self.team[index].value
            
        elif isinstance(self.team, ArrayR):
            # If the team is implemented as an ArrayR
            return self.team[index]

   
    def __len__(self):
        """
        Returns the length of the team.

        Returns:
            int: The length of the team.
        """
        return len(self.team)

    
    def __str__(self):
        """
        Returns a string representation of the team.

        Returns:
            str: A string representing the team.

        Variables:
            team_str (str): String representation of the team.
            temp_stack (ArrayStack): Temporary stack for operations.
            item (Any): Current item being processed.

        Complexity Analysis: 
            Best and worst case are O(n), where n is the size of the team.
        """
        team_str = ""
        if isinstance(self.team, ArrayStack):
            # If the team is implemented as an ArrayStack
            temp_stack = ArrayStack(self.__len__())
            for i in range(self.__len__()):
                item = self.team.pop()
                team_str += str(item) + "\n"
                temp_stack.push(item)
            for i in range(len(temp_stack)):
                item = temp_stack.pop()
                self.team.push(item)
        
        elif isinstance(self.team, CircularQueue):
            # If the team is implemented as a CircularQueue
            for i in range(self.__len__()):
                item = self.team.serve()
                team_str += str(item) + "\n"
                self.team.append(item)
        elif isinstance(self.team, ArraySortedList):
            # If the team is implemented as an ArraySortedList
            for i in range(self.__len__()):
                team_str += str(self.team[i].value)
        elif isinstance(self.team, ArrayR):
            # If the team is implemented as an ArrayR
            for i in range(self.__len__()):
                team_str += str(self.team[i]) + "\n"
        
        return team_str


class Trainer:
    """
    Represents a Pokemon Trainer who has a team of Pokemon.

    Unless stated otherwise, all methods in this class are O(1) best/worst case.
    """
    def __init__(self, name: str) -> None:
        """
        Initializes a Trainer with a name, a Pokemon team, and a Pokedex.

        Args:
            name (str): The name of the Trainer.
        
        Attributes:
            name (str): The name of the Trainer.
            pokemon_team (PokeTeam): The Trainer's Pokemon team.
            pokedex (ASet): The Trainer's Pokedex containing captured Pokemon types.

        Returns:
            None
        """
        self.name = name
        self.pokemon_team = PokeTeam()
        self.pokedex = ASet(15)

    
    def pick_team(self, method: str) -> None:
        """
        Picks a Pokemon team for the Trainer using the specified method.

        Args:
            method (str): The method for picking the team ("Manual" or "Random").

        Returns:
            None

        Complexity Analysis: 
            Best and worst case are O(n), where n is the size of the team.
        """
        # Iterate through each Pokemon in the team and register them in the Pokedex
        if method == "Manual":
            self.pokemon_team.choose_manually()
        elif method == "Random":
            self.pokemon_team.choose_randomly()
        for i in self.pokemon_team:
            self.register_pokemon(i)

    
    def get_team(self) -> PokeTeam:
        """
        Retrieves the Trainer's Pokemon team.

        Returns:
            PokeTeam: The Trainer's Pokemon team.
        """
        return self.pokemon_team

    
    def get_name(self) -> str:
        """
        Retrieves the name of the Trainer.

        Returns:
            str: The name of the Trainer.
        """
        return self.name

    
    def register_pokemon(self, pokemon: Pokemon) -> None:
        """
        Registers a captured Pokemon in the Trainer's Pokedex.

        Args:
            pokemon (Pokemon): The captured Pokemon.

        Returns:
            None
        """
        self.pokedex.add(pokemon.poketype)

    
    def get_pokedex_completion(self) -> float:
        """
        Calculates the completion percentage of the Trainer's Pokedex.

        Returns:
            float: The completion percentage of the Pokedex.
        """
        return round(float((self.pokedex.__len__()) / 15), 2)

    
    def __str__(self) -> str:
        """
        Returns a string representation of the Trainer.

        Returns:
            str: A string representation of the Trainer.
        """
        return f"Trainer {self.name} Pokedex Completion: {round(self.get_pokedex_completion() * 100)}%"