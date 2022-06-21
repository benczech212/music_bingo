import pandas as pd
import random, time, os, pdfkit
from lxml import etree, html
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors


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
        if count==0: return random.shuffle(self.get_ArtistTrack())
        else: return random.shuffle(self.get_ArtistTrack())[:count]

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
    def id_to_xy(self, id):
        return (id % self.rows, id // self.rows)

    def xy_to_id(self,xy):
        x,y = xy
        return y * self.rows + x

    def set_tracks(self,track_list):
        track_list = track_list[:self.cell_count]
        for i in range(len(track_list)):
            self.cells[i].label = track_list[i]

    def check_bingo(self):
        if not card.bingo:
            row = []
            col = []
            bingo = False
            for y in range(self.cols):
                for x in range(self.rows):
                    row.append(self.cells[self.xy_to_id((x,y))].selected)
                    col.append(self.cells[self.xy_to_id((y,x))].selected)
                if all(row) or all(col):
                    bingo = True
            if bingo:
                print("Bingo on card {}!".format(card.id))
                self.bingo = bingo

    def create_table_list(self):
        return [[self.cells[self.xy_to_id((x,y))].label for x in range(self.cols)] for y in range(self.rows)]
        
    def write_html(self):
        head = ['<link rel="stylesheet" href="styles.css">']
        body = []
        body.append('<div class="card">')
        for y in range(self.rows):
            body.append('<div class="row">')
            for x in range(self.cols):
                label = self.cells[self.xy_to_id((x,y))].label
                body.append('<div class="cell {}" >{}</div>'.format(card.get_fontsize_class(label),label))
            body.append('</div>')
        body.append('</div>')
        html_code = head + body
        document_root = html.fromstring(html_code)
        pretty_code = etree.tostring(document_root, encoding='unicode', pretty_print=True)
        print(pretty_code)
        with open('card_{:03d}.html'.format(self.id), 'w') as f:
            f.writelines(pretty_code)
        idx = 0
        pdfkit.from_file('card_{:03d}.html'.format(idx), 'card_{:03d}.pdf'.format(idx))

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
            




    
  
    

track_list = TrackList("Dead Or Alive","dead_or_alive_.csv")

num_cards = 10
cards = []
unique_list = []
for card_id in range(num_cards):
    this_track_list = track_list
    valid = False
    while not valid:
        random.shuffle(this_track_list)
        if str(this_track_list) not in unique_list:
            valid = True        
            unique_list.append(str(this_track_list))
        else:
            print(this_track_list + "Already in list")
    card = Card()
    card.set_tracks(this_track_list)
    cards.append(card)
for card in cards:
    write_html(card)