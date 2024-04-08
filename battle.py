from poke_team import *
from pokemon_base import *
from pokemon import *
from typing import Tuple
from battle_mode import BattleMode
import random
import math 
"""
Unless stated otherwise, all functions in this file are O(1) best/worst case.
"""
def attacks(attacker, defender, multiplier):
    """
    Executes an attack action between two Pokémon.

    Args:
        attacker: The attacking Pokémon object.
        defender: The defending Pokémon object.
        multiplier: The multiplier applied to the attack.

    Returns:
        None
    """
    # Perform the attack action by calling the defend method of the defender
    # and passing the result of the attacking Pokémon's attack method multiplied by the multiplier
    defender.defend(math.ceil(attacker.attack(defender) * multiplier))

    # Print the attack message indicating the attacker, defender, and the defender's remaining health
    print(f"{attacker.get_name()} attacks {defender.get_name()}: {defender.get_name()} has {round(defender.get_health())} health")

        
def lvl_faints(lvl_up, faints):
    """
    Handles the fainting of a Pokémon.

    Args:
        lvl_up: The Pokémon that leveled up.
        faints: The Pokémon that fainted.

    Returns:
        None
    """
    # Print a message indicating that the faints Pokémon has fainted
    print(f"{faints.get_name()} fainted")

    # Level up the lvl_up Pokémon
    lvl_up.level_up()

    # Print a message indicating the lvl_up Pokémon has grown to a new level
    print(f"{lvl_up.get_name()} grew to level {lvl_up.get_level()}")


def battle_turn_set(faster_mon, slower_mon, faster_team, slower_team, pokedex1, pokedex2):
    """
    Executes a battle turn in the set mode.

    Args:
        faster_mon: The Pokémon attacking first.
        slower_mon: The Pokémon being attacked.
        faster_team: The team of the faster Pokémon.
        slower_team: The team of the slower Pokémon.
        pokedex1: The completion percentage of the Pokédex of the faster Pokémon's trainer.
        pokedex2: The completion percentage of the Pokédex of the slower Pokémon's trainer.

    Returns:
        None
    """
    # Attack by the faster_mon on the slower_mon with a certain multiplier
    attacks(faster_mon, slower_mon, pokedex1/pokedex2)

    # Check if the slower_mon is still alive after the attack
    if slower_mon.get_health() > 0:
        # Attack by the slower_mon on the faster_mon with a certain multiplier
        attacks(slower_mon, faster_mon, pokedex2/pokedex1)

        # Check if the faster_mon is still alive after the attack
        if faster_mon.get_health() > 0:
            # Decrease health of both Pokémon
            faster_mon.health -= 1
            slower_mon.health -= 1

            # Check the state of both Pokémon after the attacks
            if faster_mon.is_alive() and slower_mon.is_alive():
                # Push both Pokémon back to their teams
                faster_team.push(faster_mon) 
                slower_team.push(slower_mon)
            elif slower_mon.is_alive() and not faster_mon.is_alive():
                # Handle the case where faster_mon fainted
                lvl_faints(slower_mon, faster_mon)
                slower_team.push(slower_mon)
            elif not slower_mon.is_alive() and faster_mon.is_alive():
                # Handle the case where slower_mon fainted
                lvl_faints(faster_mon, slower_mon)
                faster_team.push(faster_mon) 
            elif not slower_mon.is_alive() and not faster_mon.is_alive():
                # Handle the case where both Pokémon fainted
                print('Both pokemon fainted')

        else:
            # Handle the case where faster_mon fainted
            lvl_faints(slower_mon, faster_mon)
            slower_team.push(slower_mon)
    else:
        # Handle the case where slower_mon fainted
        lvl_faints(faster_mon, slower_mon)
        faster_team.push(faster_mon)


