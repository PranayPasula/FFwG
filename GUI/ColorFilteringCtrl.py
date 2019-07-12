import tkinter as tk
from tkinter import ttk

from GUI.PassFilterCtrl import PassFilterCtrl
from GUI.DataSingleton import DataSingleton

from pranay_sharpen import HighpassFiltering
from Color_smoothing_filters_RGB import LowpassFiltering
import numpy as np
import cv2

class ColorFilteringCtrl:

    cbInvertMasks = None
    isInvertedVar = None
    isInverted = None

    lowPassCtrl = None
    highPassCtrl = None

    def __init__(self, master):
        self.isInvertedVar = tk.IntVar(master, 0)

        lblTabHeader = ttk.Label(master, text="Color Filtering")
        lblTabHeader.pack(side=tk.TOP)
        self.lowPassCtrl = PassFilterCtrl(master, {            
            "Ideal" : "ideal_l",
            "Gaussian" : "gaussian_l",
            "Butterworth" : "butter_l" }, ("Ideal","Gaussian","Butterworth"), "Low Pass Filter")

        self.highPassCtrl = PassFilterCtrl(master, {            
            "Ideal" : "ideal_h",
            "Gaussian" : "gaussian_h",
            "Butterworth" : "butter_h",
            "Unsharp Mask" : "unsharp_m"
           }, ("Ideal","Gaussian","Butterworth","Unsharp Mask"), "High Pass Filter")

        #self.cbInvertMasks = ttk.Checkbutton(master, text="Invert (Band Pass)", command=self.cbInvertMasks_OnCheckChanged, variable=self.isInvertedVar, onvalue=1, offvalue=0)
        #self.cbInvertMasks.pack()
        
        groupFilterBtns = ttk.Frame(master)
        groupFilterBtns.pack(side=tk.BOTTOM, pady=25, fill=tk.X)
        btnApplyFilter = tk.Button(groupFilterBtns, text="Apply Filter", command=self.ApplyFilters)
        btnApplyFilter.pack(fill=tk.X, padx=10, anchor='s')

        #self.cbInvertMasks_OnCheckChanged()

    def cbInvertMasks_OnCheckChanged(self):
        if self.isInvertedVar.get() == 0:
            self.isInverted = False
        else:
            self.isInverted = True

    def ApplyFilters(self):
        data = DataSingleton.GetInstance()

        image = data.GetImageSrc(False)

        lowPassParams = self.lowPassCtrl.GetFilterParams()
        highPassParams = self.highPassCtrl.GetFilterParams()

        if self.lowPassCtrl.IsEnabled():
            lowPassFilter = LowpassFiltering(img=image, cutoff=lowPassParams[1], filter_name=lowPassParams[0], order=lowPassParams[2])
            imageFinal = lowPassFilter.filtering()
            imageFinal = cv2.cvtColor(imageFinal, cv2.COLOR_BGR2RGB)
        elif self.highPassCtrl.IsEnabled():
            highPassFilter = HighpassFiltering(img=image, cutoff=highPassParams[1], filter_name=highPassParams[0], order=highPassParams[2])
            imageFinal = highPassFilter.filtering()
            imageFinal = cv2.cvtColor(imageFinal, cv2.COLOR_BGR2RGB)

        #data.SetImageFFT(imageFFT)
        data.SetImageDst(imageFinal)

    pass


