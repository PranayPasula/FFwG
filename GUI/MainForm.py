import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from tkinter import ttk
import cv2
import sys

from GUI.OptionsCtrl import OptionsCtrl
from GUI.DataSingleton import DataSingleton

import sharp_fourier

class MainForm:
    #image = None
    lowPassEnabled = False
    #imageSrc = None
    imageSrcPIL = None
    picImageSrc = None
    #imageFFT = None
    imageFFTPIL = None
    picImageFFT = None
    top = None
    #imageGrey = None
    #imageDst = None
    imageDstPIL = None
    picImageDst = None

    options_right = None
    dataSource = None
    
    def GetImage(self, greyScale):
        if greyScale:
            image = self.imageGrey
        else:
            image = self.image
        return image

    def __init__(self):
        """initializes the GUI"""
        self.dataSource = DataSingleton.GetInstance()
        self.dataSource.SetOnSrcChanged(self.SetSourceImage)
        self.dataSource.SetOnFFTChanged(self.SetFFTImage)
        self.dataSource.SetOnDstChanged(self.SetOutputImage)
        self.InitializeComponents()

    def SetSourceImage(self):
        img = self.dataSource.GetImageSrc(False)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.imageSrcPIL = ImageTk.PhotoImage(Image.fromarray(img))
        self.picImageSrc.configure(image=self.imageSrcPIL)

    def SetFFTImage(self):
        img = self.dataSource.GetImageFFT()
        self.imageFFTPIL = ImageTk.PhotoImage(Image.fromarray(img))
        self.picImageFFT.configure(image=self.imageFFTPIL)

    def SetOutputImage(self):
        img = self.dataSource.GetImageDst()
        self.imageDstPIL = ImageTk.PhotoImage(Image.fromarray(img))
        self.picImageDst.configure(image=self.imageDstPIL)

    def openFile(self):
        filename =  filedialog.askopenfilename(initialdir = "./images/",title = "Select file",filetypes = (("Image files","*.jpg;*.png"),("jpeg files","*.jpg"),("PNG files","*.png"),("all files","*.*")))
        img = cv2.imread(filename)
        self.dataSource.SetImageSrc(img)

    def saveFile(self):
        img = self.dataSource.GetImageDst()
        if img.any():
            filename =  filedialog.asksaveasfilename(initialdir = "./images/",title = "Select file",filetypes = (("PNG files","*.png"),("jpeg files","*.jpg"),("all files","*.*")))
            if filename != None:
                cv2.imwrite(filename, img)   

    def exitProgram(self):
        self.top.quit()

    def InitializeComponents(self):
        self.top = tk.Tk()
        self.top.title("Monolithic Kernal App")

        menuBar = tk.Menu(self.top)
        self.top['menu']=menuBar
        menuFile = tk.Menu(menuBar)
        menuEdit = tk.Menu(menuBar)
        menuOptions = tk.Menu(menuBar)
        menuBar.add_cascade(menu=menuFile, label='File')
        menuBar.add_cascade(menu=menuEdit, label='Edit')
        menuBar.add_cascade(menu=menuOptions, label='Options')

        menuFile.add_command(label='Open', command=self.openFile)
        menuFile.add_command(label='Save', command=self.saveFile)
        menuFile.add_command(label='Exit', command=self.exitProgram)

        m1 = tk.PanedWindow(self.top)
        m1.pack(fill=tk.BOTH, expand=1)

        notebook = ttk.Notebook(m1, width=640, height=480)
        notebook.pack(side=tk.LEFT)

        source_tab = ttk.Frame(notebook)
        source_tab.pack()
        fft_tab = ttk.Frame(notebook)
        fft_tab.pack()
        output_tab = ttk.Frame(notebook)
        output_tab.pack()

        notebook.add(source_tab, text="Source")
        notebook.add(fft_tab, text="FFT")
        notebook.add(output_tab, text="Output")
        m1.add(notebook)

        self.picImageSrc = tk.Label(source_tab)
        self.picImageSrc.pack(fill=tk.BOTH)

        self.picImageFFT = tk.Label(fft_tab)
        self.picImageFFT.pack(fill=tk.BOTH)

        self.picImageDst = tk.Label(output_tab)
        self.picImageDst.pack(fill=tk.BOTH)

        m2 = tk.PanedWindow(m1, orient=tk.VERTICAL, width=256)
        m1.add(m2)

        self.options_right = OptionsCtrl(m2)

    def Show(self):
        #self.SetSourceImage(imagePath)
        self.top.mainloop()
