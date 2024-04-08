from poke_team import Trainer, PokeTeam
from battle import *
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from typing import Tuple
import random


class BattleTower:
    """
    Manages a tower-like structure where the player engages in battles with a series of enemy trainers.
    
    Unless stated otherwise, all methods in this class are O(1) best/worst case.
    """
    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self) -> None:
        """
        Initialize a BattleTower instance.

        Args:
            None

        Returns:
            None

        Variables:
            player_trainer (Trainer): The player's trainer instance.
            enemy_trainers (None): Queue of enemy trainers.
            defeated_counter (int): Counter to track the number of defeated enemy trainers.
        """
        self.player_trainer = Trainer('default name')  # Initialize player's trainer
        self.enemy_trainers = None  # Initialize enemy trainers
        self.defeated_counter = 0  # Initialize counter for defeated enemy trainers

        # Seed the random number generator
        random.seed(20)

        
    def set_my_trainer(self, trainer) -> None:
        """
        Set the player's trainer and assign a random number of lives to it.

        Args:
            trainer (Trainer): The trainer to set.

        Returns:
            None

        Variables:
            num_lives (int): Randomly generated number of lives for the trainer.
        """
        num_lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)  # Generate a random number of lives
        self.player_trainer = (trainer, num_lives)  # Assign the trainer and number of lives


    def generate_enemy_trainers(self, amount) -> None:
        """
        Generates enemy trainers with random teams and assigns them a random number of lives.
        
        Complexity Analysis: 
            Best and worst are O(n), where n is the amount of trainers specified by the user.
 
        Args:
            Amount (int): The number of enemy trainers to generate.
        
        Returns:
            None
        """
        # Create a temporary stack to hold generated enemy trainers
        temp_stack = ArrayStack(amount)  

        # Generate enemy trainers with random teams and assign them a random number of lives
        for i in range(amount):
            # Create a new instance of the Trainer class for each enemy trainer
            new_trainer = Trainer(f"Enemy number {i}")  
            # Pick a random team for the new trainer
            new_trainer.pick_team("Random")  
            # Assemble the team using rotate battle mode
            new_trainer.get_team().assemble_team(BattleMode.ROTATE)  
            # Generate a random number of lives for the trainer
            num_lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)  

            # Create a tuple containing the new_trainer and num_lives for each enemy trainer
            new_enemy = (new_trainer, num_lives)  
            # Push the new_enemy tuple onto the temporary stack
            temp_stack.push(new_enemy)  

        # Pop enemy trainers from the temporary stack and append them to the enemy_trainers CircularQueue
        for i in range(amount):
            self.enemy_trainers.append(temp_stack.pop())  


    def battles_remaining(self) -> bool:
        """
        Checks if there are battles remaining based on the number of lives of the player trainer
        and the number of enemy trainers left.

        Returns:
            bool: True if battles are remaining, False otherwise.
        """
        # Check if the player trainer has lives remaining and if there are any enemy trainers left
        if self.player_trainer[1] > 0 and self.enemy_trainers.__len__() > 0:
            return True
        else:
            return False


    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        """
        Proceeds to the next battle, simulating a battle between the player trainer and an enemy trainer.

        Best Case:
        The best case occurs when one of the teams runs out of Pokémon before the battle starts.
        In this case, the loop will terminate early, resulting in fewer iterations.
        Complexity: O(1) - constant time.
        
        Worst Case:
        The worst case happens when both teams have an equal number of Pokémon, and the battle continues until one team loses all its Pokémon.
        In this scenario, the loop will iterate through all the Pokémon in both teams.
        Overall, the worst-case time complexity is O(n+m), where n is the maximum number of Pokémon in one team, and m is the number of pokemon in the other team.

        Returns:
            Tuple[Trainer, Trainer, Trainer, int, int]: A tuple containing information about the battle, including 
            the winner trainer, the names of the trainers involved, and the remaining lives of each trainer.
        """
        # Extract trainers and lives from current battle
        trainer1 = self.player_trainer
        trainer2 = self.enemy_trainers.serve()
        
        t_1 = trainer1[0]  # Player trainer
        t_2 = trainer2[0]  # Enemy trainer
        l_1 = trainer1[1]  # Player trainer's lives
        l_2 = trainer2[1]  # Enemy trainer's lives

        # Create a battle instance between the two trainers
        b = Battle(t_1, t_2, BattleMode.ROTATE)
        b.teams = (b.t_1.pokemon_team.team, b.t_2.pokemon_team.team)
        
        # Commence the battle and determine the winner
        winner = b.commence_battle() #O(n)

        # Process the outcome of the battle
        if winner == t_1:  # Player wins
            print('You win!')
            self.defeated_counter += 1
            new_lives_t2 = l_2 - 1  # Decrease enemy trainer's lives
            new_tuple2 = (t_2, new_lives_t2)
            new_tuple1 = (t_1, l_1)
        elif winner == t_2:  # Enemy wins
            print('Enemy wins.')
            new_lives_t1 = l_1 - 1  # Decrease player trainer's lives
            new_tuple1 = (t_1, new_lives_t1)
            new_tuple2 = (t_2, l_2)

        # Check if enemy trainer has remaining lives
        if new_tuple2[1] > 0:
            # Regenerate enemy trainer's team
            new_tuple2[0].pokemon_team.regenerate_team(BattleMode.ROTATE)
            self.enemy_trainers.append(new_tuple2)
        else:
            print(f"{t_2.get_name()} is out of lives")

        # Check if player trainer has remaining lives
        if new_tuple1[1] > 0:
            new_tuple1[0].pokemon_team.regenerate_team(BattleMode.ROTATE)
        else:
            print("You are out of lives")

        print(f"Defeated enemies: {self.defeated_counter}")
        
        # Return battle results
        return (winner.get_name(), t_1.get_name(), t_2.get_name(), new_tuple1[1], new_tuple2[1])


    def enemies_defeated(self) -> int:
        """
        Returns the number of enemy trainers defeated by the player.

        Returns:
            int: The number of defeated enemy trainers.
        """
        return self.defeated_counter