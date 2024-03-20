from pokemon import *
import random
from typing import List
from aset import *
from data_structures.stack_adt import *
from data_structures.queue_adt import *
from data_structures.sorted_list_adt import *
from data_structures.array_sorted_list import *

class PokeTeam:
    random.seed(20)
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()

    def __init__(self):
        self.team = ArrayR(PokeTeam.TEAM_LIMIT)
        self.team_display = ArrayR(PokeTeam.TEAM_LIMIT)

    def choose_manually(self):
        for i in range(PokeTeam.TEAM_LIMIT):
            choice = input(f"Enter the name of Pokemon {i + 1}")
            pokemon_class = globals().get(choice)
            if pokemon_class in PokeTeam.POKE_LIST:
                self.team[i] = pokemon_class()
            
            else:
                print("That Pokemon does not exist")
        self.team_display = self.team

    def choose_randomly(self) -> None:
        for i in range(PokeTeam.TEAM_LIMIT):
            random_pokemon = random.choice(PokeTeam.POKE_LIST)
            self.team[i] = random_pokemon()
        self.team_display = self.team
        
    def regenerate_team(self) -> None:
        raise NotImplementedError
    
    def assemble_team(self, mode):
        assembled_team = None

        if mode == 'set':
            
            assembled_team = ArrayStack(PokeTeam.TEAM_LIMIT)
            for i in range(PokeTeam.TEAM_LIMIT):
                assembled_team.push(self.team[i])
                
        elif mode == 'rotating':
            
            assembled_team = CircularQueue(PokeTeam.TEAM_LIMIT)
            for i in range(PokeTeam.TEAM_LIMIT):
                assembled_team.append(self.team[i])

        elif mode == 'optimised':
            self.assign_team()
            assembled_team = ArraySortedList()
            for i in range(PokeTeam.TEAM_LIMIT):
                assembled_team.add(self.team[i])
    
        self.team = assembled_team
        return self.team
        
    #def assign_team(self):
        


    
    def special(self):
        #if isinstance(self.team, ArrayStack):

        #if isinstance(self.team, CircularQueue):

        #if isinstance(self.team, ArraySortedList):
        pass
    
    def __getitem__(self, index: int):
        return self.team_display[index]

    def __len__(self):
        return len(self.team)

    def __str__(self):
        team_str = ""
        for pokemon in self.team_display:
            team_str += str(pokemon) + "\n"
        return team_str


class Trainer:

    def __init__(self, name) -> None:
        self.name = name
        self.pokemon_team = PokeTeam()
        self.pokedex = ASet(15)

    def pick_team(self, method: str) -> None:
        if method == "manual":
            self.pokemon_team.choose_manually()
        elif method == "random":
            self.pokemon_team.choose_randomly()
        
    def get_team(self) -> PokeTeam:
        return self.pokemon_team

    def get_name(self) -> str:
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        self.pokedex.add(pokemon.poketype)

    def get_pokedex_completion(self) -> float:
        return round(float((self.pokedex.__len__())/0.15),2)

    def __str__(self) -> str:
        return f"{self.name}'s pokedex is {self.get_pokedex_completion()} % complete"

if __name__ == '__main__':
    t = Trainer("Max")
    t.pick_team("random")
    print(t.pokemon_team.assemble_team('set'))
    #print(t.pokemon_team.__getitem__(1))
    #print(t.pokemon_team.__len__())
    #print(t.pokemon_team.__str__())
    #print(t.get_team())
    #print(t.get_name())
    #t.register_pokemon(Bulbasaur())
    #print(t.get_pokedex_completion())
    #print(t.__str__())
