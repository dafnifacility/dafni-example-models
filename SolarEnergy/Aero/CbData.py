import os
import glob
import pandas as pd
from geographiclib.geodesic import Geodesic

DEBUG = False

class IrStore():
    # Class to hold multiple irradiance data frames (generic IrData).

    def __init__(self):
        self.waypoints = []
        self.dflist = []
        self.clist = None

    def SetWaypoints(self, waypoints):
        self.waypoints = waypoints

    def LoadAllFiles(self, nconv="modeldata_"):
        lmodeldata = sorted(glob.glob(nconv + '*.*'))
        if DEBUG:
            print("Data-files that match expression : ", lmodeldata)
        for modeldata in lmodeldata:
            dfout = self.LoadMD(modeldata)
            self.dflist.append(dfout)
        self.clist = list(zip(self.waypoints, self.dflist))

    def LoadMD(self, modeldata):
        ext=os.path.splitext(modeldata)[1]
        print("Loading dataframe from ", modeldata, " (a", ext.replace(".", ""), "file)")
        if ext == ".json":
            dfout = pd.read_json(modeldata)
        elif ext == ".csv":
            dfout = pd.read_csv(modeldata)
        elif ext == ".pqt" or ext == ".parquet":
            dfout = pd.read_parquet(modeldata)
        return dfout
    
    def GetNDF(self, position):
        '''Returns the nearest irradiance dataframe to position'''
        closep = 26000.0 # km
        closed = None
        for data in self.clist:
            wpdat = data[0]
            gds = Geodesic.WGS84.Inverse(position.lat, position.lon, wpdat.lat, wpdat.lon )
            dpts = gds['s12']/1000.0  # distance between points. Work in km.
            if dpts < closep:
                closep = dpts
                closed = data
        return closed

    def GetIrradiance(self, position=None, datetime=None):
        '''Takes a waypoint object & a datetime string, and returns the irradiance'''
        ndf = self.GetNDF(position)
        # Get the right data using the datetime obj, ie. nearest index to datetime
        dt = pd.to_datetime(datetime)
        irow = ndf[1].index.get_indexer([dt], method='nearest')[0]
        irrval = ndf[1].iat[irow, 0]
        if DEBUG:
            print("Getting Irradiance :", irrval, "at", datetime)
        return irrval
