import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import ttk

#from GUI.PassFilterCtrl import PassFilterCtrl
from GUI.TabFilteringCtrl import TabFilteringCtrl
from GUI.SharpenCtrl import SharpenCtrl
from GUI.ColorFilteringCtrl import ColorFilteringCtrl

class OptionsCtrl:

    imgMaskLabel = None
    imgNotchLabel = None
    imgSmoothLabel = None
    imgColorLabel = None
    imgSharpenLabel = None

    style = None

    def __init__(self, master):

        self.style = ttk.Style()
        self.style.configure('optionsCtrl.TNotebook', tabposition='en')

        img = Image.open('./resources/mask_label.png')
        img = img.resize((24,43), Image.ANTIALIAS)
        self.imgMaskLabel = ImageTk.PhotoImage(img)

        img = Image.open('./resources/notch_label.png')
        img = img.resize((24,44), Image.ANTIALIAS)
        self.imgNotchLabel = ImageTk.PhotoImage(img)

        img = Image.open('./resources/smooth_label.png')
        img = img.resize((24,57), Image.ANTIALIAS)
        self.imgSmoothLabel = ImageTk.PhotoImage(img)

        img = Image.open('./resources/color_label.png')
        img = img.resize((24,43), Image.ANTIALIAS)
        self.imgColorLabel = ImageTk.PhotoImage(img)

        img = Image.open('./resources/sharpen_label.png')
        img = img.resize((24,61), Image.ANTIALIAS)
        self.imgSharpenLabel = ImageTk.PhotoImage(img)

        optionsCtrl = ttk.Notebook(master, style='optionsCtrl.TNotebook', width=192)
        master.add(optionsCtrl)
        optionsCtrl.pack(side=tk.RIGHT, fill=tk.Y)

        tabMask = ttk.Frame(optionsCtrl)
        tabMask.pack()
        tabSmooth = ttk.Frame(optionsCtrl)
        tabSmooth.pack()
        tabSharpen = ttk.Frame(optionsCtrl)
        tabSharpen.pack()
        tabColor = ttk.Frame(optionsCtrl)
        tabColor.pack()
        tabNotch = ttk.Frame(optionsCtrl)
        tabNotch.pack()
        optionsCtrl.add(tabMask, image=self.imgMaskLabel)
        optionsCtrl.add(tabSmooth, image=self.imgSmoothLabel)
        optionsCtrl.add(tabSharpen, image=self.imgSharpenLabel)
        optionsCtrl.add(tabColor, image=self.imgColorLabel)
        optionsCtrl.add(tabNotch, image=self.imgNotchLabel)
        
        tabFilteringCtrl = TabFilteringCtrl(tabMask)
        tabSharpenCtrl = SharpenCtrl(tabSharpen)
        tabColorFilteringCtrl = ColorFilteringCtrl(tabColor)
        
    pass




