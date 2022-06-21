import pandas as pd
import pdfkit
import random, time, os
from lxml import etree, html


# A "FileScanner" will monitor a directory for files, allowing for easier processing of new tracklists
class FileScanner:
    def __init__(self,path):
        self.path = path
    #COMING SOON
    #TODO: Stuff


# A "TrackList" keep info on the source CSV file, and the parsed output of that file. Also provides shuffle feature
class TrackList:
    def __init__(self,name,filepath):
        self.name = name
        self.filepath = filepath
        self.df = self.read_file()
    def read_file(self):
        return pd.read_csv('dead_or_alive_.csv')
    def get_ArtistTrack(self):
        return ["{} - {}".format(self.df['Track Name'][id], self.df['Artist Name(s)'][id]) for id in range(len(self.df['Track Name']))]
    def get_suffled_ArtistTrack(self,count=0):
        out_tracklist = self.get_ArtistTrack()
        random.shuffle(out_tracklist)
        if count==0: return out_tracklist
        else: return out_tracklist[:count]

# A "Cell" is an individual boxe in the bingo grid
class Cell:
    def __init__(self,id,card, label=""):
        self.id = id
        self.label = label
        self.selected = False
        self.card = card
    def select_cell(self):
        self.selected = True
        self.card.check_bingo()
    def check(self,track_name):
        if not self.selected:
            if self.label == track_name: 
                self.select_cell()
                print("Selected {} on card {} at cell {}".format(track_name,self.card.id,self.id))
        