def battle_turn_rotate(faster_mon, slower_mon, faster_team, slower_team, pokedex1, pokedex2):
    """
    Executes a battle turn in the rotate mode.

    Args:
        faster_mon: The Pokémon attacking first.
        slower_mon: The Pokémon being attacked.
        faster_team: The team of the faster Pokémon.
        slower_team: The team of the slower Pokémon.
        pokedex1: The completion percentage of the Pokédex of the faster Pokémon's trainer.
        pokedex2: The completion percentage of the Pokédex of the slower Pokémon's trainer.

    Returns:
        None
    """
    # Attack by the faster_mon on the slower_mon with a certain multiplier
    attacks(faster_mon, slower_mon, pokedex1/pokedex2) 

    # Check if slower_mon is alive after the attack
    if slower_mon.is_alive():
        # Attack by slower_mon on faster_mon with a certain multiplier
        attacks(slower_mon, faster_mon, pokedex2/pokedex1)

        # Check if faster_mon is alive after the attack
        if faster_mon.is_alive():
            # Decrease health of both Pokémon
            faster_mon.health -= 1
            slower_mon.health -= 1

            # Check the state of both Pokémon after the attacks
            if faster_mon.is_alive() and slower_mon.is_alive():
                # Append both Pokémon back to their teams
                faster_team.append(faster_mon) 
                slower_team.append(slower_mon)
            elif slower_mon.is_alive() and not faster_mon.is_alive():
                # Handle the case where faster_mon fainted
                lvl_faints(slower_mon, faster_mon)
                slower_team.append(slower_mon)
            elif not slower_mon.is_alive() and faster_mon.is_alive():
                # Handle the case where slower_mon fainted
                lvl_faints(faster_mon, slower_mon)
                faster_team.append(faster_mon) 
            elif not slower_mon.is_alive() and not faster_mon.is_alive():
                # Handle the case where both Pokémon fainted
                print('Both pokemon fainted')

        else:
            # Handle the case where faster_mon fainted
            lvl_faints(slower_mon, faster_mon)
            slower_team.append(slower_mon)
    else:
        # Handle the case where slower_mon fainted
        lvl_faints(faster_mon, slower_mon)
        faster_team.append(faster_mon)


def add_back_to_team(criterion, team, mon, special):
    """
    Adds a Pokémon back to an optimised team with adjustments based on a given criterion.

    Args:
        criterion (str): The criterion for adjustment ('health', 'level', 'attack', 'defence', 'speed').
        team (list): The team to which the Pokémon is added.
        mon: The Pokémon to be added back to the team.
        special (bool): A flag indicating whether to apply special adjustments.

    Returns:
        None
    """
    if special:
        # Apply special adjustments based on the criterion
        if criterion == 'health':
            team.add(ListItem(mon, mon.get_health() * (-1)))
        elif criterion == 'level':
            team.add(ListItem(mon, mon.get_level() * (-1)))
        elif criterion == 'attack':
            team.add(ListItem(mon, mon.get_attack() * (-1)))
        elif criterion == 'defence':
            team.add(ListItem(mon, mon.get_defence() * (-1)))
        elif criterion == 'speed':
            team.add(ListItem(mon, mon.get_speed() * (-1)))
    else:
        # Add the Pokémon back to the team without adjustments
        if criterion == 'health':
            team.add(ListItem(mon, mon.get_health()))
        elif criterion == 'level':
            team.add(ListItem(mon, mon.get_level()))
        elif criterion == 'attack':
            team.add(ListItem(mon, mon.get_attack()))
        elif criterion == 'defence':
            team.add(ListItem(mon, mon.get_defence()))
        elif criterion == 'speed':
            team.add(ListItem(mon, mon.get_speed()))


def battle_turn_optimise(criterion, faster_mon, slower_mon, faster_team, slower_team, pokedex1, pokedex2, special):
    """
    Executes a battle turn with optimization based on a given criterion.

    Args:
        criterion: The criterion for optimization (e.g., 'health', 'level', 'attack', 'defence', 'speed').
        faster_mon: The Pokémon attacking first.
        slower_mon: The Pokémon being attacked.
        faster_team: The team of the faster Pokémon.
        slower_team: The team of the slower Pokémon.
        pokedex1: The completion percentage of the Pokédex of the faster Pokémon's trainer.
        pokedex2: The completion percentage of the Pokédex of the slower Pokémon's trainer.
        special: A boolean indicating whether to apply special adjustments to the team based on the criterion.

    Returns:
        None
    """
    # Attack by faster_mon on slower_mon with a certain multiplier
    attacks(faster_mon, slower_mon, pokedex1 / pokedex2)

    # Check if slower_mon is alive after the attack
    if slower_mon.get_health() > 0:
        # Attack by slower_mon on faster_mon with a certain multiplier
        attacks(slower_mon, faster_mon, pokedex2 / pokedex1)

        # Check if faster_mon is alive after the attack
        if faster_mon.get_health() > 0:
            # Decrease health of both Pokémon
            faster_mon.health -= 1
            slower_mon.health -= 1

            # Check the state of both Pokémon after the attacks
            if faster_mon.is_alive() and slower_mon.is_alive():
                # Add both Pokémon back to their teams with adjustments based on the criterion
                add_back_to_team(criterion, faster_team, faster_mon, special) 
                add_back_to_team(criterion, slower_team, slower_mon, special)
            elif slower_mon.is_alive() and not faster_mon.is_alive():
                # Handle the case where faster_mon fainted
                lvl_faints(slower_mon, faster_mon)
                add_back_to_team(criterion, slower_team, slower_mon, special)
            elif not slower_mon.is_alive() and faster_mon.is_alive():
                # Handle the case where slower_mon fainted
                lvl_faints(faster_mon, slower_mon)
                add_back_to_team(criterion, faster_team, faster_mon, special) 
            elif not slower_mon.is_alive() and not faster_mon.is_alive():
                # Handle the case where both Pokémon fainted
                print('Both pokemon fainted')

        else:
            # Handle the case where faster_mon fainted
            lvl_faints(slower_mon, faster_mon)
            add_back_to_team(criterion, slower_team, slower_mon, special) 
    else:
        # Handle the case where slower_mon fainted
        lvl_faints(faster_mon, slower_mon)
        add_back_to_team(criterion, faster_team, faster_mon, special)


