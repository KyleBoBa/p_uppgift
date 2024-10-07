class Player:
    def __init__(self, player_id, name, win_early, win_mid, win_late):
        self.player_id = player_id
        self.name = name
        self.win_early = win_early
        self.win_mid = win_mid
        self.win_late = win_late
        self.won_matches = 0
        self.total_matches = 0
        self.elo = 1200
    
    def __str__(self):
        return f"{self.name} har spelat {self.total_matches} och vunnit {self.won_matches}"

    def assign_team(self, team):
        self.team = team
