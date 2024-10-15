import time
import random
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.box import ROUNDED

console = Console()


class BattleStatsManager:
    def __init__(self):
        self.player1_wins = 0
        self.player2_wins = 0
        self.ties = 0
        self.console = Console()

        self.stats_table = Table(title="Battle Statistics", box=ROUNDED, title_style="yellow", style="dim")
        self.stats_table.add_column("Battle")
        self.stats_table.add_column("Player 1 Pokemon", style="green")
        self.stats_table.add_column("Player 1 Health", justify="center")
        self.stats_table.add_column("Player 1 Power", justify="center", style="green")
        self.stats_table.add_column("Player 2 Pokemon", style="red")
        self.stats_table.add_column("Player 2 Health", justify="center")
        self.stats_table.add_column("Player 2 Power", justify="center", style="red")
        self.stats_table.add_column("Winner", justify="center")

    def set_value_to_stats_table(self, battle_num, player1, player2, winner):
        if winner == "Player 1":
            win_str = Text("Player 1", style="green")
        elif winner == "Player 2":
            win_str = Text("Player 2", style="red")
        else:
            win_str = Text("Tie", style="yellow")

        self.stats_table.add_row(
            str(battle_num + 1),
            player1[0], str(player1[1]), str(player1[2]),
            player2[0], str(player2[1]), str(player2[2]),
            win_str
        )

    def show_stats_table(self):
        # Corrected the function call; assuming `battles` is a method or data
        table = Table(title="Battle Statistics", box=Table.box.ROUNDED)
        table.add_column("Battle Number", justify="center")
        table.add_column("Player 1 Pokémon", justify="center")
        table.add_column("Player 1 Health", justify="center")
        table.add_column("Player 1 Power", justify="center")
        table.add_column("Player 2 Pokémon", justify="center")
        table.add_column("Player 2 Health", justify="center")
        table.add_column("Player 2 Power", justify="center")
        table.add_column("Winner", justify="center")

        # Assuming `self.battles` is the correct place where battle history is stored
        for battle in self.battles:  # Correcting usage here
            table.add_row(
                str(battle.number),
                battle.player1.pokemon.name,
                str(battle.player1.health),
                str(battle.player1.power),
                battle.player2.pokemon.name,
                str(battle.player2.health),
                str(battle.player2.power),
                battle.winner
            )
        console.print(table)

    @property
    def player1_win_count(self) -> int:
        return self.player1_wins
    
    @player1_win_count.setter
    def player1_win_count(self, value):
        if value < 0:
            raise ValueError("Value must not be negative")
        self.player1_wins += value
        
    @property
    def player2_win_count(self) -> int:
        return self.player2_wins
    
    @player2_win_count.setter
    def player2_win_count(self, value):
        if value < 0:
            raise ValueError("Value must not be negative")
        self.player2_wins += value
        
    @property
    def tie_count(self) -> int:
        return self.ties
    
    @tie_count.setter
    def tie_count(self, value):
        if value < 0:
            raise ValueError("Value must not be negative")
        self.ties += value


