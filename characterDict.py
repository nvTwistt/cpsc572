import json
import characters
import addData
import pandas as pd
import time
from numpy import empty
from numpy.lib.arraysetops import unique
import openpyxl
import pandas as pd 
import numpy as np
import math
import itertools
import multiprocessing
import csv
characterData = characters.character
#reference https://raw.githubusercontent.com/skut21x-ga/mcu-api/master/lib/db/mcudata.json
#get the length of the characters list
numCharacters = len(characterData)
counter = 0
characterDict = {}
search_items = ['comic', 'game', 'movie', 'tv_series']

def getName(characterItem):
    return characterItem['real_name']
def getAlias(characterItem):
    characterNicknames = (characterItem['alias'])
    aliasList = characterNicknames.split(", ")
    return aliasList[0]

def getComics(characterItem):
    return characterItem[search_items[0]]

def getGames(characterItem):
    return characterItem[search_items[1]]


def getMovies(characterItem):
    return characterItem[search_items[2]]

def getTv(characterItem):
    return characterItem[search_items[3]]

#https://www.geeksforgeeks.org/how-to-remove-text-inside-brackets-in-python/
def cleanList(string):
    paren= 0
    result=''
    for ch in string:
      
    # if the character is ( then increment the paren
    # and add ( to the resultant string.
        if ch == '(':
            paren =paren+ 1
            result = result + '('
      
    # if the character is ) and paren is greater than 0, 
    # then increment the paren and 
    # add ) to the resultant string.
        elif (ch == ')') and paren:
            result = result + ')'
            paren =paren- 1
      
    # if the character neither ( nor  then add it to
    # resultant string.
        elif not paren:
            result += ch
    return result

def identifyGame(games):
    gameList = []
    for game in games:
        gameName = game + '-game'
        gameList.append(gameName)
    return gameList

def getAppearances(characterItem):
    appearanceList = []
    characterComic = getComics(characterItem)
    characterGame = getGames(characterItem)
    characterMovie = getMovies(characterItem)
    characterTv = getTv(characterItem)
    if (characterComic != "NA"):
        comics = characterComic.split(", ")
        appearanceList.extend(comics)
    if (characterGame != "NA"):
        #create function that adds "game" to the end of it so that there are no duplicates
        games = characterGame.split(", ")
        identifiedGames = identifyGame(games)
        appearanceList.extend(identifiedGames)
        
    if (characterMovie != "NA"):
        movies = []
        multiMovie = []
        if ',' in characterMovie:
            movies = characterMovie.split(", ")
            appearanceList.extend(movies)
        else:    
            multiMovie = cleanList(characterMovie);
            multiMovie = multiMovie.split("()")
            appearanceList.extend(multiMovie);
        if (getName(characterItem) == "Adolf Hitler"):
            print(multiMovie)
            while("" in multiMovie) :
                multiMovie.remove("")
            print(multiMovie)
    if (characterTv != "NA"):
        cleanedString = cleanList(characterTv)
        shows = cleanedString.split("()")
        appearanceList.extend(shows)
    while("" in appearanceList) :
        appearanceList.remove("")
    return appearanceList



#iterate through the list and get the names of all characters
counter = 0
#start time
startTime = time.time()
connectionsDict = {}
for c in characterData:
    characterAlias = getAlias(c) #n+3
    characterName = getName(c) #n
    appearances = getAppearances(c) #n+5+3+10+4+n = 2n+19
    name = ""
    if (characterAlias != "NA"):
        characterDict.update({characterAlias:appearances}) # n+1
        
    # counter is used to stop it early for testing purposes.
    #if counter == 7:
    #    break
    #counter+=1

execution_1 = (time.time() - startTime)
print('completed operations on modern MCU data in seconds: ' + str(execution_1))

def createList(newData):
    list_of_current_characters = list(characterDict.keys())
    tempList = []
    for x in list_of_current_characters:
        lowerName = x.lower()
        tempList.append(lowerName)
    list_of_comic_characters = list(newData.keys())
    differences = (set(list_of_comic_characters) - set(tempList)).union(set(tempList) - set(list_of_comic_characters))
    mergedCharacterList = list(set(list(list_of_current_characters)+list(differences)))
    return mergedCharacterList, differences

#get data from excel file
expandedData = addData.expandNetwork()

newCharacterList, differenceList = createList(expandedData)

for i in newCharacterList:
#for i in characterDict.keys():
    connectionsDict.update({i:[]})

for items in differenceList: 
    characterDict.update({items:[]})

# dataSize = len(expandedData)

execution_2 = (time.time() - startTime)
print('Retrieved, formatted comic book data and created list of all characters in seconds: ' + str(execution_2))

def mergeData(characterDict, dataDict):
    #print(dataDict)
    for c in dataDict:
    #print(c)
    # if counter_1  == 3:
    #     break
    # counter_1 +=1
        for x in characterDict:
            #name = x.lower()
            #if c == 'scatterbrain' and name == 'scatterbrain': 
                #print(dataDict[c])
                #print(characterDict[x])
            if x == c:
               items = characterDict[x]
               comicData = dataDict[c]
               mergedList = list(set(items+comicData))
               characterDict[x] = mergedList

mergeData(characterDict, expandedData)


execution_3 = (time.time() - startTime)
print('Merged two data sets in seconds: ' + str(execution_3))
#print(type(newCharacterList))

# use characterDict to get characters and their appearances
characterList = list(characterDict.keys())

#algorithm to get characters list and create dictionary runs in 5n+19

#create a dataframe to store the characters and map their weights.
df = pd.DataFrame(columns=newCharacterList, index=newCharacterList)
#df = pd.DataFrame(columns=characterDict.keys(), index=characterDict.keys())
#print(df.head())
#take the first name in the characters list

def commonCounter(a,b): 
    c = [value for value in a if value in b] 
    return len(c)

def countAppearances(minilist, fulllist):
    for marvelCharacter in minilist: #n^2
        currentCharacterAppears = characterDict[marvelCharacter]
        #print("current character is: ", marvelCharacter, " appears in: ", currentCharacterAppears)
        #iterate through the character dictionary on each character
        for singleCharacters in fulllist:
        #if the character name is not equal to the current name 
            if (marvelCharacter != singleCharacters): #n steps 
                MCUappearances = characterDict[singleCharacters]
                result = commonCounter(currentCharacterAppears,MCUappearances)
                #print("character: ", singleCharacters, "appear: " , MCUappearances)
                value = connectionsDict[marvelCharacter]
                value.append(result)
                connectionsDict[marvelCharacter] = value
                df.at[marvelCharacter,singleCharacters]=result


def multithread():
    countAppearances(newCharacterList, newCharacterList)
    #countAppearances(characterDict.keys(), characterDict.keys())
    executionTime1 = (time.time() - startTime)
    print('Done threading in seconds: ' + str(executionTime1))
#countAppearances(newCharacterList)
multithread()
#runs in n^2 + 2n+3 

df.to_csv('FullMCU.csv')
#df.to_excel (r'C:\Users\mtamk\OneDrive\Documents\SB2\Fall21\cpsc572', index = False, header=True)
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

