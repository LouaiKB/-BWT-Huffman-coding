# coding ~utf-8

"""

Author: Louai KB

View of the application

"""
import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import askquestion
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from PIL import Image
from PIL import ImageTk
from Bio import SeqIO
from bwt import Bwt
from controller import Controller


class PlaceImage:

    """This class is created to place the main logo of the application """

    @staticmethod
    def place_image(root:tk.Tk) -> None:
        """ A static method to place the logo (genome.png) in the window.

        Args:
            root (Tk object)
        """
        global text_box_window

        root.geometry('800x700')
        
        # creating canvas for padding
        canvas_for_padding = tk.Canvas(root, width=600, height=300)
        canvas_for_padding.grid(columnspan=3, rowspan=3)
        
        # importing the image
        logo = Image.open('../photos/genome.png')
        
        # placing the logo image
        genome_compression_logo = ImageTk.PhotoImage(logo)
        genome_compression_logo_label = tk.Label(root, image=genome_compression_logo)
        genome_compression_logo_label.image = genome_compression_logo
        genome_compression_logo_label.grid(row=0, column=1)

        # adding a scroll bar
        yscrollbar = tk.Scrollbar(root)
        
        # creating a text box window
        text_box_window = tk.Text(root, height=10, width=70,
                           yscrollcommand=yscrollbar.set)
        text_box_window.tag_configure('center', justify='center')
        text_box_window.tag_add('center', 1.0, 'end')
        text_box_window.place(x=120, y=185)
        
        # placing the scroll bar
        yscrollbar.place(in_=text_box_window, relx=1.0, relheight=1.0, bordermode='outside')
        yscrollbar.config(command=text_box_window.yview)


