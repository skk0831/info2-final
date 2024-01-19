import pyxel
import csv
import random

Items = []
window = 0
index = 0
file_path = 'test.csv'
column_index = 0
x = ''
y = ''

class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class BDFRenderer:
    BORDER_DIRECTIONS = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]

    def __init__(self, bdf_filename):
        self.font_bounding_box = [0, 0, 0, 0]
        self.fonts = self._parse_bdf(bdf_filename)
        self.screen_ptr = pyxel.screen.data_ptr()
        self.screen_width = pyxel.width

    def _parse_bdf(self, bdf_filename):
        fonts = {}
        code = None
        bitmap = None
        dwidth = 0
        with open(bdf_filename, "r") as f:
            for line in f:
                if line.startswith("FONTBOUNDINGBOX"):
                    self.font_bounding_box = list(map(int, line.split()[1:]))
                elif line.startswith("ENCODING"):
                    code = int(line.split()[1])
                elif line.startswith("DWIDTH"):
                    dwidth = int(line.split()[1])
                elif line.startswith("BBX"):
                    bbx = tuple(map(int, line.split()[1:]))
                elif line.startswith("BITMAP"):
                    bitmap = []
                elif line.startswith("ENDCHAR"):
                    fonts[code] = (
                        dwidth,
                        bbx,
                        bitmap,
                    )
                    bitmap = None
                elif bitmap is not None:
                    hex_string = line.strip()
                    bin_string = bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)
                    bitmap.append(int(bin_string[::-1], 2))
        return fonts

    def _draw_font(self, x, y, font, color):
        dwidth, bbx, bitmap = font
        screen_ptr = self.screen_ptr
        screen_width = self.screen_width
        x = x + self.font_bounding_box[2] + bbx[2]
        y = y + self.font_bounding_box[1] + self.font_bounding_box[3] - bbx[1] - bbx[3]
        for j in range(bbx[1]):
            for i in range(bbx[0]):
                if (bitmap[j] >> i) & 1:
                    screen_ptr[(y + j) * screen_width + x + i] = color

    def draw_text(self, x, y, text, color=7, border_color=None, spacing=0):
        for char in text:
            code = ord(char)
            if code not in self.fonts:
                continue
            font = self.fonts[code]
            if border_color is not None:
                for dx, dy in self.BORDER_DIRECTIONS:
                    self._draw_font(
                        x + dx,
                        y + dy,
                        font,
                        border_color,
                    )
            self._draw_font(x, y, font, color)
            x += font[0] + spacing

def get_random_index(num):
    return random.randint(0, num)

def get_color(num):
    return random.randint(0, num)

def get_items_from_column(file_path, column_index):
    items = set()

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 1行目はヘッダーなのでスキップする
        for row in reader:
            if len(row) > column_index:  # 指定された列が存在するか確認
                items.add(row[column_index])

    return sorted(items)

def find_values_by_key(file_path, key):
    results = []
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーを読み飛ばす
        for row in reader:
            if row[0] == key:
                results.append((row[1], row[2]))
    return results


pyxel.init(400, 200)
pyxel.mouse(True)
umplus10 = BDFRenderer("assets/umplus_j10r.bdf")
umplus12 = BDFRenderer("assets/umplus_j12r.bdf")

def update():
    global Items, window, genre_key, x, y

    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
        if (40 <= pyxel.mouse_x < 400 ) and (35 <= pyxel.mouse_y < 65):
            genre_i = 0
        elif (40 <= pyxel.mouse_x < 400 ) and (65 <= pyxel.mouse_y < 95):
            genre_i = 1
        elif (40 <= pyxel.mouse_x < 400 ) and (95 <= pyxel.mouse_y < 125):
            genre_i = 2
        elif (40 <= pyxel.mouse_x < 400 ) and (125 <= pyxel.mouse_y < 155):
            genre_i = 3
        genre_key = Items[genre_i]
        window = 1

    if window == 0:
        Items = get_items_from_column(file_path, column_index)
        index = get_random_index(len(Items))

    elif window == 1:
        Items = find_values_by_key(file_path, genre_key)
        index = get_random_index(len(Items))
  
    if pyxel.btnp(pyxel.KEY_SHIFT):
        window = 0

def draw():
    global x, y
    pyxel.cls(7)
    clor=1
    pyxel.rect(0,0,400,200,clor)
    pyxel.text(10, 10, "window: " + str(window), 0)
    pyxel.text(10, 30, str(x) + ',' + str(y), 0)

    if window == 0:
        clor = 1
        pyxel.rect(0, 0, 400, 200, clor)
        for i, j in enumerate(Items):
            pyxel.text(50, i * 30 + 50, str(j), 8)
    else:
        clor = 3
        pyxel.rect(0, 0, 400, 200, clor)
        umplus10.draw_text(20, 50, str(Items[index][0]), 8)
        if pyxel.btn(pyxel.KEY_SPACE):
            pyxel.text(20, 70, str(Items[index][1]), 8)
    
pyxel.run(update, draw)
