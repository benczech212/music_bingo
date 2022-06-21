import pandas as pd
import random, time, os, pdfkit
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
            



class Card:
    count = 0
    def __init__(self):
        self.id = Card.count
        Card.count += 1
        self.rows = 5
        self.cols = 5
        self.cell_count = self.rows * self.cols
        self.cells = [Cell(i, self) for i in range(self.cell_count)]
        self.bingo = False
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
            



def get_fontsize_class(text):
    if len(text) < 20: return "large"
    if len(text) < 30: return "medium"
    else: return "small"
    
        
def write_html(card):
    css = [
    '<style>',
    '.small{font-size:8pt; line-height: 10pt;}',
    '.medium{font-size:12pt; line-height: 14pt;}',
    '.large{font-size:16pt; line-height: 18pt;}',

    '.card{',
    'border:1px solid black;',
    '}',
    '.row {',
    'display: flex;',
    'flex-wrap: nowrap;',
    '}',
    '.cell {',
    "border: 1px solid black;",
    "width: 25vw;",
    "height: 10vw;",
    "padding: 10px;",
    "margin: 1px;",
    "text-align: center;",
    "vertical-align: middle;",
    "align-items: center;",
    "justify-content: center;",
    "display: flex;",
    "align-content: center;",
    "flex-wrap: nowrap;",
    "flex-direction: row;",
    "overflow: hidden;",
        '}',
    '</style>',
    ]
    body = []
    body.append('<div class="card">')
    for y in range(card.rows):
        body.append('<div class="row">')
        for x in range(card.cols):
            label = card.cells[card.xy_to_id((x,y))].label
            body.append('<div class="cell {}" >{}</div>'.format(get_fontsize_class(label),label))
        body.append('</div>')
    body.append('</div>')
    html_code = css + body
    print(html_code)
    with open('card_{:03d}.html'.format(card.id), 'w') as f:
        f.writelines(html_code)
    idx = 0
    pdfkit.from_file('card_{:03d}.html'.format(idx), 'card_{:03d}.pdf'.format(idx))
    


def get_track_list():
    df = pd.read_csv('dead_or_alive_.csv')
    return ["{} - {}".format(df['Track Name'][id], df['Artist Name(s)'][id]) for id in range(len(df['Track Name']))]

track_list = get_track_list()
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
    # create_table(card, card.create_table_list())


# game_count = 100
# for game in range(game_count):
#     print("Game #{}".format(game))
#     bingo_order = track_list
#     random.shuffle(bingo_order)
#     bingo_after = 0
#     for song_num, track_name in enumerate(bingo_order):
#         print("Song number {} - {}".format(song_num,track_name))
#         for card in cards:
#             for cell in card.cells:
#                 cell.check(track_name)
#             # if card.bingo:
#             #     bingo_after = song_num
#             #     break
#                     # print("{} on card {} at cell {}".format(track,card.id,cell.id))