class View(tk.Tk):

    """View class of the application that inherits from the Tkinter Tk() class
    """

    def __init__(self) -> None:

        """ Class constructor
            button_dict dictionnary contains the coordinates (x, y) 
            to place the buttons in the window.
        """

        super().__init__()
        self.title('Genome compression')
        self.controller = None
        self.button_dict = {
            "Compress": (60, 410), 
            "Decompress": (320, 410), 
            "Full compression": (590, 410), 
            "Bwt encryption": (60, 510), 
            "Bwt decryption": (320, 510),
            "Full decompression": (590, 510),
            "Quit": (389, 630)
        }

    def setup_main_interface(self) -> None:
        
        """ A Method to setup the main window, calls the place_image 
            static method to place the image.
        """
        
        PlaceImage.place_image(self)
        
        label = tk.Label(self, text='Enter the sequence manually or with a file (txt, fasta)',
                font='Raleway 10 italic', fg='#737373')

        label.place(x=250, y=360)

    def get_content_of_text_box(self) -> str:

        """ A method to retrieve the content of the text box presented in the main window.
            this textbox is created to enter sequences manually.

        Returns:
            str: content of the text box.
        """
        content = text_box_window.get(1.0, 'end')
        return content

    def top_level_windows(self, title:str) -> None:
        """ A method to create toplevel (popup) windows

        Args:
            title (str): the title of the toplevel window
        """
        global top
        global next_button
        global next_button_text

        top = tk.Toplevel()
        top.title(title)
        PlaceImage.place_image(top)
        next_button_text = tk.StringVar()
        next_button = tk.Button(top, textvariable=next_button_text, bg='#53a6ba', fg='white',
                               font='Raleway', height=2, width=15, bd=0.3)

        next_button_text.set('next')
        next_button.place(x=320, y=400)


    def create_buttons(self) -> None:

        """This method creates buttons for the main window"""

        for key, value in self.button_dict.items():
            button_text = tk.StringVar()
            button = tk.Button(self, textvariable=button_text, bg='#53a6ba', fg='white',
                               font='Raleway', height=2, width=15, bd=0.3)

            button_text.set(key)
            button.place(x=value[0], y=value[1])

            if key == 'Quit':
                button.configure(bg='#d07b1a', width=20, command=self.quit)
                button.place_configure(anchor='center')

            elif key == 'Compress':
                button.configure(command=self.compression)

            elif key == 'Decompress':
                button.configure(command=self.decompression)

            elif key == 'Full compression':
                button.configure(command=lambda:self.bwt_encryption(full=True))

            elif key == 'Bwt encryption':
                button.configure(command=self.bwt_encryption)

            elif key == 'Bwt decryption':
                button.configure(command=self.bwt_decryption)

            elif key == 'Full decompression':
                button.configure(command=lambda:self.decompression(full_dec=True))

    def open_and_get_size(self, decompression:bool=None):

        """ A method to create the file chooser for the interface
            for the decompression process (when decompression=True)
            we will choose the file of the decompression and the json file
            associated (which provides data of the compression) and we
            will use this data for the decompression process.

        Args:
            decompression (bool, optional): a bool to precise if we wanna open a sequence file for 
            the decompression or not, because we open sequence file for the compression and for 
            the Burrows Wheeler encryption and decryption other wise for the decompression we will
            provide the compressed file and json associated file. Defaults to None.

        Returns:
            size of the original file if decompression=None
            else a tuple of the compressed file and the json data.
        """

        if not decompression:

            file = askopenfile(parent=self, mode='r', title='choose a file', 
                    filetypes=(('Text files', '*.txt'), ('Fasta file', '*.fasta')))

            self.controller = Controller(file.name)
            size_of_original_file = os.path.getsize(file.name)

            return size_of_original_file

        else:
            showinfo('Decompression process', 'please choose the txt file and the json file to decompress')

            file_decompress = askopenfile(parent=self, mode='r', title='Choose a decompression file',
                    filetypes=(('Text file', '*.txt'), ("All Files","*.*")))

            self.controller = Controller(file_decompress.name)

            json_file = askopenfile(parent=self, mode='r', title='Choose the associated json file',
                            filetypes=(('Json file', '*.json'), ('All File', '*.*')))

            with open(json_file.name) as f:
                data = json.load(f)

            return (file_decompress, data)

    def save_file(self, additionnal_data:dict=None, sequence:str=None) -> None:

        """ A method to save the files
            for the compression we will use a compression format (two files: the first contains the
            compressed sequence "unicode" and the second is a json file which contains data that will
            be used for the decompression process).
        """

        if additionnal_data:

            
            try:
                
                file_to_save = asksaveasfile(initialdir=os.getcwd(), title="Select File", mode='w', defaultextension='txt')
                
                with open(file_to_save.name, 'w', encoding='utf8') as f, open(file_to_save.name[:-4] + '_json_file.json', 'w') as jsn:
                    f.write(unicode)
                    json.dump(additionnal_data, jsn)

                size_of_compressed_file = os.path.getsize(file_to_save.name)
                showinfo('Successful message', 'File saved successfully!\nThe size of the original file is: %s\nThe size of the compressed file is: %s'
                        %(str(size_of_original_file), str(size_of_compressed_file)))

                top.quit()

            except AttributeError:
                
                showerror('Error file!', 'Please enter a file')
        
        else:
            file_to_save = asksaveasfile(initialdir=os.getcwd(), title="Select File", mode='w', defaultextension='txt')
            with open(file_to_save.name, 'w', encoding='utf8') as f:
                f.write(sequence)
            showinfo('Successful message', 'File saved successfully!')
            top.quit()



    def compression(self, full:bool=None) -> None:

        """ A method to proceed the compression process step by step and the full compression 
            process is full = True.

        Args:
            full (bool): a boolean to precise if we wanna procees a full compression or not    
        """

        global binary_co
        global encoder
        global unicode
        global size_of_original_file

        
        content = self.get_content_of_text_box()
        # if the content of the text box is empty we will ask to open file
        # otherwise we will use directly the sequence entered manually

        try:
            
            if not full:

                if content == '\n':
                    size_of_original_file = self.open_and_get_size()
                    self.controller.get_sequence_from_file()

                else:
                    self.controller = Controller('')
                    self.controller.sequence = content.strip()
                    
                    # WE will create a file that contains the sequence entered manually
                    # in order to get the size than we will remove it

                    with open('f.txt', 'w') as f:
                        f.write(self.controller.sequence)
                    size_of_original_file = os.path.getsize('f.txt')
                    os.remove('f.txt')


                self.top_level_windows('Genome compression process')

                results = self.controller.compression_process_without_bwt(self.controller.sequence)
                encoder = results.pop('encoder')

                unicode = results[list(results)[-1]]
                binary_co = results[list(results)[1]]
            
                self.compression_decompression_helper(results)

            else:

                results = self.controller.compression_process_without_bwt(self.controller.sequence)
                encoder = results.pop('encoder')

                unicode = results[list(results)[-1]]
                binary_co = results[list(results)[1]]
            
                self.compression_decompression_helper(results)
                        
        except:

            showerror('Error file!', 'Please enter the right file')

    def compression_decompression_helper(self, results:dict, decompression:bool=None, full_dec:bool=None) -> None:
        
        """ This is a helper method to help us proceed the step by step compression and decompression process
        """
        
        try:

            first_key = list(results)[0]
            inserted_object = first_key + '\n' + results[first_key] + '\n'
            self.insert_in_text_box(inserted_object)
            
            if decompression:
                next_button.configure(command=lambda:self.delete_text_box(first_key, results, decompression=True))

            else:
                next_button.configure(command=lambda:self.delete_text_box(first_key, results))
               
        
        except IndexError:

            if decompression:
                
                if full_dec:
                    self.full_compression_decompression_helper(full_dec=True) 

                else:
                    self.save_patterns(decompression=True)
                    text_box.delete(3.0, 'end')         

            else:
                self.save_patterns()

                

    def delete_text_box(self, first_key:str, results:dict, decompression:bool=None) -> None:

        """This method is created to delete the text in the text box.
        """

        if decompression:
            text_box.delete(1.0, 'end')

            if len(results) != 0:
                results.pop(first_key)
                self.compression_decompression_helper(results, decompression=True, full_dec=True)

            else:
                self.save_file(sequence=decompressed_sequence)
            
        else:
            text_box.delete(1.0, 'end')

            if len(results) != 0:
                results.pop(first_key)
                self.compression_decompression_helper(results)

            else:
                additionnal_data = {
                    'encoder': encoder, 
                    'binary_seq': binary_co
                }
                self.save_file(additionnal_data)


    def insert_in_text_box(self, inserted_object:str) -> None:
        """ A method to insert in the text box

        Args:
            inserted_object (str): text ot be inserted.
        """
        global text_box 

        # adding a scroll bar
        yscrollbar = tk.Scrollbar(top)

        # creating the text box
        text_box = tk.Text(top, height=10, width=70,
                           yscrollcommand=yscrollbar.set)
        
        text_box.insert('end', inserted_object)
        text_box.tag_configure('center', justify='center')
        text_box.tag_add('center', 1.0, 'end')
        text_box.place(x=120, y=185)
        yscrollbar.place(in_=text_box, relx=1.0, relheight=1.0, bordermode='outside')
        yscrollbar.config(command=text_box.yview)


    def save_patterns(self, decompression:bool=None) -> None:

        """ A method that creates save patterns (add a save button and a responsive paragraph to 
            tell that the process is achived and ask if we want to save the sequence in a file or not)
        """

        next_button_text.set('Save')
        text_box.insert('end', '\nProcess completed whould you like to save the sequence?')
        text_box.tag_configure('center', justify='center')
        text_box.tag_add('center', 1.0, 'end')
        next_button.place_configure(x=60, y=400)
        
        button_q = tk.Button(top, text='Quit', bg='#d07b1a', fg='white',
                            font='Raleway', height=2, width=15, bd=0.3, command=top.quit)
        
        button_q.place(x=590, y=400)

    def decompression(self, full_dec:bool=None) -> None:
        
        """ A method to proceed the decompression process step by step and the full decompression 
            process is full_dec = True.

            Notice: for the decompression we can't enter sequence manually because we need the json file.

        """
        global decompressed_sequence

        try:
            
            content = self.get_content_of_text_box()

            if content != '\n':
                showerror('Error!', 'Please enter a file')
                text_box_window.delete(1.0, 'end')

            files = self.open_and_get_size(decompression=True)
            self.top_level_windows('Genome decompression process')
            file_decompress = files[0]
            json_file = files[1]
            
            results_deco = self.controller.decompression_process_without_bwt(file_decompress.name, json_file['encoder'],
                                                            json_file['binary_seq'])

            decompressed_sequence = results_deco[list(results_deco)[-1]]
            
            if full_dec:
                self.compression_decompression_helper(results_deco, decompression=True, full_dec=True)

            else:
                self.compression_decompression_helper(results_deco, decompression=True)

        except:
            showerror('Error file!', 'Please enter the right file')

    def bwt_encryption(self, full:bool=None) -> None:
        """ A method to proceed the Burrows Wheeler encryption process, we will ask
            the user if he want to proceed the BWT step by step or not.

        Args:
            full (bool): to precise if we want to process the full decompression or not. Defaults to None.
        """
        global bwt_matrix
        global gen
        global bwt_sequence
        global size_of_original_file
        
        content = self.get_content_of_text_box()

        try:
            if content == '\n':
                size_of_original_file = self.open_and_get_size()
                self.controller.get_sequence_from_file()
            
            else:
                self.controller = Controller('')
                self.controller.sequence = content.strip()

            ask_quest = askquestion('Bwt encryption', 'Would you like to proceed the step by step Burrows Wheeler Transform?')
            results_bwt = self.controller.bwt_encryption_step_by_step()
            bwt_matrix = results_bwt[0]
            bwt_sequence = results_bwt[1]

            if ask_quest == 'yes':
                gen = 'Step 1: The matrix construction '
                self.top_level_windows('BWT encryption')
                self.insert_in_text_box(gen)
                
                if full:
                    next_button.configure(command=lambda:self.get_next(gen, full=True))

                else:
                    next_button.configure(command=lambda:self.get_next(gen))
            
            else:
                self.top_level_windows('BWT encryption')
                text = 'The Bwt sequence\n' + bwt_sequence
                self.insert_in_text_box(text)
                
                if not full:
                    self.save_patterns()
                    next_button.configure(command=lambda: self.save_file(sequence=bwt_sequence))
                else:
                    next_button.configure(command=self.full_compression_helper)

        except AttributeError:
            showerror('File Error', 'Please enter the right file!')

    def bwt_decryption(self, full_dec:bool=None):
        """ A method to process the Burrows Wheeler decryption

        Args:
            full_dec (bool): for the full decompression process
        """
        global bwt_matrix_re
        global sequence_re
        global row_index
        
        content = self.get_content_of_text_box()
        try:
            if full_dec:

                if content != '\n':
                    showerror('Error!', 'Please enter a file')
                    text_box_window.delete(1.0, 'end')

                self.controller.sequence = decompressed_sequence
    
            else:

                if content == '\n':
                    self.open_and_get_size()
                    self.controller.get_sequence_from_file()
                    self.top_level_windows('BWT decryption')
                else:
                    self.controller = Controller('')
                    self.controller.sequence = content.strip()
                    self.top_level_windows('BWT decryption')

            results_bwt = self.controller.bwt_decryption()
            bwt_matrix_re = results_bwt[0]
            sequence_index = results_bwt[1]
            sequence_re = sequence_index[0]
            row_index = sequence_index[1]
            gen = 'Step 1: The Bwt sequence \n' + self.controller.sequence
            self.insert_in_text_box(gen)
            next_button.configure(command=self.step_tw_bwt_dec)
    
        except:
            showerror('Error file!', 'Please enter the right file')

    def step_tw_bwt_dec(self) -> None:
        """Helper method to proceed the Burrows Wheeler step by step encryption
        """

        gen = 'Step2: Sorted matrix construction,\nThe bwt sequence is the one who has $ in the end'
        self.insert_in_text_box(gen)
        next_button.configure(command=lambda:self.get_next(gen, decryption=True, row_index=row_index))

    def full_compression_decompression_helper(self, full_dec=None):
        
        """ Helper method for the full compression and decompression process
        """
        if full_dec:
            text = 'Now the decryption process'
            self.insert_in_text_box(text)
            next_button.configure(command=lambda:self.bwt_decryption(full_dec=True))

        else:
            gen = 'Now the compression process'
            self.insert_in_text_box(gen)
            self.controller.sequence = bwt_sequence
            next_button.configure(command=lambda:self.compression(full=True))

    def get_next(self, gen:str, decryption:bool=None, row_index:int=None, full:bool=None):
        """ This method is created to get the next of the Burrows Wheeler Matrix generator

        Args:
            gen (str): the content to be inserted in the text box
            decryption (bool): a boolean to precise if we procees the encryption or the decryption process. Defaults to None.
            row_index (int): the index of the row of the original sequence in the Burrows Wheeler reconstruction matrix
                             this variable is used to proceed the coloration of the sequence in the matrix. Defaults to None.
            full (bool): for the full compression process
        """
        if not decryption:

            try:
                gen = ''
                gen += text_box.get("1.0", "end") + next(bwt_matrix)
                self.insert_in_text_box(gen)

            except StopIteration:

                sorted_bwt = []
                indexx = 3

                bwt = self.controller.bwt_encryption_step_by_step()
                sorted_matrix = ''
                
                for i in sorted(bwt[0]):
                    sorted_matrix += str(i) + '\n'
                    sorted_bwt.append(str(i))
                
                gen = 'Step 2: The sort of the matrix\nThe BWT sequence is presented in the last column\n' + sorted_matrix + '\n\nBwt Sequence: ' + bwt_sequence
                self.insert_in_text_box(gen)

                for i in sorted_bwt:
                    j = str(indexx) + '.' + str(len(i) - 1)
                    text_box.tag_add('color', j)
                    text_box.tag_config('color', foreground='red')
                    indexx += 1 

                if not full:
                    self.save_patterns()
                    next_button.configure(command=lambda:self.save_file(sequence=bwt_sequence))
        
                else:
                    next_button.configure(command=self.full_compression_decompression_helper)
        else:

            try:
                gen = ''
                gen += text_box.get("1.0", "end") + next(bwt_matrix_re)
                self.insert_in_text_box(gen)

            except StopIteration:
                gen = text_box.get("1.0", "end") + "\n\nThe sequence: " + str(sequence_re)
                self.insert_in_text_box(gen)
                text_box.tag_add('color_re', str(3 + row_index) + '.0', str(3 + row_index) + '.' + str(len(sequence_re) + 1))
                text_box.tag_config('color_re', foreground='red')
                self.save_patterns()
                next_button.configure(command=lambda:self.save_file(sequence=sequence_re))
    
    
    def main_loop(self) ->None:
        """Main loop of our tkinter object, for the appearence of the interface
        """
        self.mainloop()