class DisplayManager:
    def __init__(self):
        self.console = Console()

    # Display the title of the program
    def display_program_info(self) -> None:
        title_panel = Panel(
            Align.center("[bold magenta]Pokemon Battle System[/bold magenta]"),
            box=ROUNDED,
            style="bold green"
        )
        
        info_panel = Panel(
            Align.center(
                "[bold yellow]![/bold yellow] Select 3-4 Pokémon to participate in the battle\n\n"
                "[green]Potion[/green] enhances your Power     [red]Poison[/red] reduces your opponent's Power\n\n"
                "[bold green]Winner:[/bold green]                         [bold red]Loser:[/bold red]\n"
                "[green]Health: [/green]+5%                     [red]Health: [/red]-10%\n"
                "[green]Power: [/green] +5%                     [green]Power:[/green] -3%\n\n"
                "[bold yellow]![/bold yellow] -2% health every battle (fatigue).\n\n"
                "[green]Press Enter to Start[/green]"
            ),
            box=ROUNDED,
            title="Game Info",
            title_align="center",
            style="white"
        )

        self.console.print(title_panel)
        self.console.print(info_panel)

        self.console.input()
        self.console.clear()

    # Display the Pokemon selection screen
    def display_pokemon_selection(self, pokemon_list) -> None:
        table = Table(title="Pokemon Selection", box=ROUNDED, title_style="bold cyan")
        table.add_column("Index", justify="center")
        table.add_column("Pokemon", justify="center", style="green")
        table.add_column("Health", justify="center")
        table.add_column("Power", justify="center")
        table.add_column("Poison", justify="center")
        table.add_column("Potion", justify="center")

        for i, pokemon in enumerate(pokemon_list):
            table.add_row(
                str(i + 1),
                pokemon[0],
                str(pokemon[1]),
                str(pokemon[2]),
                str(pokemon[3]),
                str(pokemon[4])
            )

        self.console.print(Panel(Align.center("[bold magenta]🔥 Pokemon Battle 🔥[/bold magenta]"), box=ROUNDED))
        self.console.print(Align.center(table))
        self.console.print()

    # This is the missing method added to display the selected pokemons of both players
    def display_players_selected_pokemons(self, player1, player2, player1_battle_pokemon, player2_battle_pokemon, count, all_pokemon_is_used, player1_unused, player2_unused) -> None:
        table1 = Table(title="Player 1", box=ROUNDED, title_style="green")
        table2 = Table(title="Player 2", box=ROUNDED, title_style="red")

        # Add columns to both tables
        self._add_columns_to_table(table1)
        self._add_columns_to_table(table2)

        for i in range(len(player1)):
            player1_is_used = Text("Yes", style="green") if player1[i][5] else Text("No", style="red")
            table1.add_row(str(i + 1), player1[i][0], str(player1[i][1]), str(player1[i][2]), str(player1[i][3]), str(player1[i][4]), player1_is_used)

            player2_is_used = Text("Yes", style="green") if player2[i][5] else Text("No", style="red")
            table2.add_row(str(i + 1), player2[i][0], str(player2[i][1]), str(player2[i][2]), str(player2[i][3]), str(player2[i][4]), player2_is_used)

        all_pokemon_used = Text("YES", style="green") if all_pokemon_is_used else Text("NO", style="red")

        self.console.print(Panel("[bold magenta]🔥 Battle Pokemon Selection 🔥[/bold magenta]", box=ROUNDED))
        self.console.print(f"All Pokemon Used?: {all_pokemon_used}")
        self.console.print(f"Player 1 Unused Pokemon: [red]{player1_unused}[/red]")
        self.console.print(f"Player 2 Unused Pokemon: [red]{player2_unused}[/red]")
        self.console.print(Panel(f"{table1}\n{table2}", box=ROUNDED))

        player1_battle_pokemon = f"🔥 {player1_battle_pokemon[0]} 🔥" if player1_battle_pokemon else ""
        player2_battle_pokemon = f"🔥 {player2_battle_pokemon[0]} 🔥" if player2_battle_pokemon else ""

        self.console.print(f"\n[green]Player 1 Pokemon:[/green] {player1_battle_pokemon}")
        self.console.print(f"[red]Player 2 Pokemon:[/red] {player2_battle_pokemon}\n")

    def _add_columns_to_table(self, table):
        table.add_column("Index")
        table.add_column("Pokemon")
        table.add_column("Health")
        table.add_column("Power")
        table.add_column("Poison")
        table.add_column("Potion")
        table.add_column("Used")




