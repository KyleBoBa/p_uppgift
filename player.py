class Player:
    def __init__(self, name, elo):
        self.name = name
        self.elo = elo
        self.team = None
    
    def __str__(self):
        return f"{self.name} har elon {self.elo}"

    def change_elo(self, elo):
        self.elo = elo
        return self.elo
    
    def assign_team(self, team):
        self.team = team