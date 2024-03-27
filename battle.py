from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
import random

class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        self.t_1 = trainer_1
        self.t_2 = trainer_2
        self.battle_mode = battle_mode
        self.teams = None
        self.criterion = criterion

    def commence_battle(self) -> Trainer | None:
        
        self._create_teams()
        
        
        if self.battle_mode.value == 0:
            return self.set_battle()
            
        elif self.battle_mode.value == 1:
            return self.rotate_battle()
            
        elif self.battle_mode.value == 2:
            return self.optimise_battle()
        
    def _create_teams(self) -> Tuple[PokeTeam, PokeTeam]:
       
        if self.battle_mode.value == 0:
            self.teams = (self.t_1.pokemon_team.assemble_team('set'), self.t_2.pokemon_team.assemble_team('set'))
        elif self.battle_mode.value == 1:
            self.teams = (self.t_1.pokemon_team.assemble_team('rotating'), self.t_2.pokemon_team.assemble_team('rotating'))
        elif self.battle_mode.value == 2:
            self.teams = (self.t_1.pokemon_team.assemble_team('optimise'), self.t_2.pokemon_team.assemble_team('optimise'))

    def set_battle(self) -> PokeTeam | None:
        while not self.teams[0].is_empty() and not self.teams[1].is_empty():
            mon1 = self.teams[0].pop() 
            mon2 = self.teams[1].pop()

            if mon1.get_speed() > mon2.get_speed():
                mon2.defend(mon1.attack(mon2)*(self.t_1.get_pokedex_completion()/self.t_2.get_pokedex_completion()))
                print(f"{mon1.get_name()} attacks {mon2.get_name()} and its health is lowered to {round(mon2.get_health())}")
                self.teams[0].push(mon1)
                if mon2.get_health() > 0:
                    self.teams[1].push(mon2)
                else:
                    print(f"{mon2.get_name()} fainted")
                    mon1.level_up()
                    print(f"{mon1.get_name()} grew to level {mon1.get_level()}")
            
            elif mon1.get_speed() < mon2.get_speed():
                mon1.defend(mon2.attack(mon1)*(self.t_2.get_pokedex_completion()/self.t_1.get_pokedex_completion()))
                print(f"{mon2.get_name()} attacks {mon1.get_name()} and its health is lowered to {round(mon1.get_health())}")
                self.teams[1].push(mon2)
                if mon1.get_health() > 0:
                    self.teams[0].push(mon1)
                else:
                    print(f"{mon1.get_name()} fainted")
                    mon2.level_up()
                    print(f"{mon2.get_name()} grew to level {mon2.get_level()}")

            else:
                mon1.defend(mon2.attack(mon1)*(self.t_2.get_pokedex_completion()/self.t_1.get_pokedex_completion()))
                mon2.defend(mon1.attack(mon2)*(self.t_1.get_pokedex_completion()/self.t_2.get_pokedex_completion()))
                print(f"{mon1.get_name()} attacks {mon2.get_name()}, its health is lowered to {round(mon2.get_health())}, and {mon2.get_name()} attacks {mon1.get_name()}, its health is lowered to {round(mon1.get_health())}")
                
                if mon1.get_health() > 0:
                    self.teams[0].push(mon1)
                else:
                    print(f"{mon1.get_name()} fainted")
                    mon2.level_up()
                    print(f"{mon2.get_name()} grew to level {mon2.get_level()}")
                
                if mon2.get_health() > 0:
                    self.teams[1].push(mon2)
                else:
                    print(f"{mon2.get_name()} fainted")
                    mon1.level_up()
                    print(f"{mon1.get_name()} grew to level {mon1.get_level()}")
                 
        if self.teams[0].is_empty() and self.teams[1].is_empty():
            return None
        elif self.teams[0].is_empty() and not self.teams[1].is_empty():
            return self.t_2 
        elif not self.teams[0].is_empty() and self.teams[1].is_empty():
            return self.t_1
       
    def rotate_battle(self) -> PokeTeam | None:
        
        while not self.teams[0].is_empty() and not self.teams[1].is_empty():
            
            mon1 = self.teams[0].serve()
            print(globals().get(mon1))

            mon2 = self.teams[1].serve()

            if mon1.get_speed() > mon2.get_speed():
                mon2.defend(mon1.attack(mon2)*(self.t_1.get_pokedex_completion()/self.t_2.get_pokedex_completion()))
                print(f"{mon1.get_name()} attacks {mon2.get_name()} and its health is lowered to {round(mon2.get_health())}")
                self.teams[0].append(mon1)
                if mon2.get_health() > 0:
                    self.teams[1].append(mon2)
                else:
                    print(f"{mon2.get_name()} fainted")
                    mon1.level_up()
                    print(f"{mon1.get_name()} grew to level {mon1.get_level()}")
            
            elif mon1.get_speed() < mon2.get_speed():
                mon1.defend(mon2.attack(mon1)*(self.t_2.get_pokedex_completion()/self.t_1.get_pokedex_completion()))
                print(f"{mon2.get_name()} attacks {mon1.get_name()} and its health is lowered to {round(mon1.get_health())}")
                self.teams[1].append(mon2)
                if mon1.get_health() > 0:
                    self.teams[0].append(mon1)
                else:
                    print(f"{mon1.get_name()} fainted")
                    mon2.level_up()
                    print(f"{mon2.get_name()} grew to level {mon2.get_level()}")

            else:
                mon1.defend(mon2.attack(mon1)*(self.t_2.get_pokedex_completion()/self.t_1.get_pokedex_completion()))
                mon2.defend(mon1.attack(mon2)*(self.t_1.get_pokedex_completion()/self.t_2.get_pokedex_completion()))
                print(f"{mon1.get_name()} attacks {mon2.get_name()}, its health is lowered to {round(mon2.get_health())}, and {mon2.get_name()} attacks {mon1.get_name()}, its health is lowered to {round(mon1.get_health())}")
                
                if mon1.get_health() > 0:
                    self.teams[0].append(mon1)
                else:
                    print(f"{mon1.get_name()} fainted")
                    mon2.level_up()
                    print(f"{mon2.get_name()} grew to level {mon2.get_level()}")

                if mon2.get_health() > 0:
                    self.teams[1].append(mon2)
                else:
                    print(f"{mon2.get_name()} fainted")
                    mon1.level_up()
                    print(f"{mon1.get_name()} grew to level {mon1.get_level()}")

        if self.teams[0].is_empty() and self.teams[1].is_empty():
            return None
        elif self.teams[0].is_empty() and not self.teams[1].is_empty():
            return self.t_2 
        elif not self.teams[0].is_empty() and self.teams[1].is_empty():
            return self.t_1

        
        
    def optimise_battle(self) -> PokeTeam | None:
        original_team_health1 = self.teams[0] 
        original_team_health2 = self.teams[1] 

        


if __name__ == '__main__':
    t1 = Trainer('Ash')
    t1.pick_team("random")
    print(t1.get_team())

    t2 = Trainer('Gary')
    t2.pick_team('random')
    print(t2.get_team())
    b = Battle(t1, t2, BattleMode.ROTATE)
    
    winner = b.commence_battle()
    
   
    if winner is None:
       print("Its a draw")
    else:
       print(f"The winner is {winner.get_name()}")
