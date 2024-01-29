#P uppgift - elo för league

import random
import csv
from player import Player

def introduction(player_data): #liten introduktion till programmet och vad användaren kan förvänta sig
    print("Välkommen till League of Legends matchmaking systemet\n")
    print("Här så möts spelare i en 5 mot 5 match för att ta reda på vem som är bäst!\n")
    print("Just nu ser tabellen av toppspelarna ut såhär:")
    present_top_players(player_data)

def menu(player_data): #meny för de olika funktionerna av programmet
    while True:
        print("\nMeny")
        print(u"\u2500" * 20)
        print("1. Kör en match")
        print("2. Skriv ut tabellen")
        print("3. Lägg till en ny spelare")
        print("4. Skriv ut tabellen till fil")
        print("5. Avsluta")
        try:
            choice = int(input("\nVad vill du göra? "))
            if choice == 1:
                run_match(player_data)
            elif choice == 2:
                present_top_players(player_data)
            elif choice == 3:
                """manual_create_player(player_data)"""
            elif choice == 4:
                write_to_file(player_data)
            elif choice == 5:
                print("Tack för du kört programmet")
                break
            else:
                print("Välj ett av alternativen in menyn")
        except ValueError:
            print("Ditt val är inte ett giltigt svarsalternativ, försök igen\n")

def manual_create_player(player_data): #manuellt skapa spelare för databasen genom Player klass
    player_id = input("Vilket ID får din spelare? ")
    name = input("Vad heter din spelare? ")
    win_early = input("Vad har din spelare för chans att vinna early game? ")
    win_mid = input("Vad har din spelare för chans att vinna mid game? ")
    win_late = input("Vad har din spelare för chans att vinna late game? ")

    player = Player(
                    player_id, #spelar id
                    name, #namn på spelare
                    win_early, #chans att vinna early game
                    win_mid, #chans att vinna mid game,
                    win_late, #chans att vinna late game,
                    )
    player_data.append({player})
    return player_data

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

def assign_base_elo(player_data): #sätter alla spelares base elo till 1200
    base_player_elo = 1200
    for player in player_data:
        player['elo'] = base_player_elo
    return player_data

def run_match(player_data): #lag skapas och simulering körs
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

def distribute_players(player_data, team_list): #delar ut spelarna till lag, sorterar baserat på elo så att det inte är ojämnt
    num_teams = len(team_list)
    sorted_players = sorted(player_data, key=lambda x: x['elo'])
    teams = [[] for _ in range(num_teams)]
    players_per_team = 5

    for i, player in enumerate(sorted_players):
        team_index = i % num_teams
        if len(teams[team_index]) < players_per_team:
            teams[team_index].append(player)
    return teams

def simulate_match(teams): #match simulering av de tre faserna

    simulate_early_game(teams) #Stage 1 - early game

    simulate_mid_game(teams) #Stage 2 - mid game

    simulate_late_game(teams) #Stage 3 - late game

def simulate_early_game(teams): #simulerar early game, spelare 1 för lag 1 möter spelare 1 för lag 2 osv..
    counter = 0  # räknar när resultat har blivit printat 5 gånger (alla möjliga parningar)
    team1_wins = 0  #räknare för vinster
    team2_wins = 0  
    print("\nMatchen har startat, vi får se hur det går för lagen i early game.")
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
            print(f"Spelare {j+1} i lag {i+1} {result} i early game mot spelare {j+1} i lag {2-i} ({opponent_result})")
            counter += 1
            if counter == 5: #avsluta loop
                break
        if counter == 5:
            break
    
    print(f"Lag 1 vinner: {team1_wins}")
    print(f"Lag 2 vinner: {team2_wins}\n")
    if team1_wins > 3:
        for player in teams[1]:
            player['temp_win_mid'] = player['win_mid'] * 0.9
        for player in teams[0]:
            player['temp_win_mid'] = player['win_mid']
        print("Spelarna i lag 2 har hamnat under i early game.\nDe kommer få att kämpa ännu hårdare i mid game då deras chanser att vinna har nu minskat med 10%.\n")
    elif team2_wins > 3:
        for player in teams[0]:
            player['temp_win_mid'] = player['win_mid'] * 0.9
        for player in teams[1]:
            player['temp_win_mid'] = player['win_mid']
        print("Spelarna i lag 1 har hamnat under i early game.\nDe kommer få kämpa ännu hårdare i mid game då deras chanser har minskat med 10%.\n")
    else:
        for team in teams:
            for player in team:
                player['temp_win_mid'] = player['win_mid']
        if team1_wins > team2_wins:
            print(f"Båda lagen hade ett relativt bra early game med lag 1 som kom ut på topp.\nVi får se om lag 2 drar tillbaka det i mid game då det inte är över.")
        else:
            print(f"Båda lagen hade ett relativt bra early game med lag 2 som kom ut på topp.\nVi får se om lag 1 drar tillbaka det i mid game då det inte är över.")

