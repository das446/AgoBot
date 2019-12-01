import csv

games = []           #List to contain board game objects

class BoardGame:
    def __init__(self, name, shelf, sticker, opened, player_num, game_type, duration, notes, year, condition):
        #Initialize game data
        self.name = name
        self.shelf = shelf
        self.sticker = sticker
        self.opened = opened
        self.player_num = player_num
        self.type = game_type
        self.duration = duration
        self.notes = notes
        self.year = year
        self.condition = condition

#Read Excel file and create an object for each new game+ in the list
def ReadGames():
    with open('BoardGames.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            new_game = BoardGame(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            games.append(new_game)
            

#Take in search parameters and look through list of board game items to see if any matches
def SearchBoardGames(filters):
    filters = str(filters)
    if len(filter) < 2:                                #If search parameter only has 1 or fewer letter, search for games that starts with that letter
        for i in games:
            if i.name.lower().startswith(filters.lower()):
                print(i.name)
    else:    
        for i in games:
            if filters.lower() in i.name.lower():
                print(i.name) 