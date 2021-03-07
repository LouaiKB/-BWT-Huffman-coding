# coding ~utf-8
"""

Author: Louai KB

"""

from tkinter import Tk
from tkinter import ttk

root = Tk()

root.title('test modern GUI!')

button_ttk = ttk.Button(root, text='new ttk button').pack()

root.mainloop()

class View(Tk):
    pass