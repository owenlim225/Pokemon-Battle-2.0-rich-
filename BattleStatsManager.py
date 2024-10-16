from rich.console import Console
from rich.table import Table
from rich import box

class BattleStatsManager:
    def __init__(self):
        self.console = Console()
        self.player1_wins = 0
        self.player2_wins = 0
        self.ties = 0
        
        self.GREEN = "[green]"
        self.RED = "[red]"
        self.YELLOW = "[yellow]"
        self.RESET = "[/]"
        
        # Initialize the rich table
        self.stats_table = Table(title=f"{self.YELLOW}Battle Statistics{self.RESET}", box=box.MINIMAL_DOUBLE_HEAD)
        self.stats_table.add_column("Battle", justify="center")
        self.stats_table.add_column(f"{self.GREEN}Player 1 Pokemon{self.RESET}", justify="center")
        self.stats_table.add_column(f"{self.GREEN}Player 1 Health{self.RESET}", justify="center")
        self.stats_table.add_column(f"{self.GREEN}Player 1 Power{self.RESET}", justify="center")
        self.stats_table.add_column(f"{self.RED}Player 2 Pokemon{self.RESET}", justify="center")
        self.stats_table.add_column(f"{self.RED}Player 2 Health{self.RESET}", justify="center")
        self.stats_table.add_column(f"{self.RED}Player 2 Power{self.RESET}", justify="center")
        self.stats_table.add_column("Winner", justify="center")
               
    def SetValueToStatsTable(self, battle_num, player1, player2, winner):
        win_str = "Tie"
        if winner == f"{self.GREEN}Player 1{self.RESET}":
            win_str = f"{self.GREEN}Player 1{self.RESET}"
        elif winner == f"{self.RED}Player 2{self.RESET}":
            win_str = f"{self.RED}Player 2{self.RESET}"

        self.stats_table.add_row(
            str(battle_num + 1),
            player1[0],  # Player 1 Pokemon
            str(player1[1]),  # Player 1 Health
            str(player1[2]),  # Player 1 Power
            player2[0],  # Player 2 Pokemon
            str(player2[1]),  # Player 2 Health
            str(player2[2]),  # Player 2 Power
            win_str  # Winner
        )
        
    def ShowStatsTable(self):
        if self.player1_wins > self.player2_wins:
            overall_winner = f"{self.GREEN}Player 1{self.RESET}"
        elif self.player2_wins > self.player1_wins:
            overall_winner = f"{self.RED}Player 2{self.RESET}"
        else:
            overall_winner = f"{self.YELLOW}No Overall Winner{self.RESET}"
        
        self.console.print(f"{'':<54}🔥 Pokemon Battle 🔥")
        self.console.print(f"{'':<42}🔥 ============ Overall Winner ============ 🔥")
        self.console.print(f"{'':<60}{overall_winner}\n")
        self.console.print(
            f"{'':<40}{self.GREEN}Player 1{self.RESET} Wins: {self.player1_wins}  "
            f"{self.RED}Player 2{self.RESET} Wins: {self.player2_wins}  "
            f"Ties: {self.ties}\n"
        )
        self.console.print(self.stats_table)
        
    @property
    def GetPlayer1_win_count(self) -> int:
        return self.player1_wins
    
    @GetPlayer1_win_count.setter
    def GetPlayer1_win_count(self, value):
        if value < 0:
            raise ValueError("Value must not be negative")
        self.player1_wins += value
        
    @property
    def GetPlayer2_win_count(self) -> int:
        return self.player2_wins
    
    @GetPlayer2_win_count.setter
    def GetPlayer2_win_count(self, value):
        if value < 0:
            raise ValueError("Value must not be negative")
        self.player2_wins += value
        
    @property
    def GetTie_count(self) -> int:
        return self.ties
    
    @GetTie_count.setter
    def GetTie_count(self, value):
        if value < 0:
            raise ValueError("Value must not be negative")
        self.ties += value
    