#P uppgift - elo för league

from player import Player

def menu():
    pass

def manual_create_player(players):
    namn = input("Vad heter din spelare? ")
    elo = int(input("Vad har din spelare för elo? "))
    players[namn] = elo
    print(players)

def create_player(name, elo):
    return Player(name, elo)

def create_team():
    name = input("Vad heter laget? ")
    team = []
    return name, team

def manual_assign_player():
    pass

def sort_players():
    pass

def distibute_players():
    pass

def simulate_match():
    pass

def match_result():
    pass

def main():
    players = {}
    manual_create_player(players)
    print(players)
    name, team = create_team()
    print(name)
main()