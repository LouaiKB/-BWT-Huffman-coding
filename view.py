# coding ~utf-8
"""

Author: Louai KB

"""

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
from PIL import Image
from PIL import ImageTk
from Bio import SeqIO
from bwt import Bwt


def open_fasta_file():
    compression_text.set('loading...')
    file = askopenfile(parent=root, mode='r', title='Choose genome file')
    if file:
        #sequence = SeqIO.read(file, 'fasta').seq + '$'
        text_box = tk.Text(root, height=100, width=50, padx=20, pady=10)
        for i in Bwt.bwt_construction_matrix('ATCATCATATCATGCA$'):
            text_box.insert('end', i + '\n')
            text_box.tag_configure('center', justify='center')
            text_box.tag_add('center', 1.0, 'end')
            text_box.grid(column=1, row=3)
        compression_text.set('Compress')
            


root = tk.Tk()
root.geometry('800x500')
canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)

logo = Image.open('photos/genome.png')
genome_compression_logo = ImageTk.PhotoImage(logo)
genome_compression_logo_label = tk.Label(image=genome_compression_logo)
genome_compression_logo_label.image = genome_compression_logo
genome_compression_logo_label.grid(row=0, column=1)

# buttons

decompression_text = tk.StringVar()
decompression_button = tk.Button(root,
                               textvariable=decompression_text,
                               bg='#53a6ba',
                               fg='white',
                               font='Raleway',
                               height=2,
                               width=15,
                               bd=0.3)
decompression_text.set('Decompress')
decompression_button.place(x=60, y=250)

compression_text = tk.StringVar()
compression_button = tk.Button(root,
                               textvariable=compression_text,
                               bg='#53a6ba',
                               fg='white',
                               font='Raleway',
                               height=2,
                               width=15,
                               bd=0.3,
                               command=open_fasta_file)
compression_text.set('Compress')
compression_button.place(x=320, y=250)

full_compression_text = tk.StringVar()
full_compression_button = tk.Button(root,
                        textvariable=full_compression_text,
                        bg='#53a6ba',
                        fg='white',
                        font='Raleway',
                        height=2,
                        width=15,
                        bd=0.3
                        )

full_compression_text.set('Full Compression')
full_compression_button.place(x=590, y=250)

bwt_transform_text = tk.StringVar()
bwt_transform_button = tk.Button(root,
                                 textvariable=bwt_transform_text,
                                 bg='#53a6ba',
                                 fg='white',
                                 font='Raleway',
                                 height=2,
                                 width=15,
                                 bd=0.3
                                )

bwt_transform_text.set('Bwt transform')
bwt_transform_button.place(x=60, y=350)

bwt_retransform_text = tk.StringVar()
bwt_retransform_button = tk.Button(root,
                                   textvariable=bwt_retransform_text,
                                   bg='#53a6ba',
                                   fg='white',
                                   font='Raleway',
                                   height=2,
                                   width=15,
                                   bd=0.3)

bwt_retransform_text.set('Bwt retransform')
bwt_retransform_button.place(x=320, y=350)

full_decompression = tk.StringVar()
full_decompression_button = tk.Button(root,
                                   textvariable=full_decompression,
                                   bg='#53a6ba',
                                   fg='white',
                                   font='Raleway',
                                   height=2,
                                   width=15,
                                   bd=0.3)

full_decompression.set('Full decompression')
full_decompression_button.place(x=590, y=350)

quit_text = tk.StringVar()
quit_button = tk.Button(root,
                        textvariable=quit_text,
                        bg='#d07b1a',
                        fg='white',
                        font='Raleway',
                        height=2,
                        width=20,
                        bd=0.3,
                        command=root.quit)

quit_text.set('Quit')
quit_button.place(x=389, y=460, anchor='center')

# canvas = tk.Canvas(root, width=600, height=200, bg='red')
# canvas.place(relx=0.5, rely=2.0, anchor='s')

root.mainloop()