def fight(player_a, player_b): #simulerar fighten i mid game, spelarnas chans att vinna mid game dikterar deras strenght med hjälp av chans 
    attacker_strength = sum(random.randint(1, 6) for _ in range(int(player_a['temp_win_mid'] * 10)))
    defender_strength = sum(random.randint(1, 6) for _ in range(int(player_b['temp_win_mid'] * 10)))

    print(f"{player_a['name']} attackerar med: {attacker_strength}")
    print(f"{player_b['name']} försvarar med: {defender_strength}")

    if attacker_strength > defender_strength:
        print("Attackerare vann!\n----------------------------------------------")
        return 1
    else:
        print("Försvare vann!\n----------------------------------------------")
        return 0

def simulate_mid_game(teams): #simulering av mid game, lag med flest vinnare har större chans att vinna late game
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
            player['temp_win_late'] = player['win_late'] * 0.7
        for player in teams[0]:
            player['temp_win_late'] = player['win_late']
    else:
        for player in teams[0]:
            player['temp_win_late'] = player['win_late'] * 0.7
        for player in teams[1]:
            player['temp_win_late'] = player['win_late']

def simulate_late_game(teams): #simulering av late game, medelvärde av lagens chans att vinna late game dikterar vinnare av matchen
    print("Det börjar närma sig slutet av matchen, dags att se vilket lag som vinner.\n")
    team1_average = sum(player['temp_win_late'] for player in teams[0]) / len(teams[0])
    team2_average = sum(player['temp_win_late'] for player in teams[1]) / len(teams[1])

    if team1_average > team2_average:
        print("Lag 1 vinner i late game!")
        match_winner = teams[0]
    elif team1_average < team2_average:
        print("Lag 2 vinner i late game!")
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

def present_top_players(player_data): #tabell för de bästa spelarna, sorteras baserat på matcher spelade sen andel matcher vunna
    sorted_players = sorted(player_data, key=lambda x: (x['total_matches'], x['won_matches'] / x['total_matches']) if x['total_matches'] > 0 else (0, 0), reverse=True)
    print("Plac \tNamn \t     vunna    spelade  vinst %")
    print(u"\u2500" * 48)
    for i, player in enumerate(sorted_players[:10]):
        if player['total_matches'] > 0:
            win_ratio = player['won_matches'] / player['total_matches']
            win_ratio *= 100
        else:
            win_ratio = 0
        print(f"{i + 1:<2} \t{player['name']:<12.10}  {player['won_matches']:2}\t{player['total_matches']:2} \t{win_ratio:.2f}")

def write_to_file(player_data): #skriver ut tidiage tabell till en fil i .csv format
    file_name = input("Skriv in filnamnet (inklusive .csv): ")
    try:
        sorted_players = sorted(player_data, key=lambda x: (x['total_matches'], x['won_matches'] / x['total_matches']) if x['total_matches'] > 0 else (0, 0), reverse=True)
        with open(file_name, 'w', newline='') as file:
            csv_writer = csv.writer(file, delimiter=';')
            csv_writer.writerow(["Plac", "Namn", "Vunna", "Spelade", "Vinst %"])
            for i, player in enumerate(sorted_players[:10]):
                if player['total_matches'] > 0:
                    win_ratio = player['won_matches'] / player['total_matches']
                else:
                    win_ratio = 0
                csv_writer.writerow([i + 1, player['name'], player['won_matches'], player['total_matches'], f"{win_ratio:.2%}"])
        print("Scoreboard written to file successfully.")
    except IOError:
        print("Error writing to file.")

def main(): #huvud funktion
    player_data = read_player_data()
    player_data = assign_base_elo(player_data)
    introduction(player_data)
    menu(player_data)

if __name__ == "__main__":
    main()
