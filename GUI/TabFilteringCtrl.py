import tkinter as tk
from tkinter import ttk

from GUI.PassFilterCtrl import PassFilterCtrl
from GUI.DataSingleton import DataSingleton

from Filtering import Filtering

class TabFilteringCtrl:

    cbInvertMasks = None
    isInvertedVar = None
    isInverted = None

    lowPassCtrl = None
    highPassCtrl = None

    def __init__(self, master):
        self.isInvertedVar = tk.IntVar(master, 0)

        self.lowPassCtrl = PassFilterCtrl(master, {            
            "Ideal" : "ideal_l",
            "Gaussian" : "gaussian_l",
            "Butterworth" : "butterworth_l" }, ("Ideal","Gaussian","Butterworth"), "Low Pass Filter")

        self.highPassCtrl = PassFilterCtrl(master, {            
            "Ideal" : "ideal_h",
            "Gaussian" : "gaussian_h",
            "Butterworth" : "butterworth_h" }, ("Ideal","Gaussian","Butterworth"), "High Pass Filter")

        self.cbInvertMasks = ttk.Checkbutton(master, text="Invert (Band Pass)", command=self.cbInvertMasks_OnCheckChanged, variable=self.isInvertedVar, onvalue=1, offvalue=0)
        self.cbInvertMasks.pack()
        
        groupFilterBtns = ttk.Frame(master)
        groupFilterBtns.pack(side=tk.BOTTOM, pady=25, fill=tk.X)
        btnApplyFilter = tk.Button(groupFilterBtns, text="Apply Filter", command=self.ApplyFilters)
        btnApplyFilter.pack(fill=tk.X, padx=10, anchor='s')

        self.cbInvertMasks_OnCheckChanged()

    def cbInvertMasks_OnCheckChanged(self):
        if self.isInvertedVar.get() == 0:
            self.isInverted = False
        else:
            self.isInverted = True

    def ApplyFilters(self):
        data = DataSingleton.GetInstance()

        image = data.GetImageSrc(True)

        lowPassParams = self.lowPassCtrl.GetFilterParams()
        highPassParams = self.highPassCtrl.GetFilterParams()

        mask = Filtering.GetMask(image, lowPassParams, highPassParams, self.isInverted)

        imageFinal, imageFFT, imageFilter = Filtering.ApplyFiltering(image, mask)

        data.SetImageFFT(imageFilter)
        data.SetImageDst(imageFinal)

    pass




