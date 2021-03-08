# coding ~utf-8
"""

Author: Louai KB

"""

import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)

logo = Image.open('photos/genome.png')
genome_compression_logo = ImageTk.PhotoImage(logo)
genome_compression_logo_label = tk.Label(image=genome_compression_logo)
genome_compression_logo_label.image = genome_compression_logo
genome_compression_logo_label.grid(row=0, column=1)

# buttons
compression_text = tk.StringVar()
compression_button = tk.Button(root,
                               textvariable=compression_text,
                               bg='#53a6ba',
                               fg='white',
                               font='Raleway',
                               height=2,
                               width=15,
                               bd=0.3)
compression_text.set('Decompress')
compression_button.place(x=60, y=250)

decompression_text = tk.StringVar()
decompression_button = tk.Button(root,
                               textvariable=decompression_text,
                               bg='#53a6ba',
                               fg='white',
                               font='Raleway',
                               height=2,
                               width=15,
                               bd=0.3)
decompression_text.set('Compress')
decompression_button.place(x=320, y=250)

quit_text = tk.StringVar()
quit_button = tk.Button(root,
                        textvariable=quit_text,
                        bg='#d07b1a',
                        fg='white',
                        font='Raleway',
                        height=2,
                        width=15,
                        bd=0.3,
                        command=root.quit)
quit_text.set('Quit')
quit_button.place(x=590, y=250)


canvas = tk.Canvas(root, width=600, height=200)
canvas.grid(columnspan=3)

root.mainloop()