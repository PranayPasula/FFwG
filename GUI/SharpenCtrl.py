import tkinter as tk
from tkinter import ttk
import numpy as np

from sharp_fourier import Sharpen
from GUI.DataSingleton import DataSingleton

class SharpenCtrl:
    nudGammaL = None
    nudGammaH = None
    nudDiameter = None
    nudOrder = None

    def __init__(self, master):
        """ initialize control"""
        
        groupMorphic = ttk.Frame(master)
        groupMorphic.pack()
        lblHeader=ttk.Label(groupMorphic, text='Homomorphic Sharpen')
        groupNuds = ttk.Frame(groupMorphic)

        row0 = ttk.PanedWindow(groupNuds, orient=tk.HORIZONTAL)
        col00 = ttk.Frame(row0)
        col01 = ttk.Frame(row0)

        row1 = ttk.PanedWindow(groupNuds, orient=tk.HORIZONTAL)
        col10 = ttk.Frame(row1)
        col11 = ttk.Frame(row1)

        lblGammaL=ttk.Label(col00, text='Gamma L')
        lblGammaH=ttk.Label(col01, text='Gamma H')
        lblDiameter=ttk.Label(col10, text='D0')
        lblOrder=ttk.Label(col11, text='Order')
        self.nudGammaL = ttk.Spinbox(col00, width=5, from_=0, to=1000, increment=0.1)
        self.nudGammaH = ttk.Spinbox(col01, width=5, from_=0, to=1000, increment=0.1)
        self.nudDiameter = ttk.Spinbox(col10, width=5, from_=0, to=1000)
        self.nudOrder = ttk.Spinbox(col11, width=5, from_=0, to=1000)

        row0.pack(fill=tk.X, pady=5)
        col00.pack(side=tk.LEFT, padx=10)
        col01.pack(side=tk.RIGHT, padx=10)
        row1.pack(fill=tk.X, pady=5)
        col10.pack(side=tk.LEFT, padx=10)
        col11.pack(side=tk.RIGHT, padx=10)

        lblHeader.pack(sid=tk.TOP, fill=tk.X)
        groupNuds.pack(padx=5, pady=10)
        lblGammaL.pack(side=tk.TOP)
        self.nudGammaL.pack(side=tk.LEFT)
        lblGammaH.pack(side=tk.TOP)
        self.nudGammaH.pack(side=tk.RIGHT)
        lblDiameter.pack(side=tk.TOP)
        self.nudDiameter.pack(side=tk.LEFT)
        lblOrder.pack(side=tk.TOP)
        self.nudOrder.pack(side=tk.RIGHT)

        self.nudGammaL.set(0.75)
        self.nudGammaH.set(1.25)
        self.nudDiameter.set(35)
        self.nudOrder.set(2)

        groupFilterBtns = ttk.Frame(master)
        groupFilterBtns.pack(side=tk.BOTTOM, pady=25, fill=tk.X)
        btnApplyFilter = tk.Button(groupFilterBtns, text="Apply Filter", command=self.ApplyFilters)
        btnApplyFilter.pack(fill=tk.X, padx=10, anchor='s')

    def ApplyFilters(self):
        data = DataSingleton.GetInstance()

        gammaL = float(self.nudGammaL.get())
        gammaH = float(self.nudGammaH.get())
        diameter = int(self.nudDiameter.get())
        order = int(self.nudOrder.get())
        image = data.GetImageSrc(True)

        imageFinal, imageFFT = Sharpen.homomorphic(image, gammaL, gammaH, diameter, order)

        imageFFT = Sharpen.post_process_image(np.abs(imageFFT))

        data.SetImageFFT(imageFFT)
        data.SetImageDst(imageFinal)
    pass




