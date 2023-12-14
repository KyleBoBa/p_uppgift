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
    sorted_players = sorted(player_data, key=lambda x: (x['won_matches'] / x['total_matches']) if x['total_matches'] > 0 else 0, reverse=True)
    print("Plac \tNamn \t     vunna    spelade andel vunna")
    print(u'\u2500' * 50)
    for i, player in enumerate(sorted_players[:10]):
        if player['total_matches'] > 0:
            win_ratio = player['won_matches'] / player['total_matches']
        else:
            win_ratio = 0
        print(f"{i + 1:<2} \t{player['name']:<12.10}  {player['won_matches']:2}\t{player['total_matches']:2} \t{win_ratio:.2f}")

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