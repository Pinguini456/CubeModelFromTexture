import os
import tkinter as tk
from tkinter import filedialog
from render import render, render_stair


class FormWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.vcmd = (self.register(self.entry_callback))
        self.stair = tk.IntVar(self, 0)
        self.bulk = tk.IntVar(self, 0)
        self.filename = ''
        self.up_texture_file = ''
        self.left_texture_file = ''
        self.right_texture_file = ''
        self.texture_dir = ''
        self.output_dir = ''

        self.title("Cube From Texture")
        self.geometry("250x350")
        self.minsize(250, 350)
        self.maxsize(250, 350)

        self.size_label = tk.Label(self, text="img size")
        self.model_size_label = tk.Label(self, text="model size")
        self.model_width_label = tk.Label(self, text="width:")
        self.model_height_label = tk.Label(self, text="height:")
        self.width_label = tk.Label(self, text="width:              px")
        self.height_label = tk.Label(self, text="height:              px")
        self.textures_label = tk.Label(self, text="textures")

        self.model_width = tk.Entry(self, width=5, validate='all', validatecommand=(self.vcmd, '%P'))
        self.model_height = tk.Entry(self, width=5, validate='all', validatecommand=(self.vcmd, '%P'))
        self.width = tk.Entry(self, width=5, validate='all', validatecommand=(self.vcmd, '%P'))
        self.height = tk.Entry(self, width=5, validate='all', validatecommand=(self.vcmd, '%P'))
        self.model_width.insert(0, "100")
        self.model_height.insert(0, "100")

        self.using_stair = tk.Checkbutton(self, text="use stair shape", variable=self.stair, onvalue=1, offvalue=0)
        self.bulk_mode = tk.Checkbutton(self, text="bulk convert", variable=self.bulk, command=self.toggle_bulk)

        self.up_texture = tk.Entry(self, width=15)
        self.left_texture = tk.Entry(self, width=15)
        self.right_texture = tk.Entry(self, width=15)
        self.up_texture.insert(0, 'No File Selected')
        self.left_texture.insert(0, 'No File Selected')
        self.right_texture.insert(0, 'No File Selected')
        self.up_texture_label = tk.Label(self, text='top texture:')
        self.left_texture_label = tk.Label(self, text='left texture:')
        self.right_texture_label = tk.Label(self, text='right texture:')
        self.up_texture_browse = tk.Button(self, text='Browse', command=lambda: self.upload_action('up'))
        self.left_texture_browse = tk.Button(self, text='Browse', command=lambda: self.upload_action('left'))
        self.right_texture_browse = tk.Button(self, text='Browse', command=lambda: self.upload_action('right'))
        self.all_texture_browse = tk.Button(self, text="Browse", command=lambda: self.upload_action('all'))

        self.output_label = tk.Label(self, text="output folder:")
        self.output = tk.Entry(self, width=15)
        self.output.insert(0, 'No File Selected')
        self.output_browse = tk.Button(self, text='Browse', command=lambda: self.upload_action('output'))

        self.start_button = tk.Button(self, text='Start', command=self.start)

        self.size_label.place(x=30, y=0)
        self.width_label.place(x=9, y=30)
        self.height_label.place(x=5, y=50)
        self.width.place(x=50, y=32)
        self.height.place(x=50, y=52)
        self.model_size_label.place(x=150, y=0)
        self.model_width_label.place(x=149, y=30)
        self.model_height_label.place(x=145, y=50)
        self.model_width.place(x=190, y=32)
        self.model_height.place(x=190, y=52)
        self.using_stair.place(x=140, y=70)
        self.textures_label.place(x=100, y=100)
        self.bulk_mode.place(x=10, y=120)
        self.up_texture_label.place(x=12, y=150)
        self.right_texture_label.place(x=5, y=180)
        self.left_texture_label.place(x=13, y=210)
        self.up_texture.place(x=80, y=152)
        self.left_texture.place(x=80, y=182)
        self.right_texture.place(x=80, y=212)
        self.up_texture_browse.place(x=187, y=148)
        self.left_texture_browse.place(x=187, y=178)
        self.right_texture_browse.place(x=187, y=208)
        self.output_label.place(x=0, y=260)
        self.output.place(x=80, y=262)
        self.output_browse.place(x=187, y=258)
        self.start_button.place(x=110, y=300)

    # callback for digit only validation
    def entry_callback(self, P):
        return str.isdigit(P) or P == ""

    def toggle_bulk(self):
        """toggles texture entries for bulk mode"""

        if self.bulk.get() == 1:
            self.left_texture.place_forget()
            self.left_texture_label.place_forget()
            self.left_texture_browse.place_forget()
            self.right_texture.place_forget()
            self.right_texture_label.place_forget()
            self.right_texture_browse.place_forget()
            self.up_texture_browse.place_forget()
            self.up_texture_label.config(text='textures:')
            self.all_texture_browse.place(x=187, y=150)
            self.up_texture.delete(0, tk.END)
            self.left_texture.delete(0, tk.END)
            self.right_texture.delete(0, tk.END)
            self.up_texture.insert(0, 'No File Selected')
            self.left_texture.insert(0, 'No File Selected')
            self.right_texture.insert(0, 'No File Selected')
            self.up_texture_file = ''
            self.left_texture_file = ''
            self.right_texture_file = ''
            self.texture_dir = ''
        else:
            self.all_texture_browse.place_forget()
            self.right_texture_label.place(x=5, y=180)
            self.left_texture_label.place(x=13, y=210)
            self.left_texture.place(x=80, y=182)
            self.right_texture.place(x=80, y=212)
            self.left_texture_browse.place(x=187, y=180)
            self.right_texture_browse.place(x=187, y=210)
            self.up_texture_browse.place(x=187, y=150)
            self.up_texture_label.config(text='top texture:')
            self.up_texture.delete(0, tk.END)
            self.left_texture.delete(0, tk.END)
            self.right_texture.delete(0, tk.END)
            self.up_texture.insert(0, 'No File Selected')
            self.left_texture.insert(0, 'No File Selected')
            self.right_texture.insert(0, 'No File Selected')
            self.up_texture_file = ''
            self.left_texture_file = ''
            self.right_texture_file = ''
            self.texture_dir = ''

    def upload_action(self, direction):
        """handles uploads

        Parameters:
            direction - what entry is being uploaded to
        """
        if direction == 'all' or direction == 'output':
            self.filename = filedialog.askdirectory()
        else:
            self.filename = filedialog.askopenfilename(filetypes=(('PNG', '*png'),))
        if self.filename == '':
            return

        match direction:
            case 'up':
                self.up_texture_file = self.filename
                self.up_texture.delete(0, tk.END)
                self.up_texture.insert(0, self.filename)
            case 'right':
                self.right_texture_file = self.filename
                self.right_texture.delete(0, tk.END)
                self.right_texture.insert(0, self.filename)
            case 'left':
                self.left_texture_file = self.filename
                self.left_texture.delete(0, tk.END)
                self.left_texture.insert(0, self.filename)
            case 'all':
                self.texture_dir = self.filename
                self.up_texture.delete(0, tk.END)
                self.up_texture.insert(0, self.filename)
            case 'output':
                self.output_dir = self.filename
                self.output.delete(0, tk.END)
                self.output.insert(0, self.filename)

    def start(self):
        """starts the rendering process of the models"""

        # entry checks
        if self.width.get() == '' or self.height.get() == '':
            print("invalid image size")
            return
        if self.model_width.get() == '' or self.model_height.get() == '':
            print("invalid model size")
            return
        if self.bulk.get() == 0:
            if self.up_texture_file == '':
                print("no top texture found")
                return
            if self.left_texture_file == '':
                print("no left texture found")
                return
            if self.right_texture_file == '':
                print("no right texture found")
                return
        else:
            if self.texture_dir == '':
                print("no input directory specified")
                return
        if self.output_dir == '':
            print("no output directory specified")

        img_size = (int(self.width.get()), int(self.height.get()))
        cube_size = (int(self.model_width.get()), int(self.model_height.get()))

        if self.bulk.get() == 0:
            if self.stair.get() == 1:
                render_stair(self.up_texture_file, self.left_texture_file, self.right_texture_file, img_size, cube_size, self.output_dir)
            else:
                render(self.up_texture_file, self.left_texture_file, self.right_texture_file, img_size, cube_size, self.output_dir)
        else:
            for item in os.listdir(self.texture_dir):
                texture = os.path.join(self.texture_dir, item).replace('\\', '/')

                if os.path.isdir(texture):
                    continue
                if item == 'desktop.ini':
                    continue

                if self.stair.get() == 1:
                    render_stair(texture, texture, texture, img_size, cube_size, self.output_dir)
                else:
                    render(texture, texture, texture, img_size, cube_size, self.output_dir)

            print("Done!")


