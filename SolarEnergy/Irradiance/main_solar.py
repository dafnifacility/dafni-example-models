from irradiance import GenModel
from waypoints import FlightPath

from zipfile import ZipFile

import os
import glob
import argparse

#If DAFNI
isDAFNI = os.environ.get("ISDAFNI")
# Takes an input of either a single point, or a csv/json file

gPATHI = ""
gPATHO = ""
gDEBUG = False

# Pre-amble to setup folders
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
    print("Not running within DAFNI, using run directory")


class Inputs():

    def __init__(self, ArgObj=None):
        if ArgObj == None:
            # No ArgParser, use environments (ie. running in DAFNI)
            self.inFile = os.environ.get("INFILE")  # either .json or .csv or "None"
            self.Lon = float(os.environ.get("LON"))
            self.Lat = float(os.environ.get("LAT"))
            self.Alt = float(os.environ.get("ALT"))
            self.Tilt = float(os.environ.get("TILT"))
            self.Azim = float(os.environ.get("AZIM"))
            self.StartDayTime = os.environ.get("STARTDAYTIME")
            self.NumInc = float(os.environ.get("NDAYS"))
        else:
            self.inFile = ArgObj.inFile
            self.Lon = ArgObj.lon
            self.Lat = ArgObj.lat
            self.Alt = ArgObj.alt
            self.Tilt = ArgObj.tilt
            self.Azim = ArgObj.azim
            self.StartDayTime = ArgObj.startdaytime
            self.NumInc = ArgObj.ndays


def main():
    # Setup Args
    inp = None
    parser = None
    # fromFile = False
    if isDAFNI == "True":
        inp = Inputs()
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('--inFile', type=str, default="None")
        parser.add_argument('--lon', type=float)
        parser.add_argument('--lat', type=float)
        parser.add_argument('--alt', type=float, default=-999.0)
        parser.add_argument('--tilt', type=float)
        parser.add_argument('--azim', type=float)
        parser.add_argument('--startdaytime', type=str)
        parser.add_argument('--ndays', type=int, default=14)
        args = parser.parse_args()
        inp = Inputs(args)
    # Either running from a file, or from the inputted coordinates.
    if inp.inFile == "None" or inp.inFile == None:
        # Generate single point model (don't load WB data)
        print("Generating model data for (lon/lat)", inp.Lon, inp.Lat)
        glvl = GenModel(lat=inp.Lat, lon=inp.Lon, days=inp.NumInc, tilt=inp.Tilt, tz='UTC', startday=inp.StartDayTime, altover=inp.Alt, azim=inp.Azim)
        print(glvl.poa_df) # the basic output
        if gDEBUG and isDAFNI == "False":
            glvl.plotday()
        print(gPATHO)
        print(os.path.join(gPATHO, "modeldata.json"))
        glvl.savedata(os.path.join(gPATHO, "modeldata.json"))
    else:
        # Load from file. This will be waypoints (including intermediate for now).
        if isDAFNI == "True":
            spath = os.path.join(os.path.join(gPATHI, "waypoints_*.csv"))
            iddfp = glob.glob(spath)
            if len(iddfp) == 1:
                datafp = os.path.join(iddfp[0])
            else:
                datafp = os.path.join(os.path.join(gPATHI, "waypoints.csv"))
        else:
            datafp = os.path.join(os.path.join(gPATHI, inp.inFile))
        print("Loading journey from Waypoint file, with a start time of", inp.StartDayTime)
        xfp = FlightPath(iniday=inp.StartDayTime)
        xfp.LoadIData(datafp) # Change this to be just the main points. Then do whatever path.py does !
        xfp.GenIData()
        idatafp = os.path.join(os.path.join(gPATHO, "iwaypoints.csv"))
        xfp.SaveIData(idatafp)
        # Create irrad data & save it with iwaypoints
        zfp = os.path.join(gPATHO, "helios.zip")
        zfile = ZipFile(zfp, 'w')
        zfile.write(idatafp, "iwaypoints.csv")
        for i, coord in enumerate(xfp.iwaypoints):
            glvl = GenModel(lat=coord.lat, lon=coord.lon, days=inp.NumInc, tilt=0.0, tz='UTC', startday=inp.StartDayTime, altover=coord.alt)
            filenam = "modeldata_" + str("{:04d}".format(i)) + ".json"
            glvl.savedata(os.path.join(gPATHO, filenam))
            # Note that I've changed the subsequent step to accept a zip file
            zfile.write(os.path.join(gPATHO, filenam), arcname=filenam)
        zfile.close()
        # Remove all the intermediate csv & modeldata_ files (not big files - to reduce dir clutter)
        os.remove(idatafp)
        files2rm = glob.glob(os.path.join(gPATHO, "modeldata_*.json"))
        for file in files2rm:
            os.remove(file)

if __name__ == "__main__":
    main()
