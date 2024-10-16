import PokemonArray as pa
import BattleStatsManager as BSM
import random
import time

class GameManager:
    def __init__(self) -> None:
        # =================================================
        # Stats Manager for handling data across all battles
        # =================================================
        self.stats_manager = BSM.BattleStatsManager()
        # ==============================================
        # Pokemon Array
        # Contains the list of the available pokemons
        # ==============================================
        pokemonArray = pa.PokemonArray()
        self.pokemon_array = list(pokemonArray.GetPokemonArray)
        
        # ==============================================
        # Player Pokemon Selection Array
        # Contains the selected pokemons and Index 
        # of both players
        # ==============================================
        self.player_1_array = []
        self.player_2_array = []
        self.player_1_index = []
        self.player_2_index = []
        self.player_1_selected_Pokemon = []
        self.player_2_selected_Pokemon = []
        
        # Contains: 
        # Index 0 = Power Increase/Decrease
        # Index 1 = Percentage of Increase/Decrease
        self.player_1_selected_Pokemon_Power_Increase = []
        self.player_1_selected_Pokemon_Power_Decrease = []
        self.player_2_selected_Pokemon_Power_Increase = []
        self.player_2_selected_Pokemon_Power_Decrease = []
        
        # ==================================
        # Battle Number counter and Winner
        # ==================================
        self.battle_number = 0
        self.Battle_Winner = ""
        self.player1_unused = 0
        self.player2_unused = 0
        self.all_pokemon_is_Selected = False
        
        # =======================================
        # Stats holder for previous values for
        # health and power after poison and potion
        # are applied
        # =======================================
        self.player_1_previous_health = None
        self.player_2_previous_health = None
        self.player_1_previous_power = None
        self.player_2_previous_power = None
     
    # ==============================================
    # Pokemon Selection Method
    # Handles the selection and removing pokemons
    # in the pokemon selection table
    # ==============================================       
    def PokemonArraySelection(self, index) -> bool:
        selected_indexes = []
        items_to_remove = []
        
        GREEN = "\033[32m"
        RED = "\033[31m"
        YELLOW = "\033[33m"
        RESET = "\033[0m"

        def validate_selection(selected, max_limit):
            if len(selected) == 0:
                print("No Selected Pokemon. Please Try Again!")
                return True
            if len(selected) > max_limit:
                print(f"Selected Pokemons is more than {max_limit}. Please Try Again!")
                return True
            return False

        def process_selection(selected, player_array):
            for item in selected:
                idx = item - 1
                if idx >= len(self.pokemon_array):
                    print("Number is Out of Range. Please Try Again!")
                    return True
                if idx in selected_indexes:
                    print("Duplicate Selection. Please Try Again!")
                    player_array.clear()
                    return True
                selected_indexes.append(idx)
                player_array.append(self.pokemon_array[idx])
                items_to_remove.append(idx)
            return False

        if index == 0:
            print(f"Select a Maximum of 4 Pokemons\n{YELLOW}INFO:{RESET} Select 3-4 Pokemons to use for battle (Ex. Input: 1 2 3 4)\n")
            self.player_1_index = list(map(int, input(f"{GREEN}Player 1{RESET} select sa Pokemon: ").split(" ")))

            if validate_selection(self.player_1_index, 4):
                return True
            if process_selection(self.player_1_index, self.player_1_array):
                return True
        else:
            print(f"Please Select {len(self.player_1_index)} Pokemons\n{YELLOW}INFO:{RESET} Select 3-4 Pokemons to use for battle (Ex. Input: 1 2 3 4)\n")
            self.player_2_index = list(map(int, input(f"{RED}Player 2{RESET} selects a Pokemon: ").split(" ")))

            if validate_selection(self.player_2_index, len(self.player_1_index)):
                return True
            if len(self.player_2_index) < len(self.player_1_index):
                print(f"Selected Pokemons is less than {len(self.player_1_index)}. Please Try Again!")
                return True
            if process_selection(self.player_2_index, self.player_2_array):
                return True

        for item in sorted(items_to_remove, reverse=True):
            self.pokemon_array.pop(item)       
        return False

    # ===========================================
    # Selection of pokemon that will be use for
    # Battle
    # ==========================================
    def BattlePokemonSelection(self, index) -> bool:
        GREEN = "\033[32m"
        RED = "\033[31m"
        YELLOW = "\033[33m"
        RESET = "\033[0m"
        COLOR = GREEN if index == 0 else RED
        
        if self.all_pokemon_is_Selected and index == 0:
            print(f"{YELLOW}All Pokemon is Used. Battle Can be Ended Now{RESET}")
            print(f"Enter {RED}EXIT{RESET} to end Battle or {GREEN}Press Enter Key{RESET} to Continue Battle")
            exit_input = input("> ").lower()
            
            if exit_input == "exit":
                return False, True
            elif exit_input != "exit" and exit_input != "":
                print("Wrong Input. Try Again")
                return True, False
                
        
        print("Select 1 pokemon to use for battle\n")        
        player_selection = int(input(f"{COLOR}Player {index + 1}{RESET} Select a Pokemon for Battle: "))
        
        player_array = self.player_1_array if index == 0 else self.player_2_array
        selected_pokemon_attr = 'player_1_selected_Pokemon' if index == 0 else 'player_2_selected_Pokemon'

        if player_selection <= 0:
            print(f"Selected Index is less than or equal to zero. Please try again.")
            return True, False
        elif player_selection > len(player_array):
            print(f"Selected Index is greater than {len(player_array)}. Please try again.")
            return True, False
        else:
            setattr(self, selected_pokemon_attr, player_array[player_selection - 1])
            selected_pokemon = getattr(self, selected_pokemon_attr)
            if selected_pokemon[1] <= 0:
                print("Health is Zero. Cannot Chose Pokemon")
                return True, False
            
            selected_pokemon[5] = True

            return False, False
    
    def BattlePreparation(self, index) -> bool:
        player_selected = self.player_1_selected_Pokemon if index == 0 else self.player_2_selected_Pokemon
        
        player_actions = {"use_potion": False, "use_poison": False}
        
        GREEN = "\033[32m"
        RED = "\033[31m"
        YELLOW = "\033[33m"
        RESET = "\033[0m"
        
         # Helper methods for potion and poison effects
        def __UsePotion(player) -> int:
            percentage = random.choice([0.50, 0.30, 0.10])
            
            if percentage == 0.50: percentage_str = "50%" 
            elif percentage == 0.30: percentage_str = "30%"
            elif percentage == 0.10: percentage_str = "10%" 
            
            power_increase = round(player[2] * percentage)
            player[2] += power_increase
            player[4] -= 1  # Decrease potion count
            
            return player[2], percentage_str

        def __UsePoison(opponent, player) -> int:
            percentage = random.choice([0.50, 0.30, 0.10])
            
            if percentage == 0.50: percentage_str = "50%" 
            elif percentage == 0.30: percentage_str = "30%"
            elif percentage == 0.10: percentage_str = "10%"
            
            power_decrease = round(opponent[2] * percentage)
            opponent_newPower = max((opponent[2] - power_decrease), 1)  # Minimum power of 1
            player[3] -= 1  # Decrease poison count
               
            return opponent_newPower, percentage_str
        
        if player_selected[3] == 0 and player_selected[4] == 0:
            print("No available Poison and Potions")
            input(f"Press {GREEN}Enter{RESET} to continue\n")
            
            if index == 0:
                self.player_1_actions = player_actions
                self.player_1_previous_power = self.player_1_selected_Pokemon[2]           
            else:
                self.player_2_actions = player_actions
                self.player_2_previous_power = self.player_2_selected_Pokemon[2]
            return
        
        # Poison action prompt refactored
        if player_selected[3] > 0:
            print(f"{YELLOW}INFO:{RESET} {RED}Poison{RESET} Reduce Opponents Power by a Random Percentage (10%, 30%, 50%)\n")
            use_poison = input(f"Use {RED}poison{RESET} on the opponent? [{GREEN}Y{RESET}/{RED}N{RESET}]: ").strip().lower()
            if use_poison == "y":
                player_actions["use_poison"] = True
                print(f"{RED}Poison{RESET} will be applied to the opponent\n")
                time.sleep(1)
            elif use_poison == "n":
                print(f"No {RED}Poison{RESET} used\n")
                time.sleep(1)
            else:
                print("Invalid input. Please try again.")
                return True
        else:
            print(f"No available {RED}Poison{RESET}")
            input(f"Press {GREEN}Enter{RESET} to continue\n")
        
        # Potion action prompt refactored
        if player_selected[4] > 0:
            print(f"{YELLOW}INFO:{RESET} {GREEN}Potion{RESET} Increase Your Pokemon Power by a Random Percentage (10%, 30%, 50%)\n")
            use_potion = input(f"Use {GREEN}Potion{RESET} to increase power? [{GREEN}Y{RESET}/{RED}N{RESET}]: ").strip().lower()
            if use_potion == "y":
                player_actions["use_potion"] = True
                print(f"{GREEN}Potion{RESET} will be applied\n")
                time.sleep(1)
            elif use_potion == "n":
                print(f"No {GREEN}Potion{RESET} used\n")
                time.sleep(1)
            else:
                print("Invalid input. Please try again.")
                return True
        else:
            print(f"No available {GREEN}Potion{RESET}")
            input(f"Press {GREEN}Enter{RESET} to continue\n")
            
        if index == 0:
            self.player_1_actions = player_actions
        else:
            self.player_2_actions = player_actions
            
        if hasattr(self, "player_1_actions") and hasattr(self, "player_2_actions"):
            self.player_1_previous_power = self.player_1_selected_Pokemon[2]
            self.player_2_previous_power = self.player_2_selected_Pokemon[2]
            
            power_Decrease_player1 = 0
            power_Decrease_player2 = 0
            
            # Player 1|2 Potions Actions
            if self.player_1_actions["use_potion"]:
                power_Increase, perct = __UsePotion(self.player_1_selected_Pokemon)
                self.player_1_selected_Pokemon_Power_Increase.append(power_Increase)
                self.player_1_selected_Pokemon_Power_Increase.append(perct)
                
            if self.player_2_actions["use_potion"]:
                power_Increase, perct = __UsePotion(self.player_2_selected_Pokemon)
                self.player_2_selected_Pokemon_Power_Increase.append(power_Increase)
                self.player_2_selected_Pokemon_Power_Increase.append(perct) 
   
            # Player 1|2 Poison Action
            if self.player_1_actions["use_poison"]:
                power_Decrease_player2, perct = __UsePoison(self.player_2_selected_Pokemon, self.player_1_selected_Pokemon)
                self.player_2_selected_Pokemon_Power_Decrease.append(power_Decrease_player2)
                self.player_2_selected_Pokemon_Power_Decrease.append(perct)
                
            if self.player_2_actions["use_poison"]:
                power_Decrease_player1, perct = __UsePoison(self.player_1_selected_Pokemon, self.player_2_selected_Pokemon)
                self.player_1_selected_Pokemon_Power_Decrease.append(power_Decrease_player1)
                self.player_1_selected_Pokemon_Power_Decrease.append(perct)

            if power_Decrease_player1 != 0:
                self.player_1_selected_Pokemon[2] = power_Decrease_player1   
            if power_Decrease_player2 != 0:
                self.player_2_selected_Pokemon[2] = power_Decrease_player2
                
            # Clear actions after applying to both players
            del self.player_1_actions
            del self.player_2_actions
            
            if self.player_1_selected_Pokemon[2] > self.player_2_selected_Pokemon[2]:
                self.Battle_Winner = f"{GREEN}Player 1{RESET}"
            elif self.player_1_selected_Pokemon[2] < self.player_2_selected_Pokemon[2]:
                self.Battle_Winner = f"{RED}Player 2{RESET}"
            else:
                self.Battle_Winner = "Tie"
                
            self.stats_manager.SetValueToStatsTable(self.battle_number, self.player_1_selected_Pokemon, self.player_2_selected_Pokemon, self.Battle_Winner)
                      
        return False
    
    def BattleWinner(self):
        GREEN = "\033[32m"
        RED = "\033[31m"
        RESET = "\033[0m"
        
        # If Player 1 wins
        if self.player_1_selected_Pokemon[2] > self.player_2_selected_Pokemon[2]:
            self.stats_manager.GetPlayer1_win_count = 1

            # Power difference string
            self.power_difference_str = f"{GREEN}{self.player_1_selected_Pokemon[2]}{RESET} > {RED}{self.player_2_selected_Pokemon[2]}{RESET}"

            # Save previous health and power for both players
            self.player_1_previous_health = self.player_1_selected_Pokemon[1]
            self.player_1_selected_Pokemon[2] = self.player_1_previous_power
            
            self.player_2_previous_health = self.player_2_selected_Pokemon[1]
            self.player_2_selected_Pokemon[2] = self.player_2_previous_power

            # Apply the correct changes when Player 1 wins
            self.player_1_selected_Pokemon[1] += round(self.player_1_previous_health * 0.05)  # Increase Player 1's health by 5%
            self.player_1_selected_Pokemon[2] += round(self.player_1_previous_power * 0.05)   # Increase Player 1's power by 5%
            
            self.player_2_selected_Pokemon[1] -= round(self.player_2_previous_health * 0.10)  # Decrease Player 2's health by 10%
            self.player_2_selected_Pokemon[2] += round(self.player_2_previous_power * 0.03)   # Increase Player 2's power by 3%
            
            if self.player_2_selected_Pokemon[1] <= 0:
                self.player_2_selected_Pokemon[1] = 0

        # If Player 2 wins
        elif self.player_1_selected_Pokemon[2] < self.player_2_selected_Pokemon[2]:
            self.stats_manager.GetPlayer2_win_count = 1

            # Power difference string
            self.power_difference_str = f"{RED}{self.player_1_selected_Pokemon[2]}{RESET} < {GREEN}{self.player_2_selected_Pokemon[2]}{RESET}"

            # Save previous health and power for both players
            self.player_1_previous_health = self.player_1_selected_Pokemon[1]
            self.player_1_selected_Pokemon[2] = self.player_1_previous_power 

            self.player_2_previous_health = self.player_2_selected_Pokemon[1]
            self.player_2_selected_Pokemon[2] = self.player_2_previous_power

            # Apply the correct changes when Player 2 wins
            self.player_2_selected_Pokemon[1] += round(self.player_2_previous_health * 0.05)  # Increase Player 2's health by 5%
            self.player_2_selected_Pokemon[2] += round(self.player_2_previous_power * 0.05)   # Increase Player 2's power by 5%
            
            self.player_1_selected_Pokemon[1] -= round(self.player_1_previous_health * 0.10)  # Decrease Player 1's health by 10%
            self.player_1_selected_Pokemon[2] += round(self.player_1_previous_power * 0.03)   # Increase Player 1's power by 3%
            
            if self.player_1_selected_Pokemon[1] <= 0:
                self.player_1_selected_Pokemon[1] = 0

        # If it's a tie
        else:
            self.stats_manager.GetTie_count = 1

            self.power_difference_str = f"{self.player_1_selected_Pokemon[2]} == {self.player_2_selected_Pokemon[2]}"
            
            # Reset power to previous values (no changes in a tie)
            self.player_1_selected_Pokemon[2] = self.player_1_previous_power
            self.player_2_selected_Pokemon[2] = self.player_2_previous_power
        
        

    # ====================================
    # Method that handle health adjustment
    # After every battle
    # ====================================
    def FatigueEffects(self):
        self.player_1_previous_health = self.player_1_selected_Pokemon[1]
        self.player_2_previous_health = self.player_2_selected_Pokemon[1]
        
        self.player_1_selected_Pokemon[1] = self.player_1_selected_Pokemon[1] - round(self.player_1_selected_Pokemon[1] * 0.02)
        self.player_2_selected_Pokemon[1] = self.player_2_selected_Pokemon[1] - round(self.player_2_selected_Pokemon[1] * 0.02)
        
    # ==========================================    
    # Check if pokemons is used, if all is used
    # the battle can end or continue base from
    # players decision
    # =========================================
    def CheckIfAllPokemonIsSelected(self):
        player1_not_selected = 0
        player2_not_selected = 0
        all_selected_count = 0
        
        for i in self.player_1_array:
            if i[-1] == False:
                player1_not_selected += 1
            elif i[-1] == True:
                all_selected_count += 1
                
        for i in self.player_2_array:
            if i[-1] == False:
                player2_not_selected += 1
            elif i[-1] == True:
                all_selected_count += 1
                
        if len(self.player_1_array) + len(self.player_2_array) == all_selected_count:
            self.all_pokemon_is_Selected = True
        
        self.player1_unused = player1_not_selected
        self.player2_unused = player2_not_selected
    
    # Display The battle Statistic in the end of
    # the program
    def EndBattleProgram(self):
        self.stats_manager.ShowStatsTable()
        
    # =======================================
    # Method for setting Values
    # =======================================
    def SetSelectedPokemonsToNull(self):
        self.player_1_selected_Pokemon = []
        self.player_2_selected_Pokemon = []
    
    def SetChangedPokemonPowerToNull(self):
        self.player_1_selected_Pokemon_Power_Increase = []
        self.player_1_selected_Pokemon_Power_Decrease = []
        self.player_2_selected_Pokemon_Power_Increase = []
        self.player_2_selected_Pokemon_Power_Decrease = []
    
    def ResetAllValues(self):
        self.Battle_Winner = ""
        self.player1_unused = 0
        self.player2_unused = 0
        self.all_pokemon_is_Selected = False
        self.player_1_previous_health = None
        self.player_2_previous_health = None
        self.player_1_previous_power = None
        self.player_2_previous_power = None

    # ==================================
    # Methods for Returning Values
    # ==================================
    @property
    def GetPokemonInfo(self) -> list:
        return self.pokemon_array
    
    # return Selected Pokemon Array
    @property
    def GetPlayer_1_SelectedPokemon(self) -> list:
        return self.player_1_array
    
    @property
    def GetPlayer_2_SelectedPokemon(self) -> list:
        return self.player_2_array
    
    # return selected battle pokemon
    @property
    def GetPlayer_1_BattlePokemon(self) -> list:
        return self.player_1_selected_Pokemon
    
    @property
    def GetPlayer_2_BattlePokemon(self) -> list:
        return self.player_2_selected_Pokemon
    
    # return previous power after poison and poitons
    # are applied
    @property
    def GetPlayer_1_PreviousPower(self) -> int:
        return self.player_1_previous_power
    
    @property
    def GetPlayer_2_PreviousPower(self) -> int:
        return self.player_2_previous_power
    
    # Return power increase
    @property
    def GetPlayer_1_Selected_Pokemon_Power_Increase(self) -> list:
        return self.player_1_selected_Pokemon_Power_Increase
    
    @property
    def GetPlayer_2_Selected_Pokemon_Power_Increase(self) -> list:
        return self.player_2_selected_Pokemon_Power_Increase
    
    # Return power Decrease
    @property
    def GetPlayer_1_Selected_Pokemon_Power_decrease(self) -> list:
        return self.player_1_selected_Pokemon_Power_Decrease
    
    @property
    def GetPlayer_2_Selected_Pokemon_Power_decrease(self) -> list:
        return self.player_2_selected_Pokemon_Power_Decrease
    
    # Return Battle Number
    @property
    def GetBattle_Number(self) -> int:
        return self.battle_number
    
    # Increase Battle Number
    @GetBattle_Number.setter
    def SetBattle_Number(self, value) -> None:
        if value < 0:
            raise ValueError("Value cannot be negative")
        self.battle_number += value
    
    # Get the winner of the battle
    @property
    def Get_Battle_Winner(self) -> str:
        return self.Battle_Winner
    
    # Get the str format of power difference between
    # the two players
    @property
    def Get_Power_Difference_str(self) -> str:
        return self.power_difference_str
    
    # Get Win Counts and Ties
    @property
    def Player1_win_count(self):
        return self.stats_manager.GetPlayer1_win_count
    
    @property
    def Player2_win_count(self):
        return self.stats_manager.GetPlayer2_win_count
    
    @property
    def Tie_count(self):
        return self.stats_manager.GetTie_count
    
    # Get Previous player HPs
    @property
    def GetPlayer1_prev_HP(self):
        return self.player_1_previous_health
    
    @property
    def GetPlayer2_prev_HP(self):
        return self.player_2_previous_health
    
    # Get bool if all pokemons is selected
    @property
    def Is_all_pokemone_selected(self) -> bool:
        return self.all_pokemon_is_Selected

    @property
    def GetPlayer1_unused_count(self):
        return self.player1_unused

    @property
    def GetPlayer2_unused_count(self):
        return self.player2_unused
    