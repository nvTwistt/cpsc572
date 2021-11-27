import csv
g= open("marvel_edge_list2.csv","w+",encoding='utf-8')
f= open("marvel_node_list2.csv","w+",encoding='utf-8')
with open('C:/Users/harol/Documents/CPSC572/marvelData.csv', encoding='utf-8') as info:
    reader = csv.reader(info, delimiter=',')
    topRow = list()
    first = True
    g.write("Source,Target,Weight\n")
    f.write("ID,label\n")
    for row in reader:
        if first == False:
            blankFound = False
            for i in range(len(row)):
                if i != 0 and blankFound == True:
                    if int(row[i]) > 0:
                        g.write(str(topRow.index(row[0])-1) + "," + str(topRow.index(topRow[i])-1) + "," + str(row[i]) + "\n")
                if row[i] == '':
                    blankFound = True
        else:
            first = False
            topRow = row
            for i in range(len(row)):
                if row[i] != '':
                    f.write(str(i-1) + "," + str(row[i]) + "\n")
    f.close()
    g.close()