class PokemonBattleDisplay:

    def _add_columns_to_table(self, table):
        table.add_column("Index")
        table.add_column("Pokemon")
        table.add_column("Health")
        table.add_column("Power")
        table.add_column("Poison")
        table.add_column("Potion")
        table.add_column("Used")

    # Display a table of all the selected pokemons of both players
    def display_players_selected_pokemons(self, player1, player2, player1_battle_pokemon, player2_battle_pokemon, count, All_pokemon_IsUsed, player1_unused, player2_unused) -> None:
        table1 = Table(title="Player 1", box=ROUNDED, title_style="green")
        table2 = Table(title="Player 2", box=ROUNDED, title_style="red")

        # Add columns to both tables
        self._add_columns_to_table(table1)
        self._add_columns_to_table(table2)

        for i in range(len(player1)):
            player1_isUsed = Text("Yes", style="green") if player1[i][5] else Text("No", style="red")
            table1.add_row(str(i + 1), player1[i][0], str(player1[i][1]), str(player1[i][2]), str(player1[i][3]), str(player1[i][4]), player1_isUsed)

            player2_isUsed = Text("Yes", style="green") if player2[i][5] else Text("No", style="red")
            table2.add_row(str(i + 1), player2[i][0], str(player2[i][1]), str(player2[i][2]), str(player2[i][3]), str(player2[i][4]), player2_isUsed)

        all_Pokemon_Used = Text("YES", style="green") if All_pokemon_IsUsed else Text("NO", style="red")

        self.console.print(Panel("[bold magenta]🔥 Battle Pokemon Selection 🔥[/bold magenta]", box=ROUNDED))
        self.console.print(f"All Pokemon Used?: {all_Pokemon_Used}")
        self.console.print(f"Player 1 Unused Pokemon: [red]{player1_unused}[/red]")
        self.console.print(f"Player 2 Unused Pokemon: [red]{player2_unused}[/red]")
        self.console.print(Panel(f"{table1}\n{table2}", box=ROUNDED))

        player1_battle_pokemon = f"🔥 {player1_battle_pokemon[0]} 🔥" if player1_battle_pokemon else ""
        player2_battle_pokemon = f"🔥 {player2_battle_pokemon[0]} 🔥" if player2_battle_pokemon else ""

        self.console.print(f"\n[green]Player 1 Pokemon:[/green] {player1_battle_pokemon}")
        self.console.print(f"[red]Player 2 Pokemon:[/red] {player2_battle_pokemon}\n")

    # Display Player stats where they can use poison and potions
    def display_battle_winner(self, player_selected, count) -> None:
        table = Table(title=f"Player {count + 1}", box=ROUNDED, title_style="green" if count == 0 else "red")
        table.add_column("Pokemon")
        table.add_column("Health", justify="center")
        table.add_column("Power", justify="center")
        table.add_column("Poison", justify="center")
        table.add_column("Potion", justify="center")

        table.add_row(
            player_selected[0],
            str(player_selected[1]),
            str(player_selected[2]),
            str(player_selected[3]),
            str(player_selected[4])
        )

        self.console.print(Panel("[bold magenta]🔥 Battle Preparation 🔥[/bold magenta]", box=ROUNDED))
        self.console.print(table)
        self.console.print()

    # Display The final stats of both pokemon, including poison and potion effects
    def DisplayMainBattleStats(self, player1_pokemon, player2_pokemon, player1_previousPower, player2_previousPower, player1_powerIncrease, player2_powerIncrease, player1_powerDecrease, player2_powerDecrease, battleNumber: int) -> None:
        table1 = Table(title="Player 1", box=ROUNDED, title_style="green")
        table2 = Table(title="Player 2", box=ROUNDED, title_style="red")

        table1.add_column("Pokemon")
        table1.add_column("Health")
        table1.add_column("Power")

        table2.add_column("Pokemon")
        table2.add_column("Health")
        table2.add_column("Power")

        table1.add_row(player1_pokemon[0], str(player1_pokemon[1]), str(player1_previousPower))
        table2.add_row(player2_pokemon[0], str(player2_pokemon[1]), str(player2_previousPower))

        self.console.print(Panel(f"[bold magenta]🔥 Battle {battleNumber + 1} 🔥[/bold magenta]", box=ROUNDED))
        self.console.print(Panel(f"{table1}\n{table2}", box=ROUNDED))
        self.console.input("[green]Press Enter to begin the battle[/green]")
        self.console.clear()

    # Display the Battle Winner
    def display_battle_winner(self, Winner, power_difference_str, player1_win, player2_win, tie):
        self.console.print(Panel("[bold magenta]🔥 Battle Winner 🔥[/bold magenta]", box=ROUNDED))
        self.console.print(f"[bold]🎉 {Winner} 🎉[/bold]")
        self.console.print(f"Power difference: {power_difference_str}")
        self.console.print(f"Player 1 Wins: [green]{player1_win}[/green], Player 2 Wins: [red]{player2_win}[/red], Ties: [yellow]{tie}[/yellow]")

        self.console.input("[green]Press Enter to continue[/green]")
        self.console.clear()

    # Display details of the Fatigue health Adjustment
    def DisplayFatigueAdjustment(self, player1_pokemon, player2_pokemon, player1_prev_HP, player2_prev_HP):
        table1 = Table(title="Player 1", box=ROUNDED, title_style="green")
        table2 = Table(title="Player 2", box=ROUNDED, title_style="red")

        table1.add_column("Pokemon")
        table1.add_column("Health")

        table2.add_column("Pokemon")
        table2.add_column("Health")

        p1_health_str = f"{player1_prev_HP} -> [red]{player1_pokemon[1]}[/red]"
        p2_health_str = f"{player2_prev_HP} -> [red]{player2_pokemon[1]}[/red]"

        table1.add_row(player1_pokemon[0], p1_health_str)
        table2.add_row(player2_pokemon[0], p2_health_str)

        self.console.print(Panel("[bold magenta]🔥 Pokemon Fatigue Effects 🔥[/bold magenta]", box=ROUNDED))
        self.console.print("[yellow]Due to Battle Fatigue, both Player's Pokemon Health is Reduced by 2%[/yellow]")
        self.console.print(Panel(f"{table1}\n{table2}", box=ROUNDED))

        self.console.input("[green]Press Enter to continue to Pokemon Selection[/green]")
        self.console.clear()



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


