import characterData
import addComicData
import pandas as pd
import time
import pandas as pd 


characterData = characterData.character
#reference https://raw.githubusercontent.com/skut21x-ga/mcu-api/master/lib/db/mcudata.json
#get the length of the characters list
numCharacters = len(characterData)
counter = 0
characterDict = {}
search_items = ['comic', 'game', 'movie', 'tv_series']
outputFileName = input("Enter in a csv output file (modernMCU.csv): ")
if(".csv" in outputFileName):
    print("Valid output file")
else:
    print("Please run program again and enter a valid output file")
    quit()

#Function gets characters real name   
def getName(characterItem):
    return characterItem['real_name']

#Function gets characters superhero name
def getAlias(characterItem):
    characterNicknames = (characterItem['alias'])
    aliasList = characterNicknames.split(", ")
    return aliasList[0]

#Function gets comic book appearances
def getComics(characterItem):
    return characterItem[search_items[0]]

#Function gets video game appearances
def getGames(characterItem):
    return characterItem[search_items[1]]

#Function gets movie appearances
def getMovies(characterItem):
    return characterItem[search_items[2]]

#Function gets tv show appearances
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

execution_1 = (time.time() - startTime)
print('completed operations on modern MCU data in seconds: ' + str(execution_1))

#Function creates a new character list by combining both data sets
def createList(newData):
    list_of_current_characters = list(characterDict.keys())
    tempList = []
    for x in list_of_current_characters:
        lowerName = x.lower()
        tempList.append(lowerName)
    list_of_comic_characters = list(newData.keys())
    #Gets of characters that is not present in the original list
    differences = (set(list_of_comic_characters) - set(tempList)).union(set(tempList) - set(list_of_comic_characters))
    #Gets a unique list of all characters
    mergedCharacterList = list(set(list(list_of_current_characters)+list(differences)))
    return mergedCharacterList, differences

#get data from excel file
expandedData = addComicData.expandNetwork()

newCharacterList, differenceList = createList(expandedData)
emptyDict = {}
#Function updates the names of characters in the connections dictionary
for i in newCharacterList:
    i.lower()
    connectionsDict.update({i:[]})
    emptyDict.update({i:0})

#Function adds the names of characters not in the dictionary to the list
#This is done in a way that there are no duplicates
for items in differenceList: 
    characterDict.update({items:[]})


execution_2 = (time.time() - startTime)
print('Retrieved, formatted comic book data and created list of all characters in seconds: ' + str(execution_2))

#Function merges that data from the two datasets into the one dataset
def mergeData(characterDict, dataDict):
    for c in dataDict:
        for x in characterDict:
            if x == c:
               items = characterDict[x]
               comicData = dataDict[c]
               mergedList = list(set(items+comicData))
               characterDict[x] = mergedList

mergeData(characterDict, expandedData)


execution_3 = (time.time() - startTime)
print('Merged two data sets in seconds: ' + str(execution_3))


# use characterDict to get characters and their appearances
characterList = list(characterDict.keys())

#algorithm to get characters list and create dictionary runs in 5n+19

#create a dataframe to store the characters and map their weights.
df = pd.DataFrame(columns=newCharacterList, index=newCharacterList)

#take the first name in the characters list
def commonCounter(a,b): 
    c = [value for value in a if value in b] 
    return len(c)

#Function iterates throughth list of characters and counts all their appearances with other characters
# in the MCU. It will then populate the dataframe accordingly
def countAppearances(minilist, fulllist):
    for marvelCharacter in minilist: #n^2
        currentCharacterAppears = characterDict[marvelCharacter]
        #iterate through the character dictionary on each character
        for singleCharacters in fulllist:
        #if the character name is not equal to the current name 
            if (marvelCharacter != singleCharacters): #n steps 
                MCUappearances = characterDict[singleCharacters]
                result = commonCounter(currentCharacterAppears,MCUappearances)
                value = connectionsDict[marvelCharacter]
                value.append(result)
                connectionsDict[marvelCharacter] = value
                df.at[marvelCharacter,singleCharacters]=result


#Function that runs program
def multithread():
    countAppearances(newCharacterList, newCharacterList)
    executionTime1 = (time.time() - startTime)
    print('Done threading in seconds: ' + str(executionTime1))
multithread()
#runs in n^2 + 2n+3 

#writes df to CSV
df.to_csv(outputFileName)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

