import pandas as pd
#data found at https://www.kaggle.com/csanhueza/the-marvel-universe-social-network/version/1?select=nodes.csv

#populate the dict with all the names



def formatName(name):
    name = name.lower()
    nameList = name.split(", ")
    #print(nameList)
    if(len(nameList)) == 2:
        formattedName = nameList[1] + " " + nameList[0]
        return formattedName
    elif(len(nameList)) == 1:
        slashSplit = nameList[0].split("/")
        if len(slashSplit) == 2:
            formattedName = slashSplit[0]
            return formattedName
        else:
            formattedName = slashSplit[0]
            return formattedName
    
def expandNetwork():
    df = pd.read_csv('mcuComics.csv', names=['Names', 'Appears'])
    #create a dictionary and add all names as keys and empty list as its value
    characterDict = {}
    for index, row in df.iterrows():
    #print(row['Names'], row['Appears'])
        name = formatName(row['Names'])
        appearsIn = row['Appears']
        characters = list(characterDict.keys())
        if len(characters) == 0:
            characterDict.update({name:[appearsIn]})
        elif name not in characters:
            characterDict.update({name:[appearsIn]})
        elif name in characters:
            items = characterDict[name]
            items.append(appearsIn)
            characterDict[name] = items
        #counter = 0
        # if counter == 10:
        #     break
        # counter += 1
    return characterDict
