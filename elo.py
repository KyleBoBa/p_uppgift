#P uppgift - elo för league

import csv
from player import Player

def menu():
    pass

"""def manual_create_player(players): #återkommer till denna
    namn = input("Vad heter din spelare? ")
    while True:
        try:
            elo = int(input("Vad har din spelare för elo? "))
            players[namn] = elo
            break
        except ValueError:
            print("Elo måste vara insatt som en integer, försök igen.")"""

def read_player_data():
    player_data = []
    try:
        with open('players.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=';')
            next(csv_reader)  # Skip header row
            for line in csv_reader:
                player_name = line[0].strip()
                win_early = float(line[1].strip())
                win_mid = float(line[2].strip())
                win_late = float(line[3].strip())
                won_matches = int(line[4].strip())
                total_matches = int(line[5].strip())

                #validera data
                if not (0 <= win_early <= 1):
                    raise ValueError("Invalid win_early value")
                if not (0 <= win_mid <= 1):
                    raise ValueError("Invalid win_mid value")
                if not (0 <= win_late <= 1):
                    raise ValueError("Invalid win_late value")
                if not (0 <= won_matches <= total_matches):
                    raise ValueError("Invalid won_matches or total_matches value")
                
                player_data.append({
                    'name': player_name,
                    'win_early': win_early,
                    'win_mid': win_mid,
                    'win_late': win_late,
                    'won_matches': won_matches,
                    'total_matches': total_matches
                })
    except ValueError:
        print("Inkorrekt data värden, kolla över filen")
    return player_data

def assign_elo(player_data):
    base_player_elo = 1200
    for player in player_data:
        player['elo'] = base_player_elo
    return player_data

def create_team():
    while True:
        try:
            total_players = int(input("Hur många spelare är tillgängliga att köra? "))
            break
        except ValueError:
            print("Skriv in ett antal.")
    even_players_on_teams = total_players % 10
    if even_players_on_teams != 0:
        print(f"{even_players_on_teams} spelare kommer att stå över denna runda.")
        total_players -= even_players_on_teams
    total_teams = total_players // 5
    print(f"Det kommer att skapas {total_teams} lag")
    team_list = []
    for i in range(total_teams):
        team = []
        team_list.append(team)
    return team_list

def sort_players(player_data):
    sorted_players = sorted(player_data, key=lambda x: (x['elo']))
    return sorted_players

def distibute_players(player_data, team_list):
    number_of_teams = len(team_list)
    players_per_team = 5

    for i in player_data:
        if 

def manual_distribute_players():
    pass

def simulate_match(player_data):
    pass

def adjust_player_elo():
    pass

def match_result():
    print(f"Match vinnaren är {match_winner}")

def present_top_players(player_data):
    sorted_players = sorted(player_data, key=lambda x: (x['won_matches'] / x['total_matches']) if x['total_matches'] > 0 else 0)
    print("Plac \tNamn \t     vunna    spelade andel vunna")
    print(u'\u2500' * 50)
    for i, player in enumerate(sorted_players[:10]):
        if player['total_matches'] > 0:
            win_ratio = player['won_matches'] / player['total_matches']
        else:
            win_ratio = 0
        print(f"{i + 1:<2} \t{player['name']:<12.10}  {player['won_matches']:2}\t{player['total_matches']:2} \t{win_ratio:.2f}")

def main():
    players = {}
    """manual_create_player(players)"""
    player_data = read_player_data()
    player_data = assign_elo(player_data)
    present_top_players(player_data)
    sort_players(player_data)
    team_list = create_team()
    sorted_player_list = sort_players(player_data)
    distributed_teams = distibute_players(player_data, team_list)
    for i, team in enumerate(distributed_teams):
        print(f"Team {i + 1}: {team}")

if __name__ == "__main__":
    main()