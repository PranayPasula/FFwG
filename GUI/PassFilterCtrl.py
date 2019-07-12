import tkinter as tk
from tkinter import ttk

class PassFilterCtrl:
    cmbSelectFilter = None
    nudCutoff = None
    nudOrder = None
    isEnabledVar = None
    selectedFilter = None
    dictFilters = None

    def __init__(self, master, dictFilters, displayValues, title):
        self.isEnabledVar = tk.IntVar(master, 0)
        self.dictFilters = dictFilters

        groupPassFilter = ttk.Frame(master)
        groupPassFilter.pack(pady=15)
        groupNuds = ttk.Frame(groupPassFilter)
        cbEnableFilter = ttk.Checkbutton(groupPassFilter, text=title, variable=self.isEnabledVar, command=self.cbEnableFilter_OnCheckChanged, onvalue=1, offvalue=0)

        self.cmbSelectFilter = ttk.Combobox(groupPassFilter, values=displayValues)
        self.cmbSelectFilter.bind('<<ComboboxSelected>>', self.cmbFilter_OnChange)
        self.nudCutoff = ttk.Spinbox(groupNuds, width=8, from_=0, to=1000)
        self.nudOrder = ttk.Spinbox(groupNuds, width=8, from_=0, to=1000)

        cbEnableFilter.pack()
        self.cmbSelectFilter.pack()
        groupNuds.pack(padx=5, pady=10)
        self.nudCutoff.pack(side=tk.LEFT, padx=5, fill=tk.X)
        self.nudOrder.pack(side=tk.LEFT, padx=5, fill=tk.X)

        self.cmbSelectFilter.current(0)
        self.nudCutoff.set(35)
        self.nudOrder.set(2)

        self.cbEnableFilter_OnCheckChanged()
        self.cmbFilter_OnChange(None)

    def cmbFilter_OnChange(self, event):
        self.selectedFilter = self.dictFilters[self.cmbSelectFilter.get()]
        self.EnableNudOrder()

    def EnableNudOrder(self):
        if (self.cmbSelectFilter.get() == "Butterworth" or self.cmbSelectFilter.get() == "Unsharp Mask")and self.IsEnabled():
            self.nudOrder.config(state=tk.NORMAL)
        else:
            self.nudOrder.config(state=tk.DISABLED)

    def cbEnableFilter_OnCheckChanged(self):
        if self.isEnabledVar.get() == 0:
            self.cmbSelectFilter.config(state=tk.DISABLED)
            self.nudCutoff.config(state=tk.DISABLED)
        else:
            self.cmbSelectFilter.config(state=tk.NORMAL)
            self.nudCutoff.config(state=tk.NORMAL)
        self.EnableNudOrder()

    def IsEnabled(self):
        return self.isEnabledVar.get() == 1

    def GetFilterParams(self):
        if self.IsEnabled():
            filter = self.selectedFilter
            cutoff = int(self.nudCutoff.get())
            order = int(self.nudOrder.get())
            return (filter, cutoff, order)
        else:
            return None

    pass




