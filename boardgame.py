import csv

class BoardGame:
    def __init__(self):
        #Initialize game data
        self.name = list()
        self.shelf = list()
        self.sticker = list()
        self.opened = list()
        self.player_num = list()
        self.type = list()
        self.duration = list() 
        self.something = list()     #I dont know what this column is, it just says LGBN/Popular/Chelsea/Classic/Played/Expansion
        self.year = list()
        self.condition = list() 

        #Look through the Excel file to add game datas into lists
        with open("BoardGames.csv") as csvDataFile: 
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                self.name.append(row[0])
                self.shelf.append(row[1])
                self.sticker.append(row[2])
                self.opened.append(row[3])
                self.player_num.append(row[4])
                self.type.append(row[5])
                self.duration.append(row[6])
                self.something.append(row[7])
                self.year.append(row[8])
                self.condition.append(row[9])

    #Take in a search parameter, read the file to get all the game information, then put all the game names into boardgames variable. Compare game name with filter to see if any game contains the filter, then print it out
    def RandomBoardGames(self, filters):
        filters = str(filters)
        for i in self.name:
            if filters in str(i).lower():
                print(i)
