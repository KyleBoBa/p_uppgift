#P uppgift - elo för league

import random
import csv
from player import Player

def introduction(player_data):
    print("Välkommen till League of Legends matchmaking systemet\n")
    print("Här så möts spelare i en 5 mot 5 match för att ta reda på vem som är bäst!\n")
    print("Just nu ser tabellen av toppspelarna ut såhär:")
    present_top_players(player_data)
    print("\nFör att påbörja en ny macth skriv in spelare.\n")


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
                player_id = int(line[0].strip())
                player_name = line[1].strip()
                win_early = float(line[2].strip())
                win_mid = float(line[3].strip())
                win_late = float(line[4].strip())
                won_matches = int(line[5].strip())
                total_matches = int(line[6].strip())

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
                    'player_id': player_id,
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
            elif total_players < 10:
                print("Det finns inte nog med spelare för att börja matchen.")
                break
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
    for _ in range(total_teams):
        team = []
        team_list.append(team)
    return team_list

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

def simulate_match(teams):

    simulate_early_game(teams) #Stage 1 - early game

    simulate_mid_game(teams) #Stage 2 - mid game

    simulate_late_game(teams) #Stage 3 - late game

def simulate_early_game(teams):
    counter = 0  # räknar när resultat har blivit printat 5 gånger (alla möjliga parningar)
    team1_wins = 0  #räknare för vinster
    team2_wins = 0  
    print("\nMatchen har startat, vi får se hur det går för lagen i early-game.")
    print(u"\u2500" * 68)
    for i, team in enumerate(teams):
        for j, player in enumerate(team):
            opponent_team = teams[1 - i] #motstående lag
            opponent_player = opponent_team[j] #motstående spelare
            if player['win_early'] > opponent_player['win_early']:
                result = "vann"
                opponent_result = "förlorade"
                if i == 0:
                    team1_wins += 1
                else:
                    team2_wins += 1
            else:
                result = "förlorade"
                opponent_result = "vann"
                if i == 0:
                    team2_wins += 1
                else:
                    team1_wins += 1
            print(f"Spelare {j+1} i team {i+1} {result} i early game mot spelare {j+1} i lag {2-i} ({opponent_result})")
            counter += 1
            if counter == 5: #avsluta loop
                break
        if counter == 5:
            break
    
    print(f"Team 1 wins: {team1_wins}")
    print(f"Team 2 wins: {team2_wins}\n")
    if team1_wins > 3:
        for player in teams[1]:
            player['win_mid'] *= 0.9  #minska chans att vinna mid game med 20%
        print("Spelarna i team 2 har hamnat under i early game.\nDe kommer få att kämpa ännu hårdare i midgame då deras chanser att vinna har nu minskat med 10%.\n")
    elif team2_wins > 3:
        for player in teams[0]:
            player['win_mid'] *= 0.9
        print("Spelarna i team 1 har hamnat under i early game.\nDe kommer få kämpa ännu hårdare i midgame då deras chanser har minskat med 10%.\n")
    else:
        if team1_wins > team2_wins:
            print(f"Båda lagen hade ett relativt bra early-game med lag 1 som kom ut på topp.\nVi får se om lag 2 drar tillbaka det i mid-game då det inte är över.")
        else:
            print(f"Båda lagen hade ett relativt bra early-game med lag 2 som kom ut på topp.\nVi får se om lag 1 drar tillbaka det i mid-game då det inte är över.")
def fight(player_a, player_b):
    attacker_strength = sum(random.randint(1, 6) for _ in range(int(player_a['win_mid'] * 10)))
    defender_strength = sum(random.randint(1, 6) for _ in range(int(player_b['win_mid'] * 10)))

    print(f"{player_a['name']} attackerar med: {attacker_strength}")
    print(f"{player_b['name']} försvarar med: {defender_strength}")

    if attacker_strength > defender_strength:
        print("Defender lost!\n----------------------------------------------")
        return 1
    else:
        print("Attacker lost!\n----------------------------------------------")
        return 0

def simulate_mid_game(teams):
    team1_wins = 0
    team2_wins = 0
    for i in range(len(teams[0])):
        player_a = teams[0][i]
        player_b = teams[1][i]
        
        battle_result = fight(player_a, player_b)
        
        if battle_result == 1:
            team1_wins += 1
        else:
            team2_wins += 1

    if team1_wins > team2_wins:
        for player in teams[1]:
            player['win_late'] *= 0.7
    else:
        for player in teams[0]:
            player['win_late'] *= 0.7


def simulate_late_game(teams):
    print("Det börjar närma sig slutet av matchen, dags att se vilket lag som vinner.\n")
    team1_average = sum(player['win_late'] for player in teams[0]) / len(teams[0])
    team2_average = sum(player['win_late'] for player in teams[1]) / len(teams[1])

    if team1_average > team2_average:
        print("Team 1 wins the late game!")
        match_winner = teams[0]
    elif team1_average < team2_average:
        print("Team 2 wins the late game!")
        match_winner = teams[1]
    else:
        team1_strongest_player = max(teams[0], key=lambda x: x['win_late'])
        team2_strongest_player = max(teams[1], key=lambda x: x['win_late'])
        print("Både lagen spelar väldigt bra tillsammans och i en sista teamfight så har 4 spelare dött i båda lag.")
        print(f"Det är upp till {team1_strongest_player['name']} och {team2_strongest_player['name']} att slåss till döds i slutet, vinnaren tar allt")
        if team1_strongest_player['win_late'] >= team2_strongest_player['win_late']:
            print(f"{team1_strongest_player['name']} vinner fighten att ger vinst till team 1.")
            match_winner = teams[0]
        else:
            print(f"{team2_strongest_player['name']} vinner fighten att ger vinst till team 2.")
            match_winner = teams[1]

    for team in teams:
        for player in team:
            player['total_matches'] += 1

    for player in match_winner:
        player['won_matches'] += 1
        player['elo'] += 10

    for team in teams:
        for player in team:
            if player not in match_winner:
                player['elo'] -= 10

def present_top_players(player_data):
    sorted_players = sorted(player_data, key=lambda x: (x['won_matches'] / x['total_matches']) if x['total_matches'] > 0 else 0)
    print("Plac \tNamn \t     vunna    spelade  vinst %")
    print(u"\u2500" * 48)
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
    introduction(player_data)
    
    team_list = create_team(player_data)
    if not team_list == []:
        teams = distribute_players(player_data, team_list)
        for i, team in enumerate(teams):
            print(f"Team {i + 1}: ", end="")
            for player in team:
                print(player['name'], end=" ")
            print()
        simulate_match(teams)
        present_top_players(player_data)

if __name__ == "__main__":
    main()
