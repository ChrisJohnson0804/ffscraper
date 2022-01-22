# ffscraper.py - Extracts data about Fantasy Football League

import os, requests
import numpy as np
import pandas as pd
import matplotlib as plt
import math

os.chdir(r'C:\Users\Chris\Desktop\Programming\Python\PythonTestPrgrms\FFscraper')
leagueId = 911772
weekId = 1

class Team:
    def __init__(ateam, id, ownername, luck):
        ateam.id = id
        ateam.ownername = ownername
        ateam.luck = luck

def transactionScraper(seasonId):
    url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/911772"
    res = requests.get(url, cookies={"swid": "{0DFE1DDF-7B37-4346-BE1D-DF7B37734610}", "espn_s2": "AEBUEF4iAi932Fjc9%2BOX0PcOkSOyf1n0FexR3TLKcC1Ekqn4vyyKFS89DTONNm9xIIDsrAiADiV0Ahwv90vx7KiQnpLVPAlF2h4iw6xXHakZa4DTVxnBcvK04EGHP48Q0mFSUbLH2QfwT9znMy4AIeP%2FxYyWaNiGKfcNs5XeLZ3EeOSaHU3TAdNkIywlj2GunobX%2BAcp16wMPnhGQ4CSp9iumTu%2B9MYv%2BGiKuQ5ds39yOCI0ejJU9Z%2BoZLI1wytrjeRturOPZrzT9e1HE6C1r%2BBZ"}, params= {"view":"mTeam", "seasonId":str(seasonId)})
    res.raise_for_status()
    d = res.json()[0]
    transactiondata = open('transactiondata.txt', 'a')
    transactiondata.write('Data for the ' + str(seasonId) + ' season: \n')
    for team in range (0,12):
        for member in range(0,12):
            if( d['members'][member]['id'] == d['teams'][team]['owners'][0]):
                name = str(d['members'][member]['firstName']) +' ' + str(d['members'][member]['lastName'])
        transactiondata.write(name + ': ' + '\n' + 'Waiver wire pickups: ' + str(d['teams'][team]['transactionCounter']['acquisitions']) + '\n' + 'Trades: ' + str(d['teams'][team]['transactionCounter']['trades']) + '\n\n')
    transactiondata.write('\n')


def LeagueInit(seasonId):
    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2021/segments/0/leagues/911772"
    res = requests.get(url, cookies={"swid": "{0DFE1DDF-7B37-4346-BE1D-DF7B37734610}", "espn_s2": "AEBUEF4iAi932Fjc9%2BOX0PcOkSOyf1n0FexR3TLKcC1Ekqn4vyyKFS89DTONNm9xIIDsrAiADiV0Ahwv90vx7KiQnpLVPAlF2h4iw6xXHakZa4DTVxnBcvK04EGHP48Q0mFSUbLH2QfwT9znMy4AIeP%2FxYyWaNiGKfcNs5XeLZ3EeOSaHU3TAdNkIywlj2GunobX%2BAcp16wMPnhGQ4CSp9iumTu%2B9MYv%2BGiKuQ5ds39yOCI0ejJU9Z%2BoZLI1wytrjeRturOPZrzT9e1HE6C1r%2BBZ"}, 
    params= {"view":"mTeam"})
    res.raise_for_status()
    teamdata = res.json()
    teams = []
    for team in range (0,12):
        for member in range(0,12):
            if(teamdata['members'][member]['id'] == teamdata['teams'][team]['owners'][0]):
               teams.append(Team(teamdata['teams'][team]['id'], str(teamdata['members'][member]['firstName']) +' '+ str(teamdata['members'][member]['lastName']), 0))
    return teams

def LuckScraper(seasonId):
    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2021/segments/0/leagues/911772?view=mMatchup"
    res = requests.get(url, cookies={"swid": "{0DFE1DDF-7B37-4346-BE1D-DF7B37734610}", "espn_s2": "AEBUEF4iAi932Fjc9%2BOX0PcOkSOyf1n0FexR3TLKcC1Ekqn4vyyKFS89DTONNm9xIIDsrAiADiV0Ahwv90vx7KiQnpLVPAlF2h4iw6xXHakZa4DTVxnBcvK04EGHP48Q0mFSUbLH2QfwT9znMy4AIeP%2FxYyWaNiGKfcNs5XeLZ3EeOSaHU3TAdNkIywlj2GunobX%2BAcp16wMPnhGQ4CSp9iumTu%2B9MYv%2BGiKuQ5ds39yOCI0ejJU9Z%2BoZLI1wytrjeRturOPZrzT9e1HE6C1r%2BBZ"})
    res.raise_for_status()
    d = res.json()['schedule']
    teams = LeagueInit(seasonId)
    df = []
    for game in range (0, 84):
        matchup = [d[game]['matchupPeriodId'], d[game]['home']['teamId'], d[game]['home']['totalPoints'], d[game]['away']['teamId'], d[game]['away']['totalPoints']]
        df.append(matchup)
    df = pd.DataFrame(df, columns= ['Week', 'Team1', 'Score1', 'Team2', 'Score2'])
    df.head()

    meds = (df
        .filter(['Week', 'Score1', 'Score2'])
        .melt(id_vars=['Week'], value_name='Score')
        .groupby('Week')
        .median()
        .reset_index()
        )
    print(meds)

    tm = 1

    df2 = df.query('Team1 == @tm | Team2 == @tm').reset_index(drop=True)
    ix = list(df2['Team2'] == tm)
    
    
LuckScraper(2021)


print('Done')