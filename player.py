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

    def change_win_early(self, win_early):
        self.win_early = win_early
        return self.win_early
    
    def change_win_mid(self, win_mid):
        self.win_mid = win_mid
        return self.win_mid
    
    def change_win_late(self, win_late):
        self.win_late = win_late
        return self.win_late
    
    def change_won_matches(self, won_matches):
        self.won_matches = won_matches
        return self.won_matches
    
    def change_total_matches(self, total_matches):
        self.total_matches = total_matches
        return self.win_early
    
    def adjust_elo(self, updated_elo):
        self.elo = updated_elo
    
    def assign_team(self, team):
        self.team = team
