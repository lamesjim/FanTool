from bs4 import BeautifulSoup
import urllib2

import psycopg2

conn = psycopg2.connect(database="nfl_stats", user="postgres", password="pass123", host="127.0.0.1", port="5432")
print "Opened database successfully"

cur = conn.cursor()

def make_soup(url):
    page = urllib2.urlopen(url)
    soupdata = BeautifulSoup(page, 'html.parser')
    return soupdata

def get_player_totals():
    soup = make_soup("http://www.pro-football-reference.com/years/2014/fantasy.htm")
    table_stats = soup.find("table", {"id":"fantasy"})

    data_array = []
    rank = 1
    player_data = {}

    body = table_stats.find('tbody')
    for record in body.findAll('tr'):
        for data in record.findAll('td'):
            data_array.append(data.text)
        if len(data_array) > 0:
            player_data[rank] = data_array
            data_array = []
            rank = rank + 1

    player_stats = {}

    for player in player_data:
        if len(player_data[player]) > 0:
            player_stats[player] = {
                    "name": player_data[player][0],
                    "team": player_data[player][1],
                    "position": player_data[player][2],
                    "age": player_data[player][3] if len(player_data[player][3]) > 0 else "0",
                    "games_played": player_data[player][4],
                    "games_started": player_data[player][5],
                    "completions": player_data[player][6],
                    "attempts": player_data[player][7],
                    "pass_yards": player_data[player][8],
                    "pass_tds": player_data[player][9],
                    "interceptions": player_data[player][10]
                    "carries": player_data[player][11],
                    "rush_yards": player_data[player][12],
                    "yards_per_carry": player_data[player][13],
                    "rush_tds": player_data[player][14]
                    "targets": player_data[player][15],
                    "receptions": player_data[player][16],
                    "rec_yards": player_data[player][17],
                    "yards_per_reception": player_data[player][18],
                    "rec_tds": player_data[player][19]
            }

    return player_stats

player_totals = get_player_totals()

# insert into players table
for player in player_totals:

    cur.execute("INSERT INTO PLAYERS (NAME, POSITION, AGE) \
          VALUES (%s, %s, %s);",
          (player_totals[player]["name"], player_totals[player]["position"], int(player_totals[player]["age"])))

conn.commit()
print "Records created successfully";
conn.close()