# A "Card" is All of the cells in a bingo grid as one
class Card:
    count = 0 # used for auto assigning an ID every time a new card is made.
    all_cards = []
    def __init__(self):
        self.id = Card.count # assign this card's ID as however many the count is set to.
        Card.count += 1      # then add one to the count, so the next ID is +1
        self.rows = 5        # how many cells to have in X (rows)
        self.cols = 5        # how many cells to have in Y (cols)
        self.cell_count = self.rows * self.cols 
        self.cells = [Cell(i, self) for i in range(self.cell_count)] # create a list of cells, one for each cell that is needed
        self.bingo = False   # used to tell if this card has bingo or not
        Card.all_cards.append(self)

    def id_to_xy(self, id):     # Standard ID to XY math
        return (id % self.rows, id // self.rows) # x is the remainder of id / row_count | y is the floor division of id / row_count

    def xy_to_id(self,xy):      # Standard XY to ID math
        x,y = xy                # unpack the xy 
        return y * self.rows + x  # each Y is a whole row, x is the remaining non-whole row. 

    def set_tracks(self,track_list):    # sets the cell labels to reflect a tracklist
        track_list = track_list[:self.cell_count]   # strip off any extra tracks that may have been given
        
        if len(track_list) != self.cell_count:      # if the count if too short
            print("Not enough tracks provided!")    # complain, then
            raise Exception                         # ask for help
        else:
            self.track_list = track_list
            for i in range(len(track_list)):        # for each element in the track_list
                self.cells[i].label = track_list[i] # set the label of the corresponding cell
    def get_tracks(self):
        return self.track_list
    def check_bingo(self):                          # used for checking if a card has bingo
        if not card.bingo:                          # if already has bingo, don't do anything
            rows = []                                # set up empty arry
            cols = []                                #
            diagonal = []
            reverse_diagonal = []
            new_bingo = False                           # set bingo flag to false
            bingo_rows = False                          # MOVE ALL THIS TO THE CARD, CONSIDER BINGO CLASS
            bingo_cols = False
            bingo_double_rows = False
            bingo_double_cols = False
            bingo_picture_frame = False
            bingo_diagonal = False
            bingo_double_diagonal = False
            bingo_rows_count = 0
            bingo_cols_count = 0
            
            for y in range(self.cols):              # for each col
                col = []
                row = []
                for x in range(self.rows):          # for each row
                    row.append(self.cells[self.xy_to_id((x,y))].selected)   # check normal coords (x, y) for rows
                    col.append(self.cells[self.xy_to_id((y,x))].selected)   # check backwards coords (y, x) for cols
                if all(row):                        # if rows is all true
                    bingo_rows = True               # Bingo! 
                    bingo_rows_count +=1            # add to count for double row checking
                if all(col):                        # if cols is all true
                    bingo_cols = True               # Bingo!
                    bingo_cols_count += 1           # add to count for double col checking
                rows.append(row)                    # append to row list
                cols.append(col)                    # append to col list
            for i in range(min(self.rows,self.cols)):   # check diagonal bingo
                diagonal.append(card.cells[card.xy_to_id((i,i))].selected)  # collect at (i,i)
                reverse_diagonal.append(card.cells[card.xy_to_id((i,card.rows-1-i))].selected) # collect at (i, max-1-i) 
            if all(diagonal) and all(reverse_diagonal): # check if double diagonal
                bingo_double_diagonal = True            # Bingo!
            if all(diagonal) or all(reverse_diagonal):  # check if single diagonal, either one
                bingo_diagonal = True                   # Bingo!
            if rows.count(True) > 1:                    # check if we have more than one row bingo
                bingo_double_rows = True                # Bingo!
            if cols.count(True) > 1:                    # check if we have more than one col bingo
                bingo_double_cols = True                # Bingo!
            if all(rows[0]) and all(rows[self.rows-1]) and all(cols[0]) and all(cols[self.cols-1]): # check for outer edges bingo
                bingo_picture_frame = True              # Bingo!
            
            if new_bingo:
                print("Bingo on card {}!".format(card.id))
                

        
    def write_html(self):
        head = ['<head>',
        '<link rel="stylesheet" href="styles.css">'
        '</head>'
        ]
        body = ['<body>']
        body.append('<div class="card">')
        for y in range(self.rows):
            body.append('<div class="row">')
            for x in range(self.cols):
                label = self.cells[self.xy_to_id((x,y))].label
                body.append('<div class="cell {}" >{}</div>'.format(card.get_fontsize_class(label),label))
            body.append('</div>')
        body.append('</div>')
        body.append('</body>')
        html_code = ['<html>'] + head + body +['</html>']
        document_root = html.fromstring("".join(html_code).replace("\n",""))
        pretty_code = etree.tostring(document_root, encoding='unicode', pretty_print=True)
        print(pretty_code)
        if not os.path.exists('html'): os.mkdir('html')
        with open(os.path.join('html','card_{:03d}.html'.format(self.id)), 'w') as f:
            f.writelines(pretty_code)
        
    
    def write_pdf_from_html(self):
        pdfkit.from_file(os.path.join('html','card_{:03d}.html'.format(card.id)), 'card_{:03d}.pdf'.format(card.id))

    def get_fontsize_class(self,text):
        if len(text) < 20: return "large"
        if len(text) < 30: return "medium"
        else: return "small"
               
    def print_cells(self):
        for y in range(self.cols):
            print("-"*self.rows*30)
            for x in range(self.rows):
                id = self.xy_to_id((x,y))
                cell = self.cells[id]
                label = cell.label[:30]
                # print("|({}, {}) = ID: {}|".format(x,y,id))
                print("|{: ^30}|".format(label),end="")
            print()

class CardStack:
    def __init__(self):
        self.cards = []
    def add_card(self,card):
        self.cards.append(card)





    
# ACTUAL CODE THAT DOES THE STUFF
    

track_list = TrackList("Dead Or Alive","dead_or_alive_.csv")

num_cards = 10 #number of cards to generate
cards = []


for card_id in range(num_cards):
    this_track_list = track_list.get_suffled_ArtistTrack()
    this_tracks_string = "".join(this_track_list)
    valid_new_card = True
    for othercard in Card.all_cards:
        other_tracks_string = "".join(othercard.track_list)
        if this_tracks_string == other_tracks_string:
            valid_new_card = False
            print("This card already exists!")
    if valid_new_card:
        card = Card()
        card.set_tracks(this_track_list)
        cards.append(card)

for card in cards:
    card.write_html()
    # card.write_pdf_from_html() # not working :(