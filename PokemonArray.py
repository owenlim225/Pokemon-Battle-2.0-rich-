import random

class PokemonArray:
    def __init__(self) -> None:  
        self.pokemon_Array = [
            # [Name, Health, Power, Poisons, Potions, isUsed]
            ["Pikachu", 100, 55, 0, 0, False],
            ["Charmander", 120, 60, 0, 0, False],
            ["Bulbasaur", 90, 50, 0, 0, False],
            ["Squirtle", 110, 65, 0, 0, False],
            ["Jigglypuff", 80, 45, 0, 0, False],
            ["Eevee", 95, 70, 0, 0, False],
            ["Snorlax", 150, 100, 0, 0, False],
            ["Gengar", 85, 75, 0, 0, False],
            ["Machamp", 130, 80, 0, 0, False],
            ["Mewtwo", 140, 90, 0, 0, False]
        ]
        
        self.__RandomeValueGenerator()

    def __RandomeValueGenerator(self) -> None:
        # Poison and Potion
        for i in range(len(self.pokemon_Array)):
            randomNum1 = random.randint(1, 6)
            randomNum2 = random.randint(1, 6)
            
            self.pokemon_Array[i][3] = randomNum1
            self.pokemon_Array[i][4] = randomNum2
            
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