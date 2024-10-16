from rich.console import Console
from rich.table import Table
from rich import box

class DisplayManager:
    console = Console()

    # ==================================
    # Display the title of the program
    # ==================================
    def DisplayProgramInfo(self) -> None:
        GREEN = "\033[32m"
        RED = "\033[31m"
        YELLOW = "\033[33m"
        RESET = "\033[0m"
        print("{:>20}{:>0}".format("", "🔥 Pokemon Battle 🔥\n"))
        print(f"{YELLOW}INFO:{RESET} Select 3-4 pokemon to be used for battle")
        print(f"💉 {GREEN}Potion{RESET} is used to increase your Power")    
        print(f"💀 {RED}Poison{RESET} is used to decrease opponents' Power\n")
        print("⚠ Potion and Poison affect only 1 battle")
        print("⚠ New battle resets power to its base power")
        print("⚠ Base power changes depending on whether you're the winner or loser\n")
        print(f"🎉 {GREEN}Winner:{RESET}")
        print(f"Health {GREEN}increase{RESET} by 5%")
        print(f"Power {GREEN}increase{RESET} by 5%\n")
        print(f"💔 {RED}Loser:{RESET}")
        print(f"Health {RED}decrease{RESET} by 10%")
        print(f"Power {GREEN}increase{RESET} by 3%\n")
        print("⚠ Every Battle both Player health is reduced by 2% due to fatigue\n")  
        print(f"{YELLOW}⚠ How To End Battle ⚠{RESET}")
        print("- To end the battle, all Pokémon for both players must be used\n")
        
        input(f"Press {GREEN}Enter{RESET} To Start")
        print("\033c", end="")

    # ====================================
    # Display a table of all the available
    # Pokemons for the player to select
    # ====================================   
    def DisplayPokemonSelection(self, pokemon_list) -> None:
        table = Table(title="🔥 Pokemon Selection 🔥", box=box.MINIMAL)
        table.add_column("Index", justify="center")
        table.add_column("Pokemon", justify="center")
        table.add_column("Health", justify="center")
        table.add_column("Power", justify="center")
        table.add_column("Poison", justify="center")
        table.add_column("Potion", justify="center")

        for i, pokemon in enumerate(pokemon_list, start=1):
            table.add_row(
                str(i),
                pokemon[0],  # Pokemon name
                str(pokemon[1]),  # Health
                str(pokemon[2]),  # Power
                str(pokemon[3]),  # Poison
                str(pokemon[4])   # Potion
            )

        self.console.print(table)

    

    def DisplayMainBattleStats(self,
                               player1_pokemon,
                               player2_pokemon,
                               player1_previousPower,
                               player2_previousPower,
                               player1_powerIncrease: list,
                               player2_powerIncrease: list,
                               player1_powerDecrease: list,
                               player2_powerDecrease: list,
                               battleNumber: int) -> None:
        
        # Helper function to format power changes
        def format_power_change(previous_power, final_power):
            if final_power > previous_power:
                return f"[green]{previous_power} -> {final_power}[/green]"
            elif final_power < previous_power:
                return f"[red]{previous_power} -> {final_power}[/red]"
            else:
                return f"{previous_power} -> {final_power}"

        # Player 1's Table
        table1 = Table(title=f"Player 1 - {player1_pokemon[0]}", box=box.SQUARE)
        table1.add_column("Stat", justify="center")
        table1.add_column("Value", justify="center")
        table1.add_row("Health", str(player1_pokemon[1]))
        table1.add_row("Power", format_power_change(player1_previousPower, player1_pokemon[2]))
        
        # Player 2's Table
        table2 = Table(title=f"Player 2 - {player2_pokemon[0]}", box=box.SQUARE)
        table2.add_column("Stat", justify="center")
        table2.add_column("Value", justify="center")
        table2.add_row("Health", str(player2_pokemon[1]))
        table2.add_row("Power", format_power_change(player2_previousPower, player2_pokemon[2]))

        # Display both tables
        self.console.print(f"\n🔥 Battle {battleNumber + 1} 🔥\n")
        self.console.print(table1)
        self.console.print(table2)

        # Show power increase/decrease details
        self.console.print(f"\n[green]Player 1 Power Increase:[/green] {player1_powerIncrease}")
        self.console.print(f"[red]Player 1 Power Decrease:[/red] {player1_powerDecrease}")
        self.console.print(f"\n[green]Player 2 Power Increase:[/green] {player2_powerIncrease}")
        self.console.print(f"[red]Player 2 Power Decrease:[/red] {player2_powerDecrease}\n")

        input("Press Enter to continue...")
        print("\033c", end="")  # Clears the console for the next step



    def DisplayBattleWinner(self, winner, power_difference_str, player1_win_count, player2_win_count, tie_count) -> None:
        # Display the battle winner
        table = Table(title="Battle Winner", box=box.SQUARE)
        table.add_column("Winner", justify="center")
        table.add_row(winner)

        self.console.print(table)

        # Show the power difference
        self.console.print(f"[yellow]Power Difference: [/yellow]{power_difference_str}\n")

        # Show current standings
        standings_table = Table(title="Current Standings", box=box.SIMPLE)
        standings_table.add_column("Player", justify="center")
        standings_table.add_column("Wins", justify="center")
        standings_table.add_column("Ties", justify="center")

        standings_table.add_row(f"[green]Player 1[/green]", str(player1_win_count), str(tie_count))
        standings_table.add_row(f"[red]Player 2[/red]", str(player2_win_count), str(tie_count))

        # Display the current win/tie counts for both players
        self.console.print(standings_table)

        input("Press Enter to continue...")
        print("\033c", end="")  # Clear the screen




    def DisplayBattleStatsAdjustment(self, winner, player1_pokemon, player1_prev_HP, player1_prev_Power,
                                     player2_pokemon, player2_prev_HP, player2_prev_Power) -> None:
        # Helper function to create HP and Power change strings
        def create_stat_change_str(previous_stat, new_stat):
            if new_stat > previous_stat:
                return f"[green]{previous_stat} -> {new_stat}[/green]"
            elif new_stat < previous_stat:
                return f"[red]{previous_stat} -> {new_stat}[/red]"
            else:
                return f"{previous_stat} -> {new_stat}"

        # Player 1's stat changes
        player1_HP_str = create_stat_change_str(player1_prev_HP, player1_pokemon[1])
        player1_Power_str = create_stat_change_str(player1_prev_Power, player1_pokemon[2])

        # Player 2's stat changes
        player2_HP_str = create_stat_change_str(player2_prev_HP, player2_pokemon[1])
        player2_Power_str = create_stat_change_str(player2_prev_Power, player2_pokemon[2])

        # Winner and loser labels
        if winner == "Player 1":
            winner_label = "[green]Player 1 Wins[/green]"
            loser_label = "[red]Player 2 Loses[/red]"
        elif winner == "Player 2":
            winner_label = "[red]Player 2 Wins[/red]"
            loser_label = "[green]Player 1 Loses[/green]"
        else:
            winner_label = "[yellow]It's a Tie[/yellow]"
            loser_label = "[yellow]No adjustments[/yellow]"

        # Table for showing the adjustments
        table = Table(title="Post-Battle Stat Adjustments", box=box.SQUARE)
        table.add_column("Player", justify="center")
        table.add_column("Health", justify="center")
        table.add_column("Power", justify="center")

        # Add rows for Player 1 and Player 2
        table.add_row(f"Player 1 ({player1_pokemon[0]})", player1_HP_str, player1_Power_str)
        table.add_row(f"Player 2 ({player2_pokemon[0]})", player2_HP_str, player2_Power_str)

        # Display winner and adjustments
        self.console.print(f"{winner_label}\n")
        self.console.print(table)
        self.console.print(f"{loser_label}\n")

        input("Press Enter to continue...")
        print("\033c", end="")  # Clear the console




    def DisplayFatigueAdjustment(self, player1_pokemon, player2_pokemon, player1_prev_HP, player2_prev_HP) -> None:
        # Helper function to format health reduction due to fatigue
        def format_health_change(prev_health, new_health):
            return f"{prev_health} -> [red]{new_health}[/red]"

        # Create tables for both players to show health reduction due to fatigue
        table = Table(title="Fatigue Effects", box=box.SQUARE)
        table.add_column("Player", justify="center")
        table.add_column("Pokemon", justify="center")
        table.add_column("Health After Fatigue", justify="center")

        player1_health_str = format_health_change(player1_prev_HP, player1_pokemon[1])
        player2_health_str = format_health_change(player2_prev_HP, player2_pokemon[1])

        table.add_row("Player 1", player1_pokemon[0], player1_health_str)
        table.add_row("Player 2", player2_pokemon[0], player2_health_str)

        self.console.print(table)
        input("Press Enter to continue...")
        print("\033c", end="")  # Clear the console
        


    def DisplayBattlePreparation(self, player_selected, count) -> None:
        COLOR = "[green]" if count == 0 else "[red]"
        RESET = "[/]"
        
        table = Table(title=f"{COLOR}Player {count + 1} Battle Preparation{RESET}", box=box.MINIMAL)
        table.add_column("Pokemon", justify="center")
        table.add_column("Health", justify="center")
        table.add_column("Power", justify="center")
        table.add_column("Poison", justify="center")
        table.add_column("Potion", justify="center")
        
        player_pokemon = player_selected[0]
        player_health = player_selected[1]
        player_power = player_selected[2]
        player_poisons = player_selected[3]
        player_potions = player_selected[4]
        
        table.add_row(
            player_pokemon,  # Pokemon Name
            str(player_health),  # Health
            str(player_power),   # Power
            str(player_poisons),  # Poisons
            str(player_potions)   # Potions
        )
        
        self.console.print(table)

        
    # ===========================================
    # Display a table of all the selected pokemons
    # of both players
    # ===========================================
    def DisplayPlayersSelectedPokemons(self, player1, player2, player1_battle_pokemon, player2_battle_pokemon, count, All_pokemon_IsUsed, player1_unused, player2_unused) -> None:
        table1 = Table(title="Player 1", box=box.MINIMAL)
        table2 = Table(title="Player 2", box=box.MINIMAL)
        
        table1.add_column("Index", justify="center")
        table1.add_column("Pokemon", justify="center")
        table1.add_column("Health", justify="center")
        table1.add_column("Power", justify="center")
        table1.add_column("Poison", justify="center")
        table1.add_column("Potion", justify="center")
        table1.add_column("Used", justify="center")
        
        table2.add_column("Index", justify="center")
        table2.add_column("Pokemon", justify="center")
        table2.add_column("Health", justify="center")
        table2.add_column("Power", justify="center")
        table2.add_column("Poison", justify="center")
        table2.add_column("Potion", justify="center")
        table2.add_column("Used", justify="center")

        for i in range(len(player1)):
            # Player 1 
            table1.add_row(
                str(i + 1),
                player1[i][0],
                str(player1[i][1]),
                str(player1[i][2]),
                str(player1[i][3]),
                str(player1[i][4]),
                "Yes" if player1[i][5] else "No"
            )
            
            # Player 2
            table2.add_row(
                str(i + 1),
                player2[i][0],
                str(player2[i][1]),
                str(player2[i][2]),
                str(player2[i][3]),
                str(player2[i][4]),
                "Yes" if player2[i][5] else "No"
            )
        
        # Display tables side by side by printing each row of both tables together
        table1_str = table1.rows
        table2_str = table2.rows
        combined_Table = ""
        for row1, row2 in zip(table1_str, table2_str):
            combined_Table += f"{row1}  {row2}\n"

        # Printing additional info for battle status
        all_Pokemon_Used = "Yes" if All_pokemon_IsUsed else "No"
        
        self.console.print(f"All Pokémon Used?: {all_Pokemon_Used}")
        self.console.print(f"Player 1 Unused Pokémon: {player1_unused}")
        self.console.print(f"Player 2 Unused Pokémon: {player2_unused}")
        self.console.print(table1)
        self.console.print(table2)

# You can extend this to the other methods in a similar fashion.
