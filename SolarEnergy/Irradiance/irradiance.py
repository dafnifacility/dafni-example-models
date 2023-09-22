import os
import glob
from geographiclib.geodesic import Geodesic
import pandas as pd
import pvlib
HASMPL = True
try:
    from matplotlib import pyplot
except:
    HASMPL = False

DEBUG = False
DAFNI_DDI = os.path.join(os.getcwd(), "datalocal")


class GenModel:

    def __init__(self, lat=49.749992, lon=6.637143299999934, tilt=25.0, azim=180.0, 
                 tz = 'UTC', altover=-999, days=365, startday='06-06-2023'):
        '''Setup input for pvlibs clearsky model'''
        self.power = -99.9
        self.clouds = []
        self.tz = tz
        # Generate time series using pandas. Days is the number of days to generate.
        self.days = days
        self.startday = startday
        self.times = pd.date_range(startday, freq='10min', periods=6*24*self.days, tz=tz)
        # Setup altitude (either the overriden value or the pvlib lookup)
        if altover <= -999:
            self.alt = pvlib.location.lookup_altitude(lat, lon)
        else:
            self.alt = altover
        # Initialise pvlib Location object (used for the clearsky estimates & solar pos.)
        self.loc = pvlib.location.Location(lat, lon, tz=tz, altitude=self.alt)
        # Generate clearsky model
        self.gen_clearsky(tilt, azim)

    def gen_clearsky(self, tilt, azim):
        '''Generate data from clearsky model, using data defined in the constructor'''
        clearsky = self.loc.get_clearsky(self.times)
        solar_pos = self.loc.get_solarposition(times=self.times)
        POA_irrad = pvlib.irradiance.get_total_irradiance(surface_tilt=tilt, surface_azimuth=azim,
                                                            dni=clearsky['dni'], ghi=clearsky['ghi'], dhi=clearsky['dhi'],
                                                            solar_zenith=solar_pos['apparent_zenith'], 
                                                            solar_azimuth=solar_pos['azimuth'])
        self.poa_df = pd.DataFrame({'POA': POA_irrad['poa_global']})

    def plotday(self, days=None):
        '''Basic plots to check things are working ok'''
        if not HASMPL:
            print("MatPlotlib not installed : skipping graphs")
            return
        self.poa_df_dy = self.poa_df.copy()
        self.poa_df_dy2 = self.poa_df.copy()
        # Winter
        self.poa_df_dy['Date'] = self.poa_df_dy.index
        self.poa_df_dy = self.poa_df_dy[(self.poa_df_dy['Date'] > '2023-01-01 00:00') & (self.poa_df_dy['Date'] < '2023-01-01 23:59')]
        self.poa_df_dy.index = self.poa_df_dy.index.strftime("%H:%M")
        # Summer (surely it's possible to do this in pandas without all the copy stuff !!)
        self.poa_df_dy2['Date'] = self.poa_df_dy2.index
        self.poa_df_dy2 = self.poa_df_dy2[(self.poa_df_dy2['Date'] >= '2023-06-06 00:00') & (self.poa_df_dy2['Date'] < '2023-06-06 23:59')]
        self.poa_df_dy2.index = self.poa_df_dy2.index.strftime("%H:%M")

        ax = self.poa_df_dy['POA'].plot()
        self.poa_df_dy2['POA'].plot(ax=ax)
        ax.set_title("Beam Irradiance on Plane of Array")
        ax.set_xlabel("Time "+self.tz)
        ax.set_ylabel("Irradiance ($Wm^{-2}$)")
        pyplot.show()

    def savedata(self, filep=r"modeldata.json"):
        '''Save dataframe to a file (type depending on extension - json, csv or pqt/parquet)'''
        ext=os.path.splitext(filep)[1]
        print("Saving dataframe in", filep, " (a", ext.replace(".", ""), "file)")
        if ext == ".json":
            file = self.poa_df.to_json(filep)
        elif ext == ".csv":
            file = self.poa_df.to_csv(filep)
        elif ext == ".pqt" or ext == ".parquet":
            file = self.poa_df.to_parquet(filep)


class IrData():

    def __init__(self):
        self.waypoint = None
        self.Idataframe = None  # Dont use this do I ? Yeah just use a generic zip below


class IrStore():
    # Class to hold multiple irradiance data frames (generic IrData).
    def __init__(self):
        '''clist is a combined list containing pvlib dataframes & the position of the dataframe (waypoint obj)'''
        self.waypoints = []
        self.dflist = []
        self.clist = None

    def SetWaypoints(self, waypoints):
        self.waypoints = waypoints

    def LoadAllFiles(self, nconv="modeldata_"):
        '''Load-in every modeldata file matching the pattern define in nconv'''
        lmodeldata = glob.glob(nconv + '*.*')
        if DEBUG:
            print("Data-files that match expression : ", lmodeldata)
        for modeldata in lmodeldata:
            dfout = self.LoadMD(modeldata)
            self.dflist.append(dfout)
        self.clist = list(zip(self.waypoints, self.dflist))

    def LoadMD(self, modeldata):
        '''Load in modeldata (file path)'''
        ext = os.path.splitext(modeldata)[1]
        print("Loading dataframe from ", modeldata, " (a", ext.replace(".", ""), "file)")
        if ext == ".json":
            dfout = pd.read_json(modeldata)
        elif ext == ".csv":
            dfout = pd.read_csv(modeldata)
        elif ext == ".pqt" or ext == ".parquet":
            dfout = pd.read_parquet(modeldata)
        return dfout
    
    def GetNDF(self, position):
        '''Gets the nearest data-frame in space (by geodesic) stored within the object, to the position (lat,lon)'''
        # Loop to get closest position (again this can be shortend to speed things up if needed)
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
        '''Take a waypoint object & a datetime string, and then return the best irradiance (nearest in space & time)'''
        ndf = self.GetNDF(position)
        # Get the right data using the datetime obj, ie. nearest index to datetime
        dt = pd.to_datetime(datetime)
        irow = ndf[1].index.get_indexer([dt], method='nearest')[0]
        irrval = ndf[1].iat[irow, 0]
        print("Getting Irradiance :", irrval, "at", datetime)
        return irrval

def testIrList():
    from waypoints import FlightPath
    fpTest = FlightPath()
    fpTest.LoadIData()
    DEBUG = True
    irTest = IrStore()
    irTest.SetWaypoints(fpTest.iwaypoints)
    irTest.LoadAllFiles()
    print(type(irTest.clist), len(list(irTest.clist)))
    print(irTest.clist[0][1])
