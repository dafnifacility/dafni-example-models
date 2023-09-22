import geopy
import geopy.distance
from geographiclib.geodesic import Geodesic
import itertools
import csv
from datetime import datetime, timedelta

gDEBUG = True

class FlightPath():

    def __init__(self, iniday=None, initime=None, inipos=None):
        self.iniday = iniday
        self.initime = initime
        self.inipos = inipos
        self.waypoints = [inipos]
        self.iwaypoints = None

    def GenIData(self):
        # Mark original waypoints as 1 (at some point I think it'll be best to redo this a bit so it's less clunky)
        for waypoint in self.waypoints:
            waypoint.id = 1
        if gDEBUG:
            print(len(self.waypoints), " Waypoints")
        # Create two waypoint interators (for looping over pairs)
        wpl1, wpl2 = itertools.tee(self.waypoints)
        next(wpl2, None)
        # Combine into waypoint pairs ()
        cwpl = zip(wpl1, wpl2)
        self.iwaypoints = []
        for i, wapn in enumerate(cwpl):
            if gDEBUG:
                print("Generating Flightpath Ir.Model Data for WP", i, 
                      "co-or", wapn[0].lon, wapn[0].lat," --> ", wapn[1].lon, wapn[1].lat)
            print(wapn[0])
            self.iwaypoints.append(wapn[0])
            self.__GenSubpoints(wp1=wapn[0], wp2=wapn[1])
        self.iwaypoints.append(self.waypoints[-1])

    def __GenSubpoints(self, wp1=None, wp2=None):
        # Generate wp1 Ir.data
        # Generate set of points between waypoints
        # i) Gen. geodisic (shortest path on ellipsoid) connecting wp1 & wp2
        gds = Geodesic.WGS84.Inverse(wp1.lat, wp1.lon, wp2.lat, wp2.lon ) # Arg.. bloody typo.. wp1 was usedx3 !!
        if gDEBUG:
            print("gds", gds)
        splt = int(gds['s12']/(20.0*1000.0)) - 1  # REM. s12 is in m's
        rmdr = gds['s12']%(20.0*1000.0)
        if rmdr > 0.0: # Only have final point if more than 10km to the dest.
            splt += 1
        if gDEBUG:
            print("Adding", splt, "sub-waypoints inbetween, distance is", gds['s12']/1000.0, "km")
        mdist = geopy.distance.distance(kilometers=20.0)
        iwp = wp1
        for i in range(splt):
            # Project 20km towards wp2 & create an intermediate wp. (rem ip is a geopy POINT, not my Waypoint class)
            ip = mdist.destination((iwp.lat, iwp.lon), bearing=gds['azi1'])
            iwp = Waypoint(lat=ip.latitude, lon=ip.longitude, alt=wp1.alt, speed=wp1.speed)
            self.iwaypoints.append(iwp)

    def PrintPoints(self):
        #print("Printing Main Waypoints")
        #for i, waypoint in enumerate(self.waypoints):
        #    print("point", i, waypoint.lon, waypoint.lat, waypoint.alt)
        print("Printing Full Set of Waypoints (inc. intermediates)")
        for i, iwaypoint in enumerate(self.iwaypoints):
            print("point", i, iwaypoint.lon, iwaypoint.lat, iwaypoint.alt, iwaypoint.speed, iwaypoint.id)

    def plotcourse(self):
        #import plotly.express as plx  # Need to pip this & create a flight-path dataframe for plotting.
        #fig = plx.line_mapbox(self.fpdf, lat="lat", lon="lon", color="State", zoom=3, height=300)
        #fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=2, mapbox_center_lat = 25.0, 
        #                  margin={"r":0,"t":0,"l":0,"b":0})
        #fig.show()
        pass

    def SaveIData(self, savf='waypoints.csv'):
        # Loop over all the sub-waypoint data & save it.
        csvfs = open(savf, 'w', newline='')  # newline part needed or python will mess up the line spacing on Windows.
        for data in self.iwaypoints: # just save the data, nothing fancy
            tmplst = [data.lon, data.lat, data.alt, data.speed, data.id]
            wro = csv.writer(csvfs, quoting=csv.QUOTE_ALL)
            wro.writerow(tmplst)
        csvfs.close()

    def LoadIData(self, inf='waypoints.csv'):
        with open(inf, 'r', newline='') as info:
            rd = csv.reader(info)
            lldata = list(rd)
        if gDEBUG:
            print("Load")
            print(lldata)
        # Copy into the waypoints & iwaypoints object correctly
        self.waypoints = []
        self.iwaypoints = []
        for ldata in lldata:
            tmpwp = Waypoint(lon=float(ldata[0]), lat=float(ldata[1]), alt=float(ldata[2]), 
                             speed=float(ldata[3]), id=int(ldata[4]))
            self.iwaypoints.append(tmpwp)
            if tmpwp.id == 1:
                self.waypoints.append(tmpwp)
        # Note GenIData will create track of intermediate waypoints. # Naahh better to do this manually !
        #if len(self.waypoints) == len(self.iwaypoints):
        #    self.GenIData()

    #def LoadIrData


class Waypoint():
    
    def __init__(self, lon, lat, alt=-999, speed=36.0, id=0):
        # If alt=None assume close to ground
        self.lon = lon
        self.lat = lat
        self.alt = alt
        self.speed = speed
        self.id = id

    def print(self):
        print("waypoint(cls)", self.lon, self.lat, self.alt, self.speed, self.id)


class Clock():

    def __init__(self):
       # Work in utc & worry about local times later.
       self.time = datetime.utcnow()

    def AddTime(self, deltat=0.0):
        '''Add delta to time, use this for journey in utc'''
        return self.time + timedelta(hours=deltat) # nb. this does not advance the clock !
    
    def AdvanceTime(self, deltat=0.0):
        self.time += timedelta(hours=deltat)

