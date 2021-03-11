# coding ~utf-8
"""

Author: Louai KB

"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.messagebox import showinfo
from PIL import Image
from PIL import ImageTk
from Bio import SeqIO
from bwt import Bwt
from controller import Controller


class PlaceImage:

    @staticmethod
    def place_image(root):
        root.geometry('800x500')
        canvas_for_padding = tk.Canvas(root, width=600, height=300)
        canvas_for_padding.grid(columnspan=3, rowspan=3)
        logo = Image.open('photos/genome.png')
        genome_compression_logo = ImageTk.PhotoImage(logo)
        genome_compression_logo_label = tk.Label(root, image=genome_compression_logo)
        genome_compression_logo_label.image = genome_compression_logo
        genome_compression_logo_label.grid(row=0, column=1)

class View(tk.Tk):

    def __init__(self):
        super().__init__()
        self.controller = None
        self.button_dict = {
            "Compress": (60, 250), 
            "Decompress": (320, 250), 
            "Full compression": (590, 250), 
            "Bwt encryption": (60, 350), 
            "Bwt decryption": (320, 350),
            "Full decompression": (590, 350),
            "Quit": (389, 460)
        }

    def setup_main_interface(self) -> None:
         PlaceImage.place_image(self)

    def create_buttons(self) -> None:
        for key, value in self.button_dict.items():
            button_text = tk.StringVar()
            button = tk.Button(self,
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
                button.configure(bg='#d07b1a', width=20, command=self.quit)
                button.place_configure(anchor='center')

            elif key == 'Compress':
                button.configure(command=self.compression)

            elif key == 'Decompress':
                pass

            elif key == 'Full compression':
                pass

            elif key == 'Bwt encryption':
                pass

            elif key == 'Bwt decrytpion':
                pass

            elif key == 'Full decompression':
                pass


        
    def compression(self):
        global results
        global top
        global next_button
        global next_button_text

        file = askopenfile(parent=self, mode='r', title='choose a file', 
                          filetypes=(('Text files', '*.txt'), ('Fasta file', '*.fasta')))
        
        top = tk.Toplevel()
        PlaceImage.place_image(top)

        self.controller = Controller(file.name)
        self.controller.get_sequence_from_file()
        results = self.controller.compression_process_without_bwt(self.controller.sequence)
        next_button_text = tk.StringVar()
        next_button = tk.Button(top, 
                               textvariable=next_button_text,
                               bg='#53a6ba',
                               fg='white',
                               font='Raleway',
                               height=2,
                               width=15,
                               bd=0.3)
        next_button_text.set('next')
        next_button.place(x=320, y=400)
        self.insert_in_text_box()
    
    def delete_text_box(self):
        unicode = results.pop(first_key)
        text_box.delete(1.0, 'end')
        if len(results) != 0:
            self.insert_in_text_box()
        else:
            next_button_text.set('Save')
            file_to_save = asksaveasfile(initialdir=os.getcwd(), title="Select File", mode='w', defaultextension='txt')
            with open(file_to_save.name, 'w', encoding='utf8') as f:
                f.write(unicode)
            showinfo('Successful message', 'File saved successfully!')
            top.destroy()

    def insert_in_text_box(self):
        global text_box
        global first_key
        first_key = list(results)[0]
        text_box = tk.Text(top, height=10, width=70)
        text_box.insert('end', first_key.replace('_', ' ') + '\n' + results[first_key] + '\n')
        text_box.tag_configure('center', justify='center')
        text_box.tag_add('center', 1.0, 'end')
        text_box.place(x=120, y=185)
        next_button.configure(command=self.delete_text_box)

    def main_loop(self):
        self.mainloop()

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

    from controller import Controller

    obj = View()
    obj.setup_main_interface()
    obj.create_buttons()
    obj.main_loop()