"""
This module contains PokeType, TypeEffectiveness and an abstract version of the Pokemon Class
"""
from abc import ABC
from enum import Enum
from data_structures.referential_array import ArrayR
import csv
import math

with open("type_effectiveness.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    type_effectiveness = list(csvreader)

type_effectiveness = [[float(value) for value in row] for row in type_effectiveness]

num_rows = len(type_effectiveness)
num_columns = len(type_effectiveness[0])

effectiveness_array = ArrayR(num_rows)

for i in range(num_rows): #O(n) best/worst case, where n is the number of rows in the array
    effectiveness_array[i] = type_effectiveness[i]

class PokeType(Enum):
    """
    This class contains all the different types that a Pokemon could belong to.
    Unless stated otherwise, all methods in this class are O(1) best/worst case.
    """
    FIRE = 0
    WATER = 1
    GRASS = 2
    BUG = 3
    DRAGON = 4
    ELECTRIC = 5
    FIGHTING = 6
    FLYING = 7
    GHOST = 8
    GROUND = 9
    ICE = 10
    NORMAL = 11
    POISON = 12
    PSYCHIC = 13
    ROCK = 14

class TypeEffectiveness:
    """
    Represents the type effectiveness of one Pokemon type against another.
    Unless stated otherwise, all methods in this class are O(1) best/worst case.
    """
    EFFECT_TABLE = effectiveness_array

    @classmethod
    def get_effectiveness(cls, attack_type: PokeType, defend_type: PokeType) -> float:
        """
        Returns the effectiveness of one Pokemon type against another, as a float.

        Parameters:
            attack_type (PokeType): The type of the attacking Pokemon.
            defend_type (PokeType): The type of the defending Pokemon.

        Returns:
            float: The effectiveness of the attack, as a float value between 0 and 4.
        """
        return cls.EFFECT_TABLE[attack_type.value][defend_type.value]
        

    def __len__(self) -> int:
        """
        Returns the number of types of Pokemon
        """
        return len(PokeType)
    

class Pokemon(ABC): # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """
    Represents a base Pokemon class with properties and methods common to all Pokemon.
    Unless stated otherwise, all methods in this class are O(1) best/worst case.
    """
    def __init__(self):
        """
        Initializes a new instance of the Pokemon class.
        """
        self.health = None
        self.level = None
        self.poketype = None
        self.battle_power = None
        self.evolution_line = None
        self.name = None
        self.experience = None
        self.defence = None
        self.speed = None

    def get_name(self) -> str:
        """
        Returns the name of the Pokemon.

        Returns:
            str: The name of the Pokemon.
        """
        return self.name

    def get_health(self) -> int:
        """
        Returns the current health of the Pokemon.

        Returns:
            int: The current health of the Pokemon.
        """
       
        return self.health 
        

    def get_level(self) -> int:
        """
        Returns the current level of the Pokemon.

        Returns:
            int: The current level of the Pokemon.
        """
        return self.level

    def get_speed(self) -> int:
        """
        Returns the current speed of the Pokemon.

        Returns:
            int: The current speed of the Pokemon.
        """
        return self.speed

    def get_experience(self) -> int:
        """
        Returns the current experience of the Pokemon.

        Returns:
            int: The current experience of the Pokemon.
        """
        return self.experience

    def get_poketype(self) -> PokeType:
        """
        Returns the type of the Pokemon.

        Returns:
            PokeType: The type of the Pokemon.
        """
        return self.poketype

    def get_defence(self) -> int:
        """
        Returns the defence of the Pokemon.

        Returns:
            int: The defence of the Pokemon.
        """
        return self.defence

    def get_evolution(self):
        """
        Returns the evolution line of the Pokemon.

        Returns:
            list: The evolution of the Pokemon.
        """
        return self.evolution_line

    def get_battle_power(self) -> int:
        """
        Returns the battle power of the Pokemon.

        Returns:
            int: The battle power of the Pokemon.
        """
        return self.battle_power

    def attack(self, other_pokemon) -> int:
        """
        Calculates and returns the damage that this Pokemon inflicts on the other Pokemon during an attack.

        Args:
            other_pokemon (Pokemon): The Pokemon that this Pokemon is attacking.

        Returns:
            int: The damage that this Pokemon inflicts on the other Pokemon during an attack.
    
        Variables:
            damage (int): The base damage inflicted by the attacking Pokemon.
            multiplier (float): The type effectiveness multiplier for the attack.
        """
        if other_pokemon.get_defence() < self.get_battle_power() / 2:
        # If the defending Pokemon's defence is less than half of the attacking Pokemon's battle power
            damage = math.ceil(self.get_battle_power() - other_pokemon.get_defence())

        elif other_pokemon.get_defence() < self.get_battle_power(): 
        # If the defending Pokemon's defence is less than the attacking Pokemon's battle power
            damage = math.ceil((self.get_battle_power() * 5 / 8) - (other_pokemon.get_defence() / 4))

        else:
        # If the defending Pokemon's defence is greater than or equal to the attacking Pokemon's battle power
            damage = math.ceil(self.get_battle_power() / 4)

        # Get the type effectiveness multiplier for the attack
        multiplier = TypeEffectiveness.get_effectiveness(self.poketype, other_pokemon.poketype)

        # Calculate the attack damage by multiplying the base damage with the type effectiveness multiplier
        attack_damage = damage * multiplier
            
        return attack_damage


    def defend(self, damage: int) -> None:
        """
        Reduces the health of the Pokemon by the given amount of damage, after taking
        the Pokemon's defence into account.

        Args:
            damage (int): The amount of damage to be inflicted on the Pokemon.
        
        Returns:
            None
        """
        # Calculate effective damage after considering the Pokemon's defense
        effective_damage = damage / 2 if damage < self.get_defence() else damage
        
        # Reduce the health of the Pokemon by the effective damage
        self.health -= effective_damage


    def level_up(self) -> None:
        """
        Increases the level of the Pokemon by 1, and evolves the Pokemon if it has
        reached the level required for evolution.
        
        Variables:
            self.level (int): The current level of the Pokemon.
            self.evolution_line (list): A list representing the evolution line of the Pokemon.
        
        Returns:
            None
        """
        # Increase the level of the Pokemon by 1
        self.level += 1
        
        # Check if the Pokemon has an evolution line defined and if it's not at the final stage
        if self.evolution_line and self.name in self.evolution_line[:-1]:
            self._evolve()  # Evolve the Pokemon


    def _evolve(self) -> None:
        """
        Evolves the Pokemon to the next stage in its evolution line, and updates
          its attributes accordingly.
        
        Variables:
            self.evolution_line (list): A list representing the evolution line of the Pokemon.

        Returns:
            None
        """
        if self.evolution_line:
            # Check if the Pokemon has an evolution line defined
            if self.name == self.evolution_line[0]:
                # Check if the Pokemon's current stage matches the first evolution in its line
                self.name = self.evolution_line[1]
                # Update the Pokemon's name to the next stage
                self.battle_power *= 1.5
                self.health = self.get_health() * 1.5
                self.speed *= 1.5
                self.defence *= 1.5
                # Increase each of the stats by 50%

            elif self.name == self.evolution_line[1]:
                # Check if the Pokemon's current stage matches the second evolution in its line
                self.name = self.evolution_line[2]
                # Update the Pokemon's name to the next stage
                self.battle_power *= 1.5
                self.health = self.get_health() * 1.5
                self.speed *= 1.5
                self.defence *= 1.5
                # Increase each of the stats by 50%

            else:
                print('This pokemon cannot evolve any further')
                # Inform that the Pokemon cannot evolve further if it doesn't match any evolution stage
        else:
            print('This pokemon cannot evolve')
            # Inform that the Pokemon cannot evolve if it doesn't have an evolution line defined

    def is_alive(self) -> bool:
        """
        Checks if the Pokemon is still alive (i.e. has positive health).

        Returns:
            bool: True if the Pokemon is still alive, False otherwise.
        """
        return self.get_health() > 0

    def __str__(self):
        """
        Return a string representation of the Pokemon instance in the format:
        <name> (Level <level>) with <health> health and <experience> experience
        """
        return f"{self.name} (Level {self.level}) with {self.get_health()} health and {self.get_experience()} experience"


