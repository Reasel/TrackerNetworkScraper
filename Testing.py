#!/usr/bin/python3


import argparse
import requests
import re
from setup_logging import logger
import json
import csv


class Webscrape():
    '''classes are cool, no other real reason to use this - probably going to only have one function'''
    def __init__(self):
        self.webpath = "https://api.tracker.gg/api/v2/rocket-league/standard/profile/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        self.latestseason = '18' #need a better way to update this, perhaps dynamically?
        self.rltrackermissing = "We could not find your stats,"
        self.psyonixdisabled = "Psyonix has disabled the Rocket League API"


    def retrieveDataRLTrackerFromURL(self,url):
        headers = self.headers
        playerdata = {} # define the playerdata dict
        page = requests.get(url, headers=headers)
        if page.status_code == 200:
            data = json.loads(page.text)
            segs = data["data"]["segments"]
            for segment in segs:
                        if "playlist" in segment['type']:
                            playerdata[segment['metadata']['name']] = {'rank': segment['stats']['tier']['metadata']['name'], 'iconUrl': segment['stats']['tier']['metadata']['iconUrl'], 'division': segment['stats']['division']['metadata']['name'], 'mmr': segment['stats']['rating']['value']}

        return playerdata

    def retrieveDataRLTracker(self,gamertag="reasel",platform="steam"):
        webpath = self.webpath
        headers = self.headers
        rltrackermissing = self.rltrackermissing
        psyonixdisabled = self.psyonixdisabled
        playerdata = {} # define the playerdata dict
        playerdata[gamertag] = {} # define the gamertag dict
        page = requests.get("%(webpath)s%(platform)s/%(gamertag)s" % locals(), headers=headers)
        if page.status_code == 200:
            data = json.loads(page.text)
            segs = data["data"]["segments"]
            for segment in segs:
                        if "playlist" in segment['type']:
                            playerdata[segment['metadata']['name']] = {'rank': segment['stats']['tier']['metadata']['name'], 'iconUrl': segment['stats']['tier']['metadata']['iconUrl'], 'division': segment['stats']['division']['metadata']['name'], 'mmr': segment['stats']['rating']['value']}

        return playerdata


def singleRun(gamertag,platform):
    '''Single run of Webscrape.retrieveDataRLTracker'''
    scrape = Webscrape()
    data = scrape.retrieveDataRLTracker(gamertag=gamertag,platform=platform)
    if data is not None:
        pprint(data)

def manyRun(playerCsv):
    name               = 0
    trackerNetwork     = 1
    statsLink          = 2
    onesIcon           = 3
    onesRank           = 4
    onesDivision       = 5
    onesMMR            = 6
    twosIcon           = 7
    twosRank           = 8
    twosDivision       = 9
    twosMMR            = 10
    threesIcon         = 11
    threesRank         = 12
    threesDivision     = 13
    threesMMR          = 14
    casualIcon         = 15
    casualRank         = 16
    casualDivision     = 17
    casualMMR          = 18
    snowdayIcon        = 19
    snowdayRank        = 20
    snowdayDivision    = 21
    snowdayMMR         = 22
    rumbleIcon         = 23
    rumbleRank         = 24
    rumbleDivision     = 25
    rumbleMMR          = 26
    dropshotIcon       = 27
    dropshotRank       = 28
    dropshotDivision   = 29
    dropshotMMR        = 30
    hoopsIcon          = 31
    hoopsRank          = 32
    hoopsDivision      = 33
    hoopsMMR           = 34
    tournamentIcon     = 35
    tournamentRank     = 36
    tournamentDivision = 37
    tournamentMMR      = 38
    scrape = Webscrape()
    with open(playerCsv, newline='', mode='r+') as csvfile:
        reader = csv.DictReader(csvfile)
        with open('output.csv',  mode='r+', newline='') as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                data = scrape.retrieveDataRLTrackerFromURL(url=row['Link to Stats'])
                row['1\'s Icon']           = data['Ranked Duel 1v1']['iconUrl']
                row['1\'s Division']       = data['Ranked Duel 1v1']['division']
                row['1\'s MMR']            = data['Ranked Duel 1v1']['mmr']
                row['1\'s Rank']           = data['Ranked Duel 1v1']['rank']

                row['2\'s Icon']           = data['Ranked Doubles 2v2']['iconUrl']
                row['2\'s Division']       = data['Ranked Doubles 2v2']['division']
                row['2\'s MMR']            = data['Ranked Doubles 2v2']['mmr']
                row['2\'s Rank']           = data['Ranked Doubles 2v2']['rank']

                row['3\'s Icon']           = data['Ranked Standard 3v3']['iconUrl']
                row['3\'s Division']       = data['Ranked Standard 3v3']['division']
                row['3\'s MMR']            = data['Ranked Standard 3v3']['mmr']
                row['3\'s Rank']           = data['Ranked Standard 3v3']['rank']

                row['Casual Icon']         = data['Un-Ranked']['iconUrl']
                row['Casual Division']     = data['Un-Ranked']['division']
                row['Casual MMR']          = data['Un-Ranked']['mmr']
                row['Casual Rank']         = data['Un-Ranked']['rank']

                row['Tournament Icon']     = data['Tournament Matches']['iconUrl']
                row['Tournament Division'] = data['Tournament Matches']['division']
                row['Tournament MMR']      = data['Tournament Matches']['mmr']
                row['Tournament Rank']     = data['Tournament Matches']['rank']

                row['Hoops Icon']          = data['Hoops']['iconUrl']
                row['Hoops Division']      = data['Hoops']['division']
                row['Hoops MMR']           = data['Hoops']['mmr']
                row['Hoops Rank']          = data['Hoops']['rank']

                row['Snowday Icon']        = data['Snowday']['iconUrl']
                row['Snowday Division']    = data['Snowday']['division']
                row['Snowday MMR']         = data['Snowday']['mmr']
                row['Snowday Rank']        = data['Snowday']['rank']

                row['Dropshot Icon']       = data['Dropshot']['iconUrl']
                row['Dropshot Division']   = data['Dropshot']['division']
                row['Dropshot MMR']        = data['Dropshot']['mmr']
                row['Dropshot Rank']       = data['Dropshot']['rank']

                row['Rumble Icon']         = data['Rumble']['iconUrl']
                row['Rumble Division']     = data['Rumble']['division']
                row['Rumble MMR']          = data['Rumble']['mmr']
                row['Rumble Rank']         = data['Rumble']['rank']
                writer.writerow(row)
        
        
        

    
if __name__ == "__main__":
    '''Run locally to this script'''

    from pprint import pprint # pprint is cool
    #Pass arguments for name and platform
    parser = argparse.ArgumentParser(description='Scrape Commandline Options', add_help=True)
    parser.add_argument('-p', action='store', dest='platform', help='platform options. Example: steam', choices=('steam','psn','xbl'), default='steam')
    parser.add_argument('-g', action='store', dest='gamertag', help='your gamertag', default='Reasel')
    parser.add_argument('-l', action='store', dest='playerCsv', help='path to csv', default='False')

    results = parser.parse_args()
    platform = results.platform
    gamertag = results.gamertag
    playerCsv = results.playerCsv
    
    if(playerCsv != "False"):
        manyRun(playerCsv)
    else:
        singleRun(gamertag,platform)