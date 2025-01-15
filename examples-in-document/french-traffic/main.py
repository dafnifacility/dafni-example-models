import os
import sys
import math
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

gDEBUG = False
gGRAPH = False
gSAVE = True

gPATHI = ""
gPATHO = ""

isDAFNI = os.environ.get("ISDAFNI")
print("ISDAFNI Environment variable = ", isDAFNI, type(isDAFNI))
if isDAFNI == "True":
    if os.name == "nt":
        pren = os.environ.get("HOMEDRIVE")
    else:
        pren = "/"
    gPATHI = os.path.join(pren, "data", "inputs")
    gPATHO = os.path.join(pren, "data", "outputs")
    print("Running within DAFNI: ", gPATHO)
else:
    print("Not running within DAFNI")

print(sys.version)

def trivana():
    global gDEBUG, gGRAPH, gSAVE
    global gPATHI, gPATHO
    indat = os.path.join(os.path.join(gPATHI, "BAAC_2021.xlsx"))
    print("Reading in Excel Spreadsheet with Pandas (openpyxl) : ", indat)
    df = pd.read_excel(indat, sheet_name="Accidents corporels", header=4)
    df = df.iloc[:, 1:]
    if gDEBUG: 
        print (df, df.index, df.columns)
        if False:
            df.plot("Année")
    pdat = PlotData(df)
    if gDEBUG:
        print(pdat.dataset)
    if gGRAPH:
        # Quick pyplot test
        for yr in range(1970, 1974):
            plt.errorbar(pdat.rmonths, pdat.mvals_by_year(yr), yerr=pdat.emvals_by_year(yr), label=yr)
        plt.legend(loc="upper left")
        plt.show()
        plt.errorbar(pdat.ryears, pdat.mvals_by_mnth(7), yerr=pdat.emvals_by_mnth(7), label='Aug')
        plt.legend(loc="upper right")
        plt.show()
    if gSAVE:
        if gPATHO == "":
            tva = "Run directory"
        else:
            tva = gPATHO
        print("Saving output data to : ", tva)
        outdaty = os.path.join(os.path.join(gPATHO, "daty.json"))
        outdatm = os.path.join(os.path.join(gPATHO, "datm.json"))
        jfiley = open(outdaty, "w")
        flin1 = {}
        flin2 = {}
        for yr in pdat.ryears:
            in1 = {yr : pdat.mvals_by_year(yr)}
            in2 = {yr : pdat.emvals_by_year(yr)}
            flin1.update(in1)
            flin2.update(in2)
        f1 = json.dump({"xval" : pdat.rmonths, "xlabel" : "Months", "percent" : flin1, "error" : flin2}, jfiley)
        jfiley.close()
        jfilem = open(outdatm, "w")
        flin1 = {}
        flin2 = {}
        for mnth in range(0, len(pdat.rmonths)):
            in1 = {pdat.rmonths[mnth] : pdat.mvals_by_mnth(mnth)}
            in2 = {pdat.rmonths[mnth] : pdat.emvals_by_mnth(mnth)}
            flin1.update(in1)
            flin2.update(in2)
        f1 = json.dump({"xval" : list(pdat.ryears), "xlabel" : "Years", "percent" : flin1, "epercent" : flin2}, jfilem)
        jfilem.close()
    return


class PlotData:

    def __init__(self, df):
        self.isPanda = False
        if "pandas" in str(type(df)):
            self.isPanda = True
        else:
            self.isPanda = False
        self.ryears = range(1970, 2022)
        self.rmonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.dataset = []  # This is as a fraction
        self.edataset = [] # This is the Delta-E (no asym.err)
        if self.isPanda:
            self.cdata(df)

    def cdata(self, df):  # Using the Panda import frame
        for i in range(0, len(self.ryears)):  # Years
            year = []
            eyear = []
            for j in range(1, 13): # months (+1 for yr col.)
                total = df.iloc[i, 13]
                try:
                    mnth = df.iloc[i, j]/total
                    emnth = math.sqrt(mnth*(1.0-mnth)/total) # Simpl. bin errors.
                except:
                    print("Fail : divide by zero or other issue ?")
                    mnth = -99.9
                    emnth = -99.9
                year.append(mnth)
                eyear.append(emnth)
            self.dataset.append(year)
            self.edataset.append(eyear)

    def mvals_by_year(self, year):
        return self.dataset[self.yindex(year)]

    def emvals_by_year(self, year):
        return self.edataset[self.yindex(year)]
    
    def mvals_by_mnth(self, month):
        vmnthl = []
        for vyr in self.dataset:
            vmnthl.append(vyr[month])
        return vmnthl

    def emvals_by_mnth(self, month):
        evmnthl = []
        for evyr in self.edataset:
            evmnthl.append(evyr[month])
        return evmnthl

    def yindex(self, year):
        iniyear = self.ryears[0]
        finyear = self.ryears[-1]
        assert iniyear <= year <= finyear, "Year " + str(year) + \
                                " is out of bounds. Range is " +  str(iniyear) + " to " + str(finyear)
        return (year-iniyear)

if __name__ == "__main__":
    trivana()
