#P uppgift - elo för league

import random
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

def read_player_data(): #läser in info från fil och lagrar spelar dictionary i listan
    player_data = []
    try:
        with open('players.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=';')
            next(csv_reader)  #hoppa över header row
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

def create_team(player_data): #skapar lag baserat på hur många spelare användaren matar in
    while True:
        try:
            total_players = int(input("Hur många spelare är tillgängliga att köra? "))
            if total_players > len(player_data):
                print("Det finns inte så många spelare i databasen, skriv ett mindre antal eller lägg till nya spelare manuellt")
            else:
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

def distribute_players(player_data, team_list):
    num_teams = len(team_list)
    sorted_players = sorted(player_data, key=lambda x: x['elo'])
    teams = [[] for _ in range(num_teams)]
    players_per_team = 5

    for i, player in enumerate(sorted_players):
        team_index = i % num_teams
        if len(teams[team_index]) < players_per_team:
            teams[team_index].append(player)
    return teams

def manual_distribute_players():
    pass

def simulate_match(player_data, teams):

    simulate_early_game(teams) #Stage 1 - early game

    simulate_mid_game(teams) #Stage 2 - mid game

    simulate_late_game(teams) #Stage 3 - late game

    adjust_player_elo(player_data)

    match_result()

def simulate_early_game(teams):
    counter = 0  # räknar när resultat har blivit printat 5 gånger (alla möjliga parningar)
    team1_wins = 0  #räknare för vinster
    team2_wins = 0  
    
    for i, team in enumerate(teams):
        for j, player in enumerate(team):
            opponent_team = teams[1 - i]  # motstående lag
            opponent_player = opponent_team[j]  # motstående spelare
            if player['win_early'] > opponent_player['win_early']:
                result = "won"
                opponent_result = "lost"
                if i == 0:
                    team1_wins += 1
                else:
                    team2_wins += 1
            else:
                result = "lost"
                opponent_result = "won"
                if i == 0:
                    team2_wins += 1
                else:
                    team1_wins += 1
            print(f"Player {j+1} in Team {i+1} {result} in early game against Player {j+1} in Team {2-i} ({opponent_result}).")
            counter += 1
            if counter == 5:  # avsluta loop
                break
        if counter == 5:
            break
    
    print(f"Team 1 wins: {team1_wins}")
    print(f"Team 2 wins: {team2_wins}")
    
    if team1_wins > 3:
        for player in teams[1]:
            player['win_mid'] *= 0.8  # minska med chans att vinna mid game med 20%
        print("Spelarna i lag 2 har hamnat under i early game, de kommer få kämpa ännu hårdare i midgame då deras chanser har minskat med 20%")
    elif team2_wins > 3:
        for player in teams[0]:
            player['win_mid'] *= 0.8
        print("Spelarna i lag 1 har hamnat under i early game, de kommer få kämpa ännu hårdare i midgame då deras chanser har minskat med 20%")

def simulate_mid_game(teams):
    pass

def simulate_late_game(teams):
    pass

def adjust_player_elo(player_data):
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
    team_list = create_team(player_data)
    sorted_player_list = sort_players(player_data)
    teams = distribute_players(player_data, team_list)
    for i, team in enumerate(teams):
        print(f"Team {i + 1}: {team}")
    simulate_match(player_data, teams)


if __name__ == "__main__":
    main()