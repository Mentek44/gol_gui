#!/bin/python3
# mentek44 Nov21
# MIT LICENCE

###############################################################################
# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
###############################################################################
import time
from tkinter import *
import threading

###############################################################################
# globals
SIZE = 40
DEAD = "#000000"
ALIVE = "#FFFFFF"
RUN = True


###############################################################################


def main():
    global RUN
    global SIZE
    global DEAD
    global ALIVE
    root = Tk()
    root.title("test")

    frame = Frame()

    cur = gen_grid(frame)
    # cur[4][3].rezz()
    frame.pack(side="left")
    # cur = [[CellLabel(root).set_cell_data(c=c, r=r, val=0) for c in range(SIZE)] for r in range(SIZE)]
    # new = [[CellLabel(root).set_cell_data(c=c, r=r, val=0) for c in range(SIZE)] for r in range(SIZE)]

    # glider
    cur[0][1].rezz()
    cur[1][2].rezz()
    cur[2][0].rezz()
    cur[2][1].rezz()
    cur[2][2].rezz()

    control_frame = ControlFrame(master=root, cur=cur)
    control_frame.after(200, update_gol, control_frame, cur)
    # updater = threading.Thread(target=update_gol, args=(cur,))
    # updater.start()
    control_frame.mainloop()
    RUN = False


###############################################################################


def stop_game():
    global RUN
    RUN = False


def start_game(control_frame, cur):
    global RUN
    if not RUN:
        control_frame.after(200, update_gol, control_frame, cur)
        RUN = True


class ControlFrame(Frame):
    def __init__(self, master=None, cur=None):
        super(ControlFrame, self).__init__(master=master)
        self.master = master
        self.pack(side="right")
        self.create_widgets(cur=cur)

    def create_widgets(self, cur):
        self.count = Label(self)
        self.count["text"] = 0
        self.count.pack(side="top")

        self.btn_start = Button(self)
        self.btn_start["text"] = "Start"
        self.btn_start["command"] = lambda: start_game(self, cur)
        self.btn_start.pack(side="top")

        self.btn_stop = Button(self, text="Stop", command=stop_game)
        self.btn_stop.pack(side="top")

class Cell(object):
    r = 0
    c = 0
    alive = False

    def __init__(self, row, col, alive):
        self.r = row
        self.c = col
        self.alive = alive

    def set_cell_data(self, row, col, alive):
        self.r = row
        self.c = col
        self.alive = alive


class MyLabel(Label):
    alive = False

    def __init__(self, *args, **kwargs):
        self.alive = False
        super(MyLabel, self).__init__(*args, **kwargs)

    def die(self):
        global ALIVE
        global DEAD
        self.alive = False
        self.configure(bg=DEAD)

    def rezz(self):
        self.alive = True
        self.configure(bg=ALIVE)


###############################################################################
# cell pos getter

def has_left(cells: list[list[Cell]], cell: Cell) -> bool:
    r = cell.r
    c = cell.c - 1 if cell.c != 0 else None
    return (r is not None and c is not None) and cells[r][cell.c - 1].alive


def has_right(cells: list[list[Cell]], cell: Cell) -> bool:
    # checks if the provided cell has a right neighbour
    # returns True if there is indeed a right neighbour and no wall
    r = cell.r
    c = cell.c + 1 if cell.c + 1 < len(cells) else None
    return (r is not None and c is not None) and cells[r][cell.c + 1].alive


def has_top(cells: list[list[Cell]], cell: Cell) -> bool:
    r = cell.r - 1 if cell.r != 0 else None
    c = cell.c
    return (r is not None and c is not None) and cells[cell.r - 1][c].alive


def has_bot(cells: list[list[Cell]], cell: Cell) -> bool:
    r = cell.r + 1 if cell.r + 1 < len(cells) else None
    c = cell.c
    return (r is not None and c is not None) and cells[cell.r + 1][c].alive


