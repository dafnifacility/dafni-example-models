import json
import os
import argparse
from zipfile import ZipFile
from waypoints import FlightPath
from aero import Aeroplane
from CbData import IrStore

#If DAFNI
isDAFNI = os.environ.get("ISDAFNI")
# Other variables
gStartDayTime = os.environ.get("STARTDAYTIME")
gSpeed = os.environ.get("SPEED")

gPATHI = ""
gPATHO = ""
gDEBUG = True # False

# Pre-amble to setup folders
print("ISDAFNI Environment variable = ", isDAFNI, type(isDAFNI))
if isDAFNI == "True":
    if os.name == "nt":
        pren = os.environ.get("HOMEDRIVE")
    else:
        pren = "/"
    gPATHI = os.path.join(pren, "data", "inputs")
    gPATHO = os.path.join(pren, "data", "outputs")
    print("Running within DAFNI: ", gPATHO, gPATHI)
else:
    print("Not running within DAFNI, using run directory")


class Inputs():

    def __init__(self, ArgObj=None):
        if ArgObj == None:
            # No ArgParser, use environments (ie. running in DAFNI)
            self.StartDayTime = os.environ.get("STARTDAYTIME")
            self.Speed = float(os.environ.get("SPEED"))
        else:
            self.StartDayTime = ArgObj.startdaytime
            self.Speed = ArgObj.speed

def main():
        # Setup Args
    inp = None
    parser = None
    # fromFile = False
    if isDAFNI == "True":
        inp = Inputs()
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('--startdaytime', type=str)
        parser.add_argument('--speed', type=float)
        args = parser.parse_args()
        inp = Inputs(args)

    xfp, irTest = loaddata()
    # We want to use the earlist time from the index of the irradiance data, rather than setting it twice.
    if inp.StartDayTime == "" or inp.StartDayTime == None or inp.StartDayTime == "None":
        inp.StartDayTime = str(irTest.dflist[0].index[0])
    mwaypoints = []  # Setup the main waypoints for aeroplane iteration and movement.
    for coord in xfp.iwaypoints:
        if coord.id == 1:
            mwaypoints.append(coord)
    flcond = True   # switch to false after journey complete
    # Setup plane to resemble Solar Impulse II - coefs are educated estimates - they'll be in the right ball-park though.
    plane = Aeroplane(wingspan=236.0, wingarea=2900.0*0.92, panelarea=2900.0, weight=5100.0, paradragcoef=0.02, OswaldEff=0.85)
    # Set speed.
    plane.speed = mwaypoints[0].speed
    plane.position = mwaypoints[0]
    plane.startdatetime = inp.StartDayTime # gStartDayTime
    # Move plane
    tid = 1   # Target waypoint id
    currtwp = mwaypoints[tid]  # Target waypoint
    if gDEBUG:
        print("Check Irrad data : ", len(irTest.clist)) # Quick check of irTest combined list.
        print("================================")
    # REMEMBER to keep track of & update the global clock - do this through the aero class.
    while flcond == True:
        plane.Move(currtwp) # startcurrleg in the Wp1 needed for speed & alt.
        plane.UpdateEngineState(irTest) # Update & save the fuel status (battery charge in this case)
        plane.RecordIteration()
        # The clock is updated in the Move function.
        if plane.AtMWPNode(currtwp):
            print("Now at WP", currtwp.lon, currtwp.lat)
            # Adjust speed & alt to the previous target wp (which will then update below)
            plane.speed = currtwp.speed
            plane.position.speed = currtwp.speed
            plane.position.alt = currtwp.alt
            tid += 1
            if tid < len(mwaypoints):
                currtwp = mwaypoints[tid]
            else:
                break
    # Save the output data
    jfile = "flightrecord.json"
    ofilep = os.path.join(gPATHO, jfile)
    jsonfile = open(ofilep, "w")
    json.dump(plane.record, jsonfile, indent=4)
    jsonfile.close()
    # Also save the performance data
    plane.RecordPerformance()
    jpfile = "performrecord.json"
    pfilep = os.path.join(gPATHO, jpfile)
    jsonpfile = open(pfilep, "w")
    json.dump(plane.recordPD, jsonpfile, indent=4)
    jsonpfile.close()

def loaddata():
    # Unzip main data file (ir)
    zfip = os.path.join(gPATHI, "helios.zip")
    zfi = ZipFile(zfip, 'r') 
    zfi.extractall(gPATHI)
    zfi.close()
    # Load waypoints from file
    print("Loading waypoints")
    datafp = os.path.join(gPATHI, "iwaypoints.csv")
    xfp = FlightPath(iniday='2023-06-06', initime='02:00')  # Note this iniday/time isn't currently used.
    xfp.LoadIData(datafp)
    print("Finshed loading the waypoints")
    # Load irr data & link up 'main' waypoint list
    irTest = IrStore()
    irTest.SetWaypoints(xfp.iwaypoints)
    IrLp = os.path.join(gPATHI, "modeldata_")
    irTest.LoadAllFiles(nconv=IrLp)
    return xfp, irTest

if __name__ == "__main__":
    main()
