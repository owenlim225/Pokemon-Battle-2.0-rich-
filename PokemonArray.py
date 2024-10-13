import random

class PokemonArray:
    def __init__(self) -> None:  
        self.pokemon_Array = [
            # [Name, Health, Power, Poisons, Potions, isUsed]
            ["Pikachu", 0, 0, 0, 0, False],
            ["Charmander", 0, 0, 0, 0, False],
            ["Bulbasaur", 0, 0, 0, 0, False],
            ["Squirtle", 0, 0, 0, 0, False],
            ["Jigglypuff", 0, 0, 0, 0, False],
            ["Eevee", 0, 0, 0, 0, False],
            ["Snorlax", 0, 0, 0, 0, False],
            ["Gengar", 0, 0, 0, 0, False],
            ["Machamp", 0, 0, 0, 0, False],
            ["Mewtwo", 0, 0, 0, 0, False]
        ]
        
        self._randomValGenerator()

    def _randomValGenerator(self) -> None:
        # Poison and Potion
        for i in range(len(self.pokemon_Array)):
            randintHealth = random.randint(50, 100)
            randitPower = random.randint(50, 150)
            randintPoison = random.randint(1, 6)
            randitPotion = random.randint(1, 6)
            
            self.pokemon_Array[i][1] = randintHealth
            self.pokemon_Array[i][2] = randitPower
            self.pokemon_Array[i][3] = randintPoison
            self.pokemon_Array[i][4] = randitPotion
            
    @property
    def GetPokemonArray(self) -> list:
        # ============================================
        # Returns the pokemon_Array.
        #
        # Return:
        #     list: A 2D list where each sublist contains the following:
        #     [Name (str), Health (int), Power (int), Poisons (int), Potions (int)].
        # ============================================
        return self.pokemon_Array