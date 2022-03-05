from lib2to3.pgen2.pgen import DFAState
from bs4 import BeautifulSoup
import requests
import pandas as pd 
from time import sleep
import random


def findstats():  # Creates a frame which holds the names and stats of teams 
    #~~~~~~~~ Offensive Soup
    response = requests.get('https://www.espn.com/nfl/stats/team/_/table/general/sort/gamesPlayed/dir/desc').text  # sorted by games played
    soup = BeautifulSoup(response, 'lxml')
    league = soup.find_all('tbody', class_='Table__TBODY')
    stats = soup.find_all('tr', {'data-idx': '0'}, class_='Table__TR Table__TR--sm Table__even', )
    team_names = soup.find_all('tr', class_='Table__TR Table__TR--sm Table__even')
    teams = soup.find_all('tbody', class_='Table__TBODY')
    teamstats = teams[1]
    teamstats_ind = teamstats.find_all('tr', class_='Table__TR Table__TR--sm Table__even')

    #~~~~~~~ Defensive Soup
    response2 = requests.get('https://www.espn.com/nfl/stats/team/_/view/defense/table/general/sort/gamesPlayed/dir/desc').text # Sorted by games played 
    soup2 = BeautifulSoup(response2, 'lxml')
    teams2 = soup2.find_all('tbody', class_='Table__TBODY')
    teamstats2 = teams2[1]
    teamstats_ind2 = teamstats2.find_all('tr', class_='Table__TR Table__TR--sm Table__even')
    teamnames = []

    o_yards = []
    o_pts_g = []
    o_yds_g = []
    d_pts_g = []

    for i in range(32):
        teamnames.append(team_names[i].text)

    # Offensive stats 
    for i in range(len(teamstats_ind)):
        
        teamstatslist = []
        stats_ind_list = []
        teamstatslist.append(teamstats_ind[i])
        for i in range(len(teamstatslist)):
            stats_ind_list.append(teamstatslist[i].find_all('td', class_='Table__TD'))
        yds = stats_ind_list[0][1].text
        ptsg = stats_ind_list[0][8].text
        oydsg = stats_ind_list[0][2].text
        o_yards.append(yds)
        o_pts_g.append(ptsg)
        o_yds_g.append(oydsg)

    #Defensive Stats 
    for i in range(len(teamstats_ind2)):
        teamstatslist2 = []
        stats_ind_list2 = []
        teamstatslist2.append(teamstats_ind2[i])
        for i in range(len(teamstatslist2)):
            stats_ind_list2.append(teamstatslist2[i].find_all('td', class_='Table__TD'))
        dptsg = stats_ind_list2[0][8].text
        d_pts_g.append(dptsg)

    nfl_teamstats = {
        'Team': teamnames,
        'Offensive Yards': o_yards,
        'Offensive PTS/G': o_pts_g,
        'Offensive YDS/G': o_yds_g,
        'Defensive PTS/G': d_pts_g,
    }

    df = pd.DataFrame(nfl_teamstats)

    # Turning column values into numbers
    df['Offensive Yards'] = df['Offensive Yards'].str.split(',').str.join('').astype(int)  # This removes the comma so we can turn it into an integer
    df['Offensive YDS/G'] = df['Offensive YDS/G'].astype(float) 
    df['Offensive PTS/G'] = df['Offensive PTS/G'].astype(float)
    df['Defensive PTS/G'] = df['Defensive PTS/G'].astype(float)

    # sorting it by column
    #df2 = df.sort_values(by='Defensive PTS/G', ascending=True)

    df.set_index('Team', inplace=True)

    return df













