import tkinter as tk

class FormWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.vcmd = (self.register(self.entry_callback))
        self.stair = tk.IntVar
        self.bulk = tk.IntVar(self, 0)

        self.title("Cube From Texture")
        self.geometry("250x350")
        # self.minsize(250, 150)
        # self.maxsize(250, 150)

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
        self.up_texture_browse = tk.Button(self, text='Browse')
        self.left_texture_browse = tk.Button(self, text='Browse')
        self.right_texture_browse = tk.Button(self, text='Browse')


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
        self.up_texture_browse.place(x=187, y=150)
        self.left_texture_browse.place(x=187, y=180)
        self.right_texture_browse.place(x=187, y=210)

    def entry_callback(self, P):
        return str.isdigit(P) or P == ""

    def toggle_bulk(self):
        if self.bulk.get() == 1:
            self.left_texture.place_forget()
            self.left_texture_label.place_forget()
            self.left_texture_browse.place_forget()
            self.right_texture.place_forget()
            self.right_texture_label.place_forget()
            self.right_texture_browse.place_forget()
            self.up_texture_label.config(text='textures:')
        else:
            self.right_texture_label.place(x=5, y=180)
            self.left_texture_label.place(x=13, y=210)
            self.left_texture.place(x=80, y=182)
            self.right_texture.place(x=80, y=212)
            self.left_texture_browse.place(x=187, y=180)
            self.right_texture_browse.place(x=187, y=210)
            self.up_texture_label.config(text='top texture:')

