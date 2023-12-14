#P uppgift - elo för league

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
    with open('players.csv', 'r') as file:
        for line in file:
            line = line.strip().split(";")
            player_name = line[0].strip()
            win_early = float(line[1].strip())
            win_mid = float(line[2].strip())
            win_late = float(line[3].strip())
            won_matches = int(line[4].strip())
            total_matches = int(line[5].strip())
            player_data.append({
                'name': player_name,
                'win_early': win_early,
                'win_mid': win_mid,
                'win_late': win_late,
                'won_matches': won_matches,
                'total_matches': total_matches
            })
    return player_data

def present_top_players(player_data):
    try:
        sorted_players = sorted(player_data, key=lambda x: (x['won_matches'] / x['total_matches']), reverse=True)
    except ZeroDivisionError:
        print("Dina spelare har inga matcher än, kan inte rangordna baserat på matcher")
    else:
        print("Plac Namn vunna spelade andel vunna")
        for i, player in enumerate(sorted_players[:10]):
            win_ratio = player['won_matches'] / player['total_matches'] if player['total_matches'] > 0 else 0
            print(f"{i + 1} {player['name']} {player['won_matches']} {player['total_matches']} {win_ratio:.2f}")

def create_team():
    pass

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
    """manual_create_player(players)"""
    print(players)
    player_data = read_player_data()
    present_top_players(player_data)
    
if __name__ == "__main__":
    main()