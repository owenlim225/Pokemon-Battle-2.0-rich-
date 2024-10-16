# # Uncomment this import if there is missing modules 

# import packages
# packages.InitializePackages()

import GameManager as GM
import DisplayManager as DP
import time

class Gameplay:
    def __init__(self) -> None:
        # Initialize Managers Class
        self.game_Manager = GM.GameManager()
        self.display_Manager = DP.DisplayManager()
        
        # Battle Variable Flag
        self.all_pokemons_isUsed = False
     
        # Start the program
        self.main()
        
    # =============================   
    # Main Game Method    
    # =============================
    def main(self) -> None:
        # ======================================
        # Pokemon Group Selection for player 1 and 2
        # ======================================
        self.PokemonArraySelection()
        
        # =====================================
        # Pokemon Battle Loop
        # =====================================
        while not self.all_pokemons_isUsed:
            # Selection of pokemon that will be
            # use for battle
            self.all_pokemons_isUsed = self.Battle_Pokemon_Selection()
            if self.all_pokemons_isUsed:
                print("\033c", end="")
                break
            
            self.BattlePreparation()
            self.MainBattle()
            self.PostBattleAdjustments()

        self.game_Manager.EndBattleProgram()
        print("Program Ended")
    def PokemonArraySelection(self) -> None:
        # ==============================
        #  Pokemon array selection for
        #  both Player
        # ==============================
        
        # Display Title and Program Information
        self.display_Manager.DisplayProgramInfo()
        
        count = 0
        while count != 2:
            try: 
                self.display_Manager.DisplayPokemonSelection(self.game_Manager.GetPokemonInfo)  
                
                selection_Errors = self.game_Manager.PokemonArraySelection(count)
                
                # Check IndexError for user input selections
                if selection_Errors: 
                    time.sleep(1)
                    print("\033c", end="")
                    continue
                count += 1
                
                # Clear the Console for better UX
                print("\033c", end="")
            except ValueError:
                print("Invald Input. Please Try Again!")
                time.sleep(1)
                print("\033c", end="")
                continue
            
    def Battle_Pokemon_Selection(self) -> bool:        
        # =====================================
        # Pokemon Selection for Battle
        # =====================================
        self.game_Manager.SetSelectedPokemonsToNull()
        self.game_Manager.SetChangedPokemonPowerToNull() 
        self.game_Manager.CheckIfAllPokemonIsSelected()
        
        count = 0
        while count != 2:
            try:
                self.display_Manager.DisplayPlayersSelectedPokemons(
                        self.game_Manager.GetPlayer_1_SelectedPokemon,
                        self.game_Manager.GetPlayer_2_SelectedPokemon,
                        self.game_Manager.GetPlayer_1_BattlePokemon,
                        self.game_Manager.GetPlayer_2_BattlePokemon,
                        count,
                        self.game_Manager.Is_all_pokemone_selected,
                        self.game_Manager.GetPlayer1_unused_count,
                        self.game_Manager.GetPlayer2_unused_count)
                
                selection_Errors, exit = self.game_Manager.BattlePokemonSelection(count)
                
                # Check IndexError for user input selections
                if selection_Errors: 
                    time.sleep(1)
                    print("\033c", end="")
                    continue
                
                count += 1
                
                if exit:
                    return True
                       
                # Clear the Console for better UX
                print("\033c", end="")
                
            except ValueError:
                print("Invald Input. Please Try Again!")
                time.sleep(1)
                print("\033c", end="")
                continue
        else:
            self.display_Manager.DisplayPlayersSelectedPokemons(
                    self.game_Manager.GetPlayer_1_SelectedPokemon,
                    self.game_Manager.GetPlayer_2_SelectedPokemon,
                    self.game_Manager.GetPlayer_1_BattlePokemon,
                    self.game_Manager.GetPlayer_2_BattlePokemon,
                    count,
                    self.game_Manager.Is_all_pokemone_selected,
                    self.game_Manager.GetPlayer1_unused_count,
                    self.game_Manager.GetPlayer2_unused_count)
            print("{:<43}{:<0}".format("", "Preparing Pokemons"))
            time.sleep(2)   
            print("\033c", end="")
            
    def BattlePreparation(self) -> None:
        # ==================================
        # Battle Preparation where the players
        # can decide whether they can use
        # poison or postion
        # ==================================
        count = 0
        while count != 2:
            try:
                if count == 0:
                    self.display_Manager.DisplayBattlePreparation(
                        self.game_Manager.GetPlayer_1_BattlePokemon,
                        count)
                elif count == 1:
                    self.display_Manager.DisplayBattlePreparation(
                        self.game_Manager.GetPlayer_2_BattlePokemon,
                        count)
                    
                selection_Errors = self.game_Manager.BattlePreparation(count)
                
                # Check IndexError for user input selections
                if selection_Errors: 
                    time.sleep(1)
                    print("\033c", end="")
                    continue    
                count += 1
                
                # Clear the Console for better UX
                print("\033c", end="")
                
            except ValueError:
                print("Invald Input. Please Try Again!")
                time.sleep(1)
                print("\033c", end="")
                continue
        else:
            print("{:<15}{:>0}".format(
                "",
                "🔥 Entering Battle Stage 🔥\n"
            ))
            time.sleep(1)
            
    def MainBattle(self):
        self.display_Manager.DisplayMainBattleStats(
            self.game_Manager.GetPlayer_1_BattlePokemon,
            self.game_Manager.GetPlayer_2_BattlePokemon,
            self.game_Manager.GetPlayer_1_PreviousPower,
            self.game_Manager.GetPlayer_2_PreviousPower,
            self.game_Manager.GetPlayer_1_Selected_Pokemon_Power_Increase,
            self.game_Manager.GetPlayer_2_Selected_Pokemon_Power_Increase,
            self.game_Manager.GetPlayer_1_Selected_Pokemon_Power_decrease,
            self.game_Manager.GetPlayer_2_Selected_Pokemon_Power_decrease,
            self.game_Manager.GetBattle_Number
        )
        self.game_Manager.SetBattle_Number = 1

        self.game_Manager.BattleWinner()

        # Displaying the winner using the newly added DisplayBattleWinner method
        self.display_Manager.DisplayBattleWinner(
            self.game_Manager.Get_Battle_Winner,
            self.game_Manager.Get_Power_Difference_str,
            self.game_Manager.Player1_win_count,
            self.game_Manager.Player2_win_count,
            self.game_Manager.Tie_count
        )

        
    def PostBattleAdjustments(self):
        # Display battle stats adjustment
        self.display_Manager.DisplayBattleStatsAdjustment(
            self.game_Manager.Get_Battle_Winner,
            self.game_Manager.GetPlayer_1_BattlePokemon,
            self.game_Manager.GetPlayer1_prev_HP,
            self.game_Manager.GetPlayer_1_PreviousPower,
            self.game_Manager.GetPlayer_2_BattlePokemon,
            self.game_Manager.GetPlayer2_prev_HP,
            self.game_Manager.GetPlayer_2_PreviousPower
        )

        # Apply and display fatigue effects
        self.game_Manager.FatigueEffects()
        self.display_Manager.DisplayFatigueAdjustment(
            self.game_Manager.GetPlayer_1_BattlePokemon,
            self.game_Manager.GetPlayer_2_BattlePokemon,
            self.game_Manager.GetPlayer1_prev_HP,
            self.game_Manager.GetPlayer2_prev_HP
        )

        # Reset values for the next battle
        self.game_Manager.ResetAllValues()


    
        
if __name__ == "__main__":
    Gameplay()