class Battle:
    """ 
    Represents a mechanism for conducting Pokémon battles between two trainers in a turn-based fashion.

    Unless stated otherwise, all methods in this class are O(1) best/worst case.
    """
    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion='health') -> None:
        """
        Initializes a Battle instance.

        Args:
            trainer_1 (Trainer): The first trainer participating in the battle.
            trainer_2 (Trainer): The second trainer participating in the battle.
            battle_mode (BattleMode): The mode of the battle (e.g., 'set' or 'rotate').
            criterion (str): The criterion used for adjustments (default is 'health').

        Returns:
            None
        """
        self.t_1 = trainer_1
        self.t_2 = trainer_2
        self.battle_mode = battle_mode
        self.teams = None
        self.regen_teams = None
        self.criterion = criterion


    def commence_battle(self) -> Trainer | None:
        """
        Initiates the battle based on the chosen battle mode.

        Returns:
            Trainer or None: The winning trainer or None if the battle does not conclude.
        """
        # Check if it's a "set" battle mode
        if self.battle_mode.value == 0:
            # Call the set_battle method and return the winning trainer
            return self.set_battle()
        
        # Check if it's a "rotate" battle mode
        elif self.battle_mode.value == 1:
            # Call the rotate_battle method and return the winning trainer
            return self.rotate_battle()
        
        # Check if it's an "optimise" battle mode
        elif self.battle_mode.value == 2:
            # Call the optimise_battle method and return the winning trainer
            return self.optimise_battle()
        
        # If the battle mode is not recognized, return None
        return None

        
    def _create_teams(self) -> Tuple[PokeTeam, PokeTeam]:
        """
        Creates and assembles teams for both trainers based on the battle mode.

        Returns:
            Tuple[PokeTeam, PokeTeam]: A tuple containing the teams for both trainers.
        """
        # Let both trainers pick their teams
        self.t_1.pick_team('Random')
        self.t_2.pick_team('Random')
        
        # Depending on the battle mode, assemble the teams accordingly
        if self.battle_mode.value == 0:
            # For "set" battle mode, assemble teams with the "SET" strategy
            self.t_1.pokemon_team.assemble_team(BattleMode.SET)
            self.t_2.pokemon_team.assemble_team(BattleMode.SET)
        
        elif self.battle_mode.value == 1:
            # For "rotate" battle mode, assemble teams with the "ROTATE" strategy
            self.t_1.pokemon_team.assemble_team(BattleMode.ROTATE)
            self.t_2.pokemon_team.assemble_team(BattleMode.ROTATE)
            
        elif self.battle_mode.value == 2:
            # For "optimise" battle mode, assemble teams with the "OPTIMISE" strategy
            self.t_1.pokemon_team.assemble_team(BattleMode.OPTIMISE)
            # Assign teams with specific criterion for optimisation
            self.t_1.pokemon_team.assign_team(self.criterion)
            self.t_2.pokemon_team.assemble_team(BattleMode.OPTIMISE)
            # Assign teams with specific criterion for optimisation
            self.t_2.pokemon_team.assign_team(self.criterion)
            
        # Store the assembled teams in the instance variable 'teams'
        self.teams = (self.t_1.pokemon_team.team, self.t_2.pokemon_team.team)
        
        # Return the assembled teams
        return self.teams


    def set_battle(self) -> PokeTeam | None:
        """
        Conducts a battle using the "set" mode strategy.

        Returns:
            PokeTeam | None: The winning trainer or None if it's a tie.
       
        Complexity Analysis: 
        
        Best Case:
        The best case occurs when one of the teams runs out of Pokémon before the battle starts.
        In this case, the loop will terminate early, resulting in fewer iterations.
        Complexity: O(1) - constant time.
        
        Worst Case:
        The worst case happens when both teams have an equal number of Pokémon, and the battle continues until one team loses all its Pokémon.
        In this scenario, the loop will iterate through all the Pokémon in both teams.
        Within each iteration, there are constant-time operations such as popping, pushing, determining attack order, and resolving attacks.
        Overall, the worst-case time complexity is O(n+m), where n is the maximum number of Pokémon in one team, and m is the number of pokemon in the other team.
        """
        while not self.teams[0].is_empty() and not self.teams[1].is_empty():
            # Pop the next Pokemon from each team
            mon1 = self.teams[0].pop() 
            mon2 = self.teams[1].pop()
            # Register the Pokemon for each trainer
            self.t_2.register_pokemon(mon1)
            self.t_1.register_pokemon(mon2)

            # Determine which Pokemon attacks first based on speed
            if mon1.get_speed() > mon2.get_speed():
                # If mon1 is faster, it attacks first
                battle_turn_set(mon1, mon2, self.teams[0], self.teams[1], self.t_1.get_pokedex_completion(), self.t_2.get_pokedex_completion())
            
            elif mon2.get_speed() > mon1.get_speed():
                # If mon2 is faster, it attacks first
                battle_turn_set(mon2, mon1, self.teams[1], self.teams[0], self.t_2.get_pokedex_completion(), self.t_1.get_pokedex_completion())
            
            else:
                # If both Pokemon have the same speed, they attack simultaneously
                attacks(mon2, mon1, (self.t_2.get_pokedex_completion()/self.t_1.get_pokedex_completion()))
                attacks(mon1, mon2, (self.t_1.get_pokedex_completion()/self.t_2.get_pokedex_completion()))
                
                # Handle the aftermath of the simultaneous attack
                if mon1.get_health() > 0 and mon2.get_health() > 0:
                    # If both Pokemon survive, they each lose 1 health point
                    mon1.health -= 1
                    mon2.health -= 1
                    
                    if mon1.get_health() > 0 and mon2.get_health() > 0:
                        # If both Pokemon still have health, push them back to their teams
                        self.teams[0].push(mon1)
                        self.teams[1].push(mon2)
                    
                    elif mon1.get_health() > 0 and not mon2.get_health() > 0:
                        # If mon2 faints, handle the fainting
                        lvl_faints(mon1, mon2)
                        self.teams[0].push(mon1)
                    
                    elif mon2.get_health() > 0 and not mon1.get_health() > 0:
                        # If mon1 faints, handle the fainting
                        lvl_faints(mon2, mon1)
                        self.teams[1].push(mon2)
                    
                    elif not mon2.get_health() > 0 and not mon1.get_health() > 0:
                        # If both Pokemon faint, print a message
                        print(f"{mon1.get_name()} fainted")
                        print(f"{mon2.get_name()} fainted")
                        
                elif not mon1.get_health() > 0 and mon2.get_health() > 0:
                    # If mon1 faints, handle the fainting
                    lvl_faints(mon2, mon1)
                    self.teams[1].push(mon2)
                
                elif mon1.get_health() > 0 and not mon2.get_health() > 0:
                    # If mon2 faints, handle the fainting
                    lvl_faints(mon1, mon2)
                    self.teams[0].push(mon1)

                elif not mon2.get_health() > 0 and not mon1.get_health() > 0:
                    # If both Pokemon faint, print a message
                    print(f"{mon1.get_name()} fainted")
                    print(f"{mon2.get_name()} fainted")
        # Return the winning trainer or None if it's a tie
        if self.teams[0].is_empty() and self.teams[1].is_empty():
            return None
        elif self.teams[0].is_empty() and not self.teams[1].is_empty():
            return self.t_2 
        elif not self.teams[0].is_empty() and self.teams[1].is_empty():
            return self.t_1

       
    def rotate_battle(self) -> PokeTeam | None:
        """
        Conducts a battle using the "rotate" mode strategy.

        Returns:
            PokeTeam | None: The winning trainer or None if it's a tie.
        
        Complexity Analysis: 
        
        Best Case:
        The best case occurs when one of the teams runs out of Pokémon before the battle starts.
        In this case, the loop will terminate early, resulting in fewer iterations.
        Complexity: O(1) - constant time.
        
        Worst Case:
        The worst case happens when both teams have an equal number of Pokémon, and the battle continues until one team loses all its Pokémon.
        In this scenario, the loop will iterate through all the Pokémon in both teams.
        Within each iteration, there are constant-time operations such as popping, pushing, determining attack order, and resolving attacks.
        Overall, the worst-case time complexity is O(n+m), where n is the maximum number of Pokémon in one team, and m is the number of pokemon in the other team.
        """

        while not self.teams[0].is_empty() and not self.teams[1].is_empty():
            # Serve the next Pokemon from each team
            mon1 = self.teams[0].serve() 
            mon2 = self.teams[1].serve()
            # Register the Pokemon for each trainer
            self.t_2.register_pokemon(mon1)
            self.t_1.register_pokemon(mon2)

            # Determine which Pokemon attacks first based on speed
            if mon1.get_speed() > mon2.get_speed():
                # If mon1 is faster, it attacks first
                battle_turn_rotate(mon1, mon2, self.teams[0], self.teams[1], self.t_1.get_pokedex_completion(), self.t_2.get_pokedex_completion())
                
            elif mon2.get_speed() > mon1.get_speed():
                # If mon2 is faster, it attacks first
                battle_turn_rotate(mon2, mon1, self.teams[1], self.teams[0], self.t_2.get_pokedex_completion(), self.t_1.get_pokedex_completion())
            
            else:
                # If both Pokemon have the same speed, they attack simultaneously
                attacks(mon2, mon1, (self.t_2.get_pokedex_completion()/self.t_1.get_pokedex_completion()))
                attacks(mon1, mon2, (self.t_1.get_pokedex_completion()/self.t_2.get_pokedex_completion()))
                
                # Handle the aftermath of the simultaneous attack
                if mon1.get_health() > 0 and mon2.get_health() > 0:
                    # If both Pokemon survive, they each lose 1 health point
                    mon1.health -= 1
                    mon2.health -= 1
                    
                    if mon1.get_health() > 0 and mon2.get_health() > 0:
                        # If both Pokemon still have health, append them back to their teams
                        self.teams[0].append(mon1)
                        self.teams[1].append(mon2)
                    
                    elif mon1.get_health() > 0 and not mon2.get_health() > 0:
                        # If mon2 faints, handle the fainting
                        lvl_faints(mon1, mon2)
                        self.teams[0].append(mon1)
                    
                    elif mon2.get_health() > 0 and not mon1.get_health() > 0:
                        # If mon1 faints, handle the fainting
                        lvl_faints(mon2, mon1)
                        self.teams[1].append(mon2)
                    
                    elif not mon2.get_health() > 0 and not mon1.get_health() > 0:
                        # If both Pokemon faint, print a message
                        print(f"{mon1.get_name()} fainted")
                        print(f"{mon2.get_name()} fainted")
                        
                elif not mon1.get_health() > 0 and mon2.get_health() > 0:
                    # If mon1 faints, handle the fainting
                    lvl_faints(mon2, mon1)
                    self.teams[1].append(mon2)
                
                elif mon1.get_health() > 0 and not mon2.get_health() > 0:
                    # If mon2 faints, handle the fainting
                    lvl_faints(mon1, mon2)
                    self.teams[0].append(mon1)

                elif not mon2.get_health() > 0 and not mon1.get_health() > 0:
                    # If both Pokemon faint, print a message
                    print(f"{mon1.get_name()} fainted")
                    print(f"{mon2.get_name()} fainted")
        # Return the winning trainer or None if it's a tie
        if self.teams[0].is_empty() and self.teams[1].is_empty():
            return None
        elif self.teams[0].is_empty() and not self.teams[1].is_empty():
            return self.t_2 
        elif not self.teams[0].is_empty() and self.teams[1].is_empty():
            return self.t_1

        
        
    def optimise_battle(self) -> PokeTeam | None:
        """
        Conducts a battle using the "optimise" mode strategy.

        Returns:
            PokeTeam | None: The winning trainer or None if it's a tie.

        Complexity Analysis: 
        
        Best Case:
        The best case occurs when one of the teams runs out of Pokémon before the battle starts.
        In this case, the loop will terminate early, resulting in fewer iterations.
        Complexity: O(1) - constant time.
        
        Worst Case:
        The worst case happens when both teams have an equal number of Pokémon, and the battle continues until one team loses all its Pokémon.
        In this scenario, the loop will iterate through all the Pokémon in both teams.
        Within each iteration, there are constant-time operations such as popping, pushing, determining attack order, and resolving attacks.
        Overall, the worst-case time complexity is O(n+m), where n is the maximum number of Pokémon in one team, and m is the number of pokemon in the other team.
        """
        while not self.teams[0].is_empty() and not self.teams[1].is_empty():

            # Serve the next Pokemon from each team
            mon1 = self.teams[0][0].value
            self.teams[0].delete_at_index(0)
            mon2 = self.teams[1][0].value
            self.teams[1].delete_at_index(0)
        
            # Register the Pokemon for each trainer
            self.t_2.register_pokemon(mon1)
            self.t_1.register_pokemon(mon2)
            
            # Determine which Pokemon attacks first based on speed
            if mon1.get_speed() > mon2.get_speed():
                # If mon1 is faster, it attacks first
                battle_turn_optimise(self.criterion, mon1, mon2, self.teams[0], self.teams[1], self.t_1.get_pokedex_completion(), self.t_2.get_pokedex_completion(), self.t_1.pokemon_team.reversed)
            
            elif mon1.get_speed() < mon2.get_speed():
                # If mon2 is faster, it attacks first
                battle_turn_optimise(self.criterion, mon2, mon1, self.teams[1], self.teams[0], self.t_2.get_pokedex_completion(), self.t_1.get_pokedex_completion(), self.t_1.pokemon_team.reversed)
                
            else:
                # If both Pokemon have the same speed, they attack simultaneously
                attacks(mon2, mon1, (self.t_2.get_pokedex_completion()/self.t_1.get_pokedex_completion()))
                attacks(mon1, mon2, (self.t_1.get_pokedex_completion()/self.t_2.get_pokedex_completion()))
                
                # Handle the aftermath of the simultaneous attack
                if mon1.get_health() > 0 and mon2.get_health() > 0:
                    mon1.health -= 1
                    mon2.health -= 1
                    
                    if mon1.get_health() > 0 and mon2.get_health() > 0:
                        # If both Pokemon still have health, add them back to their teams
                        add_back_to_team(self.criterion, self.teams[0], mon1, self.t_1.pokemon_team.reversed)
                        add_back_to_team(self.criterion, self.teams[1], mon2, self.t_1.pokemon_team.reversed)
                    
                    elif mon1.get_health() > 0 and not mon2.get_health() > 0:
                        # If mon2 faints, handle the fainting
                        lvl_faints(mon1, mon2)
                        add_back_to_team(self.criterion, self.teams[0], mon1, self.t_1.pokemon_team.reversed)
                    
                    elif mon2.get_health() > 0 and not mon1.get_health() > 0:
                        # If mon1 faints, handle the fainting
                        lvl_faints(mon2, mon1)
                        add_back_to_team(self.criterion, self.teams[1], mon2, self.t_1.pokemon_team.reversed)
                    
                    elif not mon2.get_health() > 0 and not mon1.get_health() > 0:
                        # If both Pokemon faint, print a message
                        print(f"{mon1.get_name()} fainted")
                        print(f"{mon2.get_name()} fainted")
                        
                elif not mon1.get_health() > 0 and mon2.get_health() > 0:
                    # If mon1 faints, handle the fainting
                    lvl_faints(mon2, mon1)
                    add_back_to_team(self.criterion, self.teams[1], mon2, self.t_1.pokemon_team.reversed)
                
                elif mon1.get_health() > 0 and not mon2.get_health() > 0:
                    # If mon2 faints, handle the fainting
                    lvl_faints(mon1, mon2)
                    add_back_to_team(self.criterion, self.teams[0], mon1, self.t_1.pokemon_team.reversed)

                elif not mon2.get_health() > 0 and not mon1.get_health() > 0:
                    # If both Pokemon faint, print a message
                    print(f"{mon1.get_name()} fainted")
                    print(f"{mon2.get_name()} fainted")

        # Return the winning trainer or None if it's a tie
        if self.teams[0].is_empty() and self.teams[1].is_empty():
            return None
        elif self.teams[0].is_empty() and not self.teams[1].is_empty():
            return self.t_2 
        elif not self.teams[0].is_empty() and self.teams[1].is_empty():
            return self.t_1
