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


class View:

    def __init__(self, root):
        self.root = root
        self.button_dict = {}
    
    def setup_main_interface(self) -> None:
        
        self.canvas_for_padding = tk.Canvas(self.root,  width=600, height=300)
        self.canvas_for_padding.grid(columnspan=3, rowspan=3)
        
        logo = Image.open('photos/genome.png')
        self.genome_compression_logo = ImageTk.PhotoImage(logo)
        self.genome_compression_logo_label = tk.Label(image=self.genome_compression_logo)
        self.genome_compression_logo_label.image = self.genome_compression_logo
        self.genome_compression_logo_label.grid(row=0, column=1)

    def create_buttons(self, buttons_informations : dict ):
        self.button_dict = buttons_informations
        for key, value in self.button_dict.items():
            button_text = tk.StringVar()
            button = tk.Button(self.root,
                               textvariable=button_text,
                               bg='#53a6ba',
                               fg='white',
                               font='Raleway',
                               height=2,
                               width=15,
                               bd=0.3)
            button_text.set(key)
            button.place(x=value[0], y=value[1])

            if key == 'Quit':
                button.configure(bg='#d07b1a', width=20)
                button.place_configure(anchor='center')

    def main_loop(self):
        self.root.mainloop()

# def open_fasta_file():
#     compression_text.set('loading...')
#     file = askopenfile(parent=root, mode='r', title='Choose genome file')
#     if file:
#         #sequence = SeqIO.read(file, 'fasta').seq + '$'
#         text_box = tk.Text(root, height=100, width=50, padx=20, pady=10)
#         for i in Bwt.bwt_construction_matrix('ATCATCATATCATGCA$'):
#             text_box.insert('end', i + '\n')
#             text_box.tag_configure('center', justify='center')
#             text_box.tag_add('center', 1.0, 'end')
#             text_box.grid(column=1, row=3)
#         compression_text.set('Compress')
            
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('800x500')

    dictt = {
            "Compress": (60, 250), 
            "Decompress": (320, 250), 
            "Full compression": (590, 250), 
            "Bwt encryption": (60, 350), 
            "Bwt decryption": (320, 350),
            "Full decompression": (590, 350),
            "Quit": (389, 460)}

    obj = View(root)
    obj.setup_main_interface()
    obj.create_buttons(dictt)
    obj.main_loop()