class GameManager:
    def __init__(self) -> None:
        # =================================================
        # Stats Manager for handling data across all battles
        # =================================================
        self.stats_manager = BattleStatsManager()
        # ==============================================
        # Pokemon Array
        # Contains the list of the available pokemons
        # ==============================================
        self.pokemon_array = PokemonArray().GetPokemonArray
        
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
        self.battle_winner = ""
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

        def validate_selection(selected, max_limit):
            if len(selected) == 0:
                console.print("[red]No Pokémon selected. Please try again![/red]")
                return True
            if len(selected) > max_limit:
                console.print(f"[red]Selected Pokémon exceeds the limit of {max_limit}. Please try again![/red]")
                return True
            return False

        def process_selection(selected, player_array):
            for item in selected:
                idx = item - 1
                if idx >= len(self.pokemon_array):
                    console.print("[red]Selection is out of range. Please try again![/red]")
                    return True
                if idx in selected_indexes:
                    console.print("[red]Duplicate selection. Please try again![/red]")
                    player_array.clear()
                    return True
                selected_indexes.append(idx)
                player_array.append(self.pokemon_array[idx])
                items_to_remove.append(idx)
            return False

        try:
            if index == 0:
                console.print(f"[yellow]INFO:[/yellow] Select 3-4 Pokémon for battle (e.g., 1 2 3 4)")
                self.player_1_index = list(map(int, input("Player 1, select your Pokémon: ").split()))
                if validate_selection(self.player_1_index, 4):
                    return True
                if process_selection(self.player_1_index, self.player_1_array):
                    return True
            else:
                console.print(f"[yellow]INFO:[/yellow] Select the same number of Pokémon as Player 1.")
                self.player_2_index = list(map(int, input("Player 2, select your Pokémon: ").split()))
                if validate_selection(self.player_2_index, len(self.player_1_index)):
                    return True
                if len(self.player_2_index) < len(self.player_1_index):
                    console.print(f"[red]Player 2 selected fewer Pokémon than Player 1. Please try again![/red]")
                    return True
                if process_selection(self.player_2_index, self.player_2_array):
                    return True

        except ValueError:
            console.print("[red]Invalid input. Please enter numbers only![/red]")
            return True

        for item in sorted(items_to_remove, reverse=True):
            self.pokemon_array.pop(item)
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
    def battle_pokemon_selection(self, index) -> bool:
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
    
    def battle_preparation(self, index) -> bool:
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
            
            power_increase = int(player[2] * percentage)
            player[2] += power_increase
            player[4] -= 1  # Decrease potion count
            
            return player[2], percentage_str

        def __UsePoison(opponent, player) -> int:
            percentage = random.choice([0.50, 0.30, 0.10])
            
            if percentage == 0.50: percentage_str = "50%" 
            elif percentage == 0.30: percentage_str = "30%"
            elif percentage == 0.10: percentage_str = "10%"
            
            power_decrease = int(opponent[2] * percentage)
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
                self.battle_winner = f"{GREEN}Player 1{RESET}"
            elif self.player_1_selected_Pokemon[2] < self.player_2_selected_Pokemon[2]:
                self.battle_winner = f"{RED}Player 2{RESET}"
            else:
                self.battle_winner = "Tie"
                
            self.stats_manager.SetValueToStatsTable(self.battle_number, self.player_1_selected_Pokemon, self.player_2_selected_Pokemon, self.battle_winner)
                      
        return False
    
    def battle_winner(self):
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
            self.player_1_selected_Pokemon[1] += int(self.player_1_previous_health * 0.05)  # Increase Player 1's health by 5%
            self.player_1_selected_Pokemon[2] += int(self.player_1_previous_power * 0.05)   # Increase Player 1's power by 5%
            
            self.player_2_selected_Pokemon[1] -= int(self.player_2_previous_health * 0.10)  # Decrease Player 2's health by 10%
            self.player_2_selected_Pokemon[2] += int(self.player_2_previous_power * 0.03)   # Increase Player 2's power by 3%
            
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
            self.player_2_selected_Pokemon[1] += int(self.player_2_previous_health * 0.05)  # Increase Player 2's health by 5%
            self.player_2_selected_Pokemon[2] += int(self.player_2_previous_power * 0.05)   # Increase Player 2's power by 5%
            
            self.player_1_selected_Pokemon[1] -= int(self.player_1_previous_health * 0.10)  # Decrease Player 1's health by 10%
            self.player_1_selected_Pokemon[2] += int(self.player_1_previous_power * 0.03)   # Increase Player 1's power by 3%
            
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
    def check_if_all_pokemon_is_selected(self):
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
    def end_battle_program(self):
        self.stats_manager.ShowStatsTable()
        
    # =======================================
    # Method for setting Values
    # =======================================
    def set_selected_pokemons_to_null(self):
        self.player_1_selected_Pokemon = []
        self.player_2_selected_Pokemon = []
    
    def set_changed_pokemon_power_to_null(self):
        self.player_1_selected_Pokemon_Power_Increase = []
        self.player_1_selected_Pokemon_Power_Decrease = []
        self.player_2_selected_Pokemon_Power_Increase = []
        self.player_2_selected_Pokemon_Power_Decrease = []
    
    def ResetAllValues(self):
        self.battle_winner = ""
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
    def get_pokemon_info(self) -> list:
        return self.pokemon_array
    
    # return Selected Pokemon Array
    @property
    def get_player_1_selected_pokemon(self) -> list:
        return self.player_1_array
    
    @property
    def get_player_2_selected_pokemon(self) -> list:
        return self.player_2_array
    
    # return selected battle pokemon
    @property
    def get_player_1_battle_pokemon(self) -> list:
        return self.player_1_selected_Pokemon
    
    @property
    def get_player_2_battle_pokemon(self) -> list:
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
    def Get_battle_winner(self) -> str:
        return self.battle_winner
    
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
    def is_all_pokemon_selected(self) -> bool:
        return self.all_pokemon_is_Selected

    @property
    def get_player1_unused_count(self):
        return self.player1_unused

    @property
    def get_player2_unused_count(self):
        return self.player2_unused
    