def has_top_left(cells: list[list[Cell]], cell: Cell) -> bool:
    r = cell.r - 1 if cell.r != 0 else None
    c = cell.c - 1 if cell.c != 0 else None
    return (r is not None and c is not None) and cells[cell.r - 1][cell.c - 1].alive


def has_top_right(cells: list[list[Cell]], cell: Cell) -> bool:
    r = cell.r - 1 if cell.r != 0 else None
    c = cell.c + 1 if cell.c + 1 < len(cells) else None
    return (r is not None and c is not None) and cells[cell.r - 1][cell.c + 1].alive


def has_bot_left(cells: list[list[Cell]], cell: Cell) -> bool:
    r = cell.r + 1 if cell.r + 1 < len(cells) else None
    c = cell.c - 1 if cell.c != 0 else None
    return (r is not None and c is not None) and cells[cell.r + 1][cell.c - 1].alive


def has_bot_right(cells: list[list[Cell]], cell: Cell) -> bool:
    r = cell.r + 1 if cell.r + 1 < len(cells) else None
    c = cell.c + 1 if cell.c + 1 < len(cells) else None
    return (r is not None and c is not None) and cells[cell.r + 1][cell.c + 1].alive


###############################################################################
# define rules for next generation


def get_neighbour_count(cells: list[list[Cell]], cell: Cell) -> int:
    anc = 0
    if has_left(cells, cell):
        anc += 1
    if has_right(cells, cell):
        anc += 1
    if has_top(cells, cell):
        anc += 1
    if has_bot(cells, cell):
        anc += 1
    if has_bot_right(cells, cell):
        anc += 1
    if has_bot_left(cells, cell):
        anc += 1
    if has_top_right(cells, cell):
        anc += 1
    if has_top_left(cells, cell):
        anc += 1
    return anc


###############################################################################

def gen_next(old: list[list[Cell]], new: list[list[MyLabel]]) -> list[list[MyLabel]]:
    # new = [[Cell(row=r, col=c) for c in range(len(old))] for r in range(len(old))]
    for ri, r in enumerate(old):
        for ci, c in enumerate(r):
            # alive neighbour count
            anc = get_neighbour_count(old, c)
            # check for neighbours and create cell accordingly
            if c.alive:
                if anc > 3:  # DEAD
                    new[ri][ci].die()
                elif anc == 2 or anc == 3:  # ALIVE
                    new[ri][ci].rezz()
                elif anc < 2:  # DEAD
                    new[ri][ci].die()
            else:
                if anc == 3:  # ALIVE
                    new[ri][ci].rezz()
    return new


###############################################################################


def clone_cells(labels: list[list[MyLabel]]) -> list[list[Cell]]:
    cells = []
    for ri, r in enumerate(labels):
        cols = []
        for ci, c in enumerate(labels[ri]):
            # TODO clone data from label into some data structure
            cell = Cell(row=ri, col=ci, alive=c.alive)
            cols.append(cell)
        cells.append(cols)
    return cells


def update_gol(root: ControlFrame, cur: list[list[MyLabel]]):
    global RUN
    global ALIVE
    global DEAD
    if RUN:
        try:
            tmp_cell = clone_cells(cur)
            cur = gen_next(tmp_cell, new=cur)
            # time.sleep(0.2)
            root.count["text"] += 1
            root.after(200, update_gol, root, cur)
        except Exception as e:
            print(e)


def gen_grid(frame):
    cur = []
    for ri, r in enumerate(range(SIZE)):
        col = []
        for ci, c in enumerate(range(SIZE)):
            label = MyLabel(frame, width=4, height=2, bg=DEAD)
            label.grid(row=ri, column=ci, padx=1, pady=1)
            label.bind('<Button-1>', lambda e, lab=label: switch_state(lab))
            col.append(label)
        cur.append(col)
    return cur


def switch_state(cell: Label):
    if cell.alive:
        cell.die()
    else:
        cell.rezz()

###############################################################################


try:
    if __name__ == "__main__":
        main()
except Exception as e:
    RUN = False
    print(e)
