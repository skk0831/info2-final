import pyxel
import csv

Items = []
window = 0
file_path = 'test.csv'
column_index = 0
x = ''
y = ''

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


def update():
    global Items, window, genre_key, x, y

    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
        # if 0 <= pyxel.mouse_x < 400 / 3:
        #     x = 0
        # elif 400 / 3 <= pyxel.mouse_x < 2 * 400 / 3:
        #     x = 1
        # else:
        #     x = 2
        # if 0 <= pyxel.mouse_y < 200 / 3:
        #     y = 0
        # elif 200 / 3 <= pyxel.mouse_y < 2 * 200 / 3:
        #     y = 1
        # else:
        #     y = 2
        if (40 <= pyxel.mouse_x < 400 ) and (35 <= pyxel.mouse_y < 65):
            genre_i = 0
        elif (40 <= pyxel.mouse_x < 400 ) and (65 <= pyxel.mouse_y < 95):
            genre_i = 1
        elif (40 <= pyxel.mouse_x < 400 ) and (95 <= pyxel.mouse_y < 125):
            genre_i = 2
        elif (40 <= pyxel.mouse_x < 400 ) and (125 <= pyxel.mouse_y < 155):
            genre_i = 3
        #genre_i = x * 3 + y  # x:列　y：行
        genre_key = Items[genre_i]
        window = 1

    if window == 0:
        Items = get_items_from_column(file_path, column_index)

    elif window == 1:
        Items = find_values_by_key(file_path, genre_key)


def draw():
    global x, y
    pyxel.cls(7)
    pyxel.text(10, 10, "window: " + str(window), 0)
    pyxel.text(10, 30, str(x) + ',' + str(y), 0)
    for i, j in enumerate(Items):
        #pyxel.text(i//3 * 60 + 30, i%3 * 60 + 30, str(j),0)
        pyxel.text(50, i * 30 + 50, str(j), 0)

pyxel.run(update, draw)