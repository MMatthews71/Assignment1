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
        team_size = int(input("How many pokemon will be in this team? (limit 6)"))
        for i in range(team_size):
            choice = input(f"Enter the name of Pokemon {i + 1}")
            pokemon_class = globals().get(choice)
            if pokemon_class in PokeTeam.POKE_LIST:
                self.team[i] = pokemon_class()
            else:
                print("That Pokemon does not exist")
        self.team_display = self.team

    def choose_randomly(self) -> None:
        team_size = int(input("How many pokemon will be in this team? (limit 6)"))
        for i in range(team_size):
            random_pokemon = random.choice(PokeTeam.POKE_LIST)
            self.team[i] = random_pokemon()
        self.team_display = self.team
        
    def regenerate_team(self, battle_mode, criterion) -> None:
        pass
        
    
    def assemble_team(self, mode):
        assembled_team = None

        if mode == 'set':
            
            assembled_team = ArrayStack(PokeTeam.TEAM_LIMIT)
            for i in range(PokeTeam.TEAM_LIMIT):
                if not self.team[i] == None:
                    assembled_team.push(self.team[i])
                
        elif mode == 'rotating':
            
            assembled_team = CircularQueue(PokeTeam.TEAM_LIMIT)
            for i in range(PokeTeam.TEAM_LIMIT):
                if not self.team[i] == None:
                    assembled_team.append(self.team[i])

        elif mode == 'optimised':
            self.assign_team()
            assembled_team = ArraySortedList(PokeTeam.TEAM_LIMIT)
            for i in range(PokeTeam.TEAM_LIMIT):
                if not self.team[i] == None:
                    assembled_team.add(self.team[i])
    
        self.team = assembled_team
        return self.team
        
    #def assign_team(self):
        #criterion =
    
    def special(self):
        #if isinstance(self.team, ArrayStack):

        #if isinstance(self.team, CircularQueue):

        #if isinstance(self.team, ArraySortedList):
        pass
    
    def __getitem__(self, index: int):
        return self.team_display[index]

    def __len__(self):
        length = 0
        for i in range(PokeTeam.TEAM_LIMIT):
            if not self.team[i] == None:
                length += 1
        return length

    def __str__(self):
        team_str = ""
        for i in range(len(self.team_display)):
            if self.team_display[i] is not None:
                team_str += str(self.team_display[i]) + "\n"
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
        for i in self.pokemon_team:
            if not i == None:
                self.register_pokemon(i)
        
    def get_team(self) -> PokeTeam:
        return self.pokemon_team

    def get_name(self) -> str:
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        self.pokedex.add(pokemon.poketype)

    def get_pokedex_completion(self) -> float:
        return round(float((self.pokedex.__len__())/15), 2)

    def __str__(self) -> str:
        return f"Trainer {self.name} Pokedex Completion: {round(self.get_pokedex_completion()*100)}%"

if __name__ == '__main__':
    t = Trainer("Max")
    t.pick_team("random")
    print(t.pokemon_team.assemble_team('optimised'))
    #print(t.pokemon_team.__getitem__(0))
    #print(t.pokemon_team.__len__())
    #print(t.pokemon_team.__str__())
    #print(t.get_team())
    #print(t.get_name())
    #t.register_pokemon(Bulbasaur())
    #print(t.get_pokedex_completion())
    #print(t.__str__())
