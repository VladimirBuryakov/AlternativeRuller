import tkinter as tk
from tkinter import Scale, Button, Text, Scrollbar

import os
import sys

selected_cell = None
class VRuler(tk.Canvas):
    '''Vertical Ruler'''

    def __init__(self, master, width, height, offset=0):
        super().__init__(master, width=width, height=height)
        self.offset = offset

        step = 10

        for y in range(step, height, step):
            if y % 50 == 0:
                self.create_line(0, y, 13, y, width=2)
                self.create_text(20, y, text=str(y/50), angle=90)
            else:
                self.create_line(2, y, 7, y)

        self.position = self.create_line(0, 0, 50, 0, fill='red', width=2)
        self.highlight_line = None

    def set_mouse_position(self, y):
        y -= self.offset
        self.coords(self.position, 0, y, 50, y)

    def highlight_vertical_line(self, y1, y2):
        if self.highlight_line:
            self.delete(self.highlight_line)
        self.highlight_line = self.create_line(0, y1, 0, y2, fill='green', width=15)

    def clear_highlight_vertical_line(self):
        if self.highlight_line:
            self.delete(self.highlight_line)
            self.highlight_line = None



class HRuler(tk.Canvas):
    '''Horizontal Ruler'''

    def __init__(self, master, width, height, offset=0):
        super().__init__(master, width=width, height=height)
        self.offset = offset

        step = 10
        for x in range(step, width, step):
            if x % 50 == 0:

                self.create_line(x, 0, x, 13, width=2)
                self.create_text(x, 20, text=str(x/50))
            else:
                self.create_line((x, 2), (x, 7))

        self.position = self.create_line(0, 0, 0, 50, fill='red', width=2)
        self.highlight_line = None

    def set_mouse_position(self, x):
        x -= self.offset
        self.coords(self.position, x, 0, x, 50)

    def highlight_horizontal_line(self, x1, x2):
        if self.highlight_line:
            self.delete(self.highlight_line)
        self.highlight_line =self.create_line(x1, 0, x2, 0, fill='green', width=15)

    def clear_highlight_horizontal_line(self):
        if self.highlight_line:
            self.delete(self.highlight_line)
            self.highlight_line = None


def motion(event):
    x, y = event.x, event.y
    hr.set_mouse_position(x)
    vr.set_mouse_position(y)

def click(event):
    global selected_cell

    if selected_cell:
        c.itemconfigure(selected_cell, fill='white')

    x, y = event.x - table_offset_x, event.y - table_offset_y
    x = x // cell_width
    y = y // cell_height

    selected_cell = c.create_rectangle(table_offset_x + x * cell_width, table_offset_y + y * cell_height,
                                       table_offset_x + (x + 1) * cell_width, table_offset_y + (y + 1) * cell_height,
                                       fill='green')

    vr.clear_highlight_vertical_line()
    hr.clear_highlight_horizontal_line()

    vr.highlight_vertical_line(table_offset_y + y * cell_height,table_offset_y + (y + 1) * cell_height)
    hr.highlight_horizontal_line(table_offset_x + x * cell_width, table_offset_x +(x + 1) * cell_width)
    print_text(f"Выбрана ячейка ({x}, {y})")
    print_text(f'Размер ячейки {(((y+1) * cell_height)-(y * cell_height))/50}cm на {(((x + 1) * cell_width)-(x * cell_width))/50}cm ')
    print_text('---------------------')

def print_text(text):
    text_widget.insert('end', text + '\n')

def on_width_scale_change(value):
    global cell_width
    cell_width = int(value)

    # Очистка сетки таблицы
    c.delete("table")

    for x in range(0, rows):
        for y in range(0, strings):
            x1 = table_offset_x + x * cell_width
            y1 = table_offset_y + y * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            c.create_rectangle(x1, y1, x2, y2, outline='black', tags="table")

def on_height_scale_change(value):
    global cell_height
    cell_height = int(value)

    c.delete("table")

    for x in range(0, rows):
        for y in range(0, strings):
            x1 = table_offset_x + x * cell_width
            y1 = table_offset_y + y * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            c.create_rectangle(x1, y1, x2, y2, outline='black', tags="table")

def restart_application():
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == "__main__":
    rows = 15
    strings = 8
    cell_width = 75
    cell_height = 40
    table_offset_x = 35
    table_offset_y = 35

    root = tk.Tk()
    root.geometry(f"1280x720")
    root.resizable(False, False)
    root['bg'] = 'white'

    vr = VRuler(root, 25, 720)
    vr.place(x=0, y=28)

    hr = HRuler(root, 1280, 25)
    hr.place(x=28, y=0)

    c = tk.Canvas(root, width=1280, height=720, bg='white')
    c.place(x=28, y=28)

    width_scale = Scale(root, from_=10, to=100, orient="horizontal", command=on_width_scale_change)
    width_scale.set(cell_width)  # Установка начального значения ползунка ширины
    width_scale.place(x=60, y=650)

    height_scale = Scale(root, from_=10, to=100, orient="horizontal", command=on_height_scale_change)
    height_scale.set(cell_height)  # Установка начального значения ползунка высоты
    height_scale.place(x=60, y=600)

    restart_button = Button(root, text="Обновить экран", command=restart_application)
    restart_button.place(x=1100, y=650)

    text_widget = Text(root, width=50, height=10)
    text_widget.place(x=450, y=520)

    # Создание вертикального скроллбара
    scrollbar = Scrollbar(root, command=text_widget.yview)
    scrollbar.place(x=850, y=520, height=175)
    text_widget.config(yscrollcommand=scrollbar.set)

    # for x in range(0, rows):
    #     for y in range(0, strings):
    #         x1 = x * cell_width + table_offset_x
    #         y1 = y * cell_height + table_offset_y
    #         x2 = x1 + cell_width
    #         y2 = y1 + cell_height
    #         c.create_rectangle(x1, y1, x2, y2, outline='black')

    c.bind('<Motion>', motion)
    c.bind('<Button-1>', click)

    root.mainloop()