class Gameplay:
    def __init__(self) -> None:
        # Initialize Managers Class
        self.game_manager = GameManager()
        self.display_manager = DisplayManager()
        
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
            self.all_pokemons_isUsed = self.battle_pokemon_selection()
            if self.all_pokemons_isUsed:
                print("\033c", end="")
                break
            
            self.battle_preparation()
            self.MainBattle()
            self.PostBattleAdjustments()

        self.game_manager.end_battle_program()
        print("Program Ended")
    def PokemonArraySelection(self) -> None:
        # ==============================
        #  Pokemon array selection for
        #  both Player
        # ====================`==========
        
        # Display Title and Program Information
        self.display_manager.display_program_info()
        
        count = 0
        while count != 2:
            try: 
                self.display_manager.display_pokemon_selection(self.game_manager.get_pokemon_info)  
                
                selection_Errors = self.game_manager.PokemonArraySelection(count)
                
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
            
    def battle_pokemon_selection(self) -> bool:
        # =====================================
        # Pokemon Selection for Battle
        # =====================================
        self.game_manager.set_selected_pokemons_to_null()
        self.game_manager.set_changed_pokemon_power_to_null()
        self.game_manager.check_if_all_pokemon_is_selected()

        count = 0
        while count != 2:
            try:
                # Displaying selected Pokemons for both players
                self.display_manager.display_players_selected_pokemons(
                    self.game_manager.get_player_1_selected_pokemon(),
                    self.game_manager.get_player_2_selected_pokemon(),
                    self.game_manager.get_player_1_battle_pokemon(),
                    self.game_manager.get_player_2_battle_pokemon(),
                    count,
                    self.game_manager.is_all_pokemon_selected(),
                    self.game_manager.get_player1_unused_count(),
                    self.game_manager.get_player2_unused_count()
                )
                
                selection_errors, exit_game = self.game_manager.battle_pokemon_selection(count)
                
                # Handle invalid selections
                if selection_errors: 
                    time.sleep(1)
                    self.clear_console()
                    continue

                count += 1
                
                # Exit condition
                if exit_game:
                    return True

                self.clear_console()

            except ValueError:
                print("Invalid Input. Please Try Again!")
                time.sleep(1)
                self.clear_console()
                continue
        
        # After both players have selected their Pokémon
        self.display_manager.display_players_selected_pokemons(
            self.game_manager.get_player_1_selected_pokemon(),
            self.game_manager.get_player_2_selected_pokemon(),
            self.game_manager.get_player_1_battle_pokemon(),
            self.game_manager.get_player_2_battle_pokemon(),
            count,
            self.game_manager.is_all_pokemon_selected(),
            self.game_manager.get_player1_unused_count(),
            self.game_manager.get_player2_unused_count()
        )
        print("{:<43}{:<0}".format("", "Preparing Pokemons"))
        time.sleep(2)
        self.clear_console()

    def battle_preparation(self) -> None:
        # ==================================
        # Battle Preparation
        # ==================================
        count = 0
        while count != 2:
            try:
                # Display battle preparation for each player
                self.display_manager.display_battle_preparation(
                    self.game_manager.get_player_1_battle_pokemon() if count == 0 else self.game_manager.get_player_2_battle_pokemon(),
                    count
                )
                
                selection_errors = self.game_manager.battle_preparation(count)
                
                # Handle input errors
                if selection_errors: 
                    time.sleep(1)
                    self.clear_console()
                    continue    

                count += 1
                self.clear_console()

            except ValueError:
                print("Invalid Input. Please Try Again!")
                time.sleep(1)
                self.clear_console()
                continue
        
        # After preparation is complete
        print("{:<15}{:>0}".format("", "🔥 Entering Battle Stage 🔥\n"))
        time.sleep(1)

    def main_battle(self):
        # Display main battle stats
        self.display_manager.display_main_battle_stats(
            self.game_manager.get_player_1_battle_pokemon(),
            self.game_manager.get_player_2_battle_pokemon(),
            self.game_manager.get_player_1_previous_power(),
            self.game_manager.get_player_2_previous_power(),
            self.game_manager.get_player_1_selected_pokemon_power_increase(),
            self.game_manager.get_player_2_selected_pokemon_power_increase(),
            self.game_manager.get_player_1_selected_pokemon_power_decrease(),
            self.game_manager.get_player_2_selected_pokemon_power_decrease(),
            self.game_manager.get_battle_number()
        )
        
        self.game_manager.set_battle_number(1)

        # Determine and display battle winner
        self.game_manager.battle_winner()
        self.display_manager.display_battle_winner(
            self.game_manager.get_battle_winner(),
            self.game_manager.get_power_difference_str(),
            self.game_manager.player1_win_count(),
            self.game_manager.player2_win_count(),
            self.game_manager.tie_count()
        )

    def post_battle_adjustments(self):
        # Display post-battle stats adjustment
        self.display_manager.display_battle_stats_adjustment(
            self.game_manager.get_battle_winner(),
            self.game_manager.get_player_1_battle_pokemon(),
            self.game_manager.get_player1_prev_hp(),
            self.game_manager.get_player_1_previous_power(),
            self.game_manager.get_player_2_battle_pokemon(),
            self.game_manager.get_player2_prev_hp(),
            self.game_manager.get_player_2_previous_power()
        )

        # Apply fatigue effects
        self.game_manager.fatigue_effects()

        # Display fatigue adjustment for both players
        self.display_manager.display_fatigue_adjustment(
            self.game_manager.get_player_1_battle_pokemon(),
            self.game_manager.get_player_2_battle_pokemon(),
            self.game_manager.get_player1_prev_hp(),
            self.game_manager.get_player2_prev_hp()
        )

        # Reset values for the next battle
        self.game_manager.reset_all_values()

    def clear_console(self):
        print("\033c", end="")

    
        
if __name__ == "__main__":
    Gameplay()