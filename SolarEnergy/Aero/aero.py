import math
from scipy import optimize
import CbData
from waypoints import Waypoint
import geopy
import geopy.distance
from geographiclib.geodesic import Geodesic
import numpy

gDEBUG = False

class Aeroplane:
    #Class set to quickly calc for heavier than air flight.
    # Power = 0.5 * density * Vf**3 * S * C * + Weight**2 / ((0.5 *density*V*S) * 3.14159 * e*AR)

    def __init__(self, wingspan=35.8, wingarea=174.0, panelarea=160.0, weight=2950.0, paradragcoef=0.025, OswaldEff=0.8):
        # Fixed aerodynamic parameters. Imperial Units !!
        self.b = wingspan # ft
        self.S = wingarea # ft2, note this is the wing-area not the PV area.
        self.PV = panelarea
        self.CD0 = paradragcoef # parasitic (non-lift drag) coeficient
        self.weight = weight # in lbs (US/UK the same)
        self.e = OswaldEff   # This is a correction for excess drag (lift), compared to ideal elliptical wing.
        self._SetAspectRatio()
        # Positional stuff
        self.speed = None # mph
        self.altitude = None
        self.chkspeed = None # When checking stall/max speed.
        self.position = None # Position in Lat/Long/alt. Waypoint class.
        self.oldpos = None # The position at start of iteration
        self.time = 0.0 # Journey Timer, in minutes.
        self.dt = 10.0  # minutes, clock increment.
        # Engine related
        self.maxpower = 70.0
        self.maxbattpack = 633.0*260.0 * 3600.0   # BattWeight(kg)*Density, in Watt-hrs, conv. to Joules with 3600 (60x60)
        self.currentbatt = self.maxbattpack # Start at full battery power
        self.egain = 0.0 # Energy loss & gain in last time increment.
        self.eloss = 0.0
        self.irrad = 0.0 # Irradiance for iteration
        self.record = []
        self.recordPD = []
        # Constants (propeff will depend on height - ie. airdensity, to a 1/3 power I think ?)
        self.pveff = 0.3  # Panel Conv. efficiency, mono-cryst Si cells. (typically ~0.3 ballpark)
        self.chargeff = 0.9    # Typ. 0.6-0.9
        self.motoreff = 0.94   # includes batt->motor losses. 
        self.propeff = 0.85    # https://web.mit.edu/16.unified/www/FALL/thermodynamics/notes/node86.html
        # conversion factors
        self.convert = {"km2miles": 0.621371, "miles2km": 1.609344,
                        "kmph2fps": 0.911344, "fps2kmph": 1.09728,
                        "fps2mph": 0.681818, "mph2fps": 1.46667,
                        "ft22m2": 0.092903, "m22ft2": 10.7639,
                        "kgpm32slugspft3": 0.00194032, "slugspft32kgpm3": 515.37891,
                        "kgpm32lbpft3": 0.062428, "lbpft32kgpm3": 16.01}
        self.startdatetime = None

    def Move(self, ctarget):
        # Note fix the speed to get this working in DAFNI, easy to change later.
        self.CheckSpeed(h=self.position.alt)
        # Get the power (irad) for this position
        #print("Currently at : ", self.position.lon, self.position.lat, "(travelling to ", ctarget.lon, ctarget.lat, ")")
        gds = Geodesic.WGS84.Inverse(self.position.lat, self.position.lon, ctarget.lat, ctarget.lon )
        bearing = gds['azi1']
        self.oldpos = self.position
        # Iterate fowards
        dist = self.speed*(self.dt/60.0)*self.convert.get('miles2km')   # distance moved in km. Cvrt mph to kmph. Div by 60 mins for hrs.
        mdist = geopy.distance.distance(kilometers=dist)
        ip = mdist.destination((self.oldpos.lat, self.oldpos.lon), bearing=bearing) # Project forward to new pos. with geopy
        self.position = Waypoint(lat=ip.latitude, lon=ip.longitude, alt=self.position.alt, speed=self.speed)   # later on . height ... height ... height !!!
        self.time += self.dt
        print("Moved ", dist, " km towards : ", self.position.lon, self.position.lat, "alt=", self.position.alt )
        return

    def AtMWPNode(self, ctarget):
        # Are we near the position
        cmvdist = self.speed*(self.dt/60.0)*self.convert.get('miles2km')   # distance moved in kmh-1
        gds = Geodesic.WGS84.Inverse(self.position.lat, self.position.lon, ctarget.lat, ctarget.lon)
        dtct = gds['s12']/1000.0  # distance to ctarget. gds returns in m, 1000 to switch to km.
        print("Dist to WP / it.dist", dtct, cmvdist)
        if dtct < cmvdist:
            return True
        else:
            return False

    def UpdateEngineState(self, pIrData=None):
        '''pIrData is the data object for the combined wp/irrad object'''
        # Power use & refuel ... almost there now
        print("Updating Engine State")
        from datetime import datetime, timedelta # to top
        currclk = datetime.fromisoformat(self.startdatetime)  + timedelta(minutes=self.time)
        energy_used = self.PowerReqSI(Vf=self.speed*self.convert.get('mph2fps'), h=self.position.alt)/(self.motoreff*self.propeff)*self.dt*60.0 # Speed to ft/s
        energy_gained = self.GetIrrad(pIrData, currclk)*self.chargeff*self.pveff*self.dt*60.0*self.S*self.convert.get('ft22m2') # Factor is ft2 to m2 ! was 800.0
        print("Energy Used", energy_used/1000000.0, " & Energy Gained", energy_gained/1000000.0, " (in MJ)")
        print("-------------------------------------------")
        updatebatt = self.currentbatt + (energy_gained - energy_used)
        self.currentbatt = min(self.maxbattpack, updatebatt)
        self.eloss = energy_used # by engine (J)
        self.egain = energy_gained # by PV Panel
        return

    def RecordIteration(self):
        '''Records the status of the plane at the end of each iteration. (nb. will not include last WP & start.)'''
        storeit = [self.time, self.speed, self.position.lon, self.position.lat, self.position.alt, self.irrad, 
                   self.eloss, self.egain, self.currentbatt, round(100.0*self.currentbatt/self.maxbattpack, 3)]
        self.record.append(storeit)

    def RecordPerformance(self):
        '''Records the performance curves of the aircraft, including stall/max speeds and climb info'''
        heightl = numpy.linspace(0.0, 11000.0, 110)
        speedl = numpy.linspace(15.0, 115.0, 100)
        for height in heightl:
            sthtl = []
            sthtl.append(height)
            sthtl.append(self.AirDensity(height)*self.convert.get('slugspft32kgpm3'))   # Convert dens. to SI for output.
            sthtl.append(self.T(h=height)-273.15)     # 273.15 converts to Centigrade
            sthtl.append(self.GetStall(height))
            sthtl.append(self.GetMaxVelocityBounds(scl=self.maxpower, h=height))
            tspdl = []
            for spd in speedl:
                tmpl = []
                tmpl.append(spd)
                tmpl.append(self.maxpower)
                tmpl.append(self.PowerReqHP(Vf=spd*self.convert.get('mph2fps'), h=height)) # KJS wip
                tspdl.append(tmpl)
            sthtl.append(tspdl)
            self.recordPD.append(sthtl)

    def GetIrrad(self, pIrDataObj, datetime):
        '''Get Irrd from nearest co-ord/time. pIrDataObj is a combined object (see irradiance.py)'''
        ir = pIrDataObj.GetIrradiance(self.position, datetime)
        self.irrad = ir
        print("Returning GetIrrad", ir)
        return ir

    def _SetAspectRatio(self):
        '''Returns the aspect ratio = Wingspan**2/Wing area (both are in ft)'''
        self.AR = self.b**2/self.S
        print("Aspect Ratio is ", self.AR)

    def _GVB_ftn(self, Vf, scl, h=0.0):
        '''Internal function used to evaluate roots of the power curve (Newton-Raphson method)'''
        '''Units (mix of Imp. & SI): velocity in fps, scl (power) in hp, h(eight) in m'''
        return self.PowerReqHP(Vf, h)-scl

    def GetMaxVelocityBounds(self, scl=70.0, h=0.0): # Fix height dependence donem scl is max power ... neaten this
        '''Returns the maximum speed in mph (from the power-curve). scl is the max engine power (hp), h in meters'''
        # P(vf) - scl = PowerReqHP(self, Vf) -scl  # hcl & h are fixed params in the root finding
        v2 = optimize.newton(self._GVB_ftn, 100.0, args=(scl, h,))  # 100.0 is a start estimate for the root.
        print("v2 = ", v2*self.convert.get('fps2mph')) # 0.681 is fts-1 -> mph
        return v2*self.convert.get('fps2mph')

    def GetStall(self, h=0.0):
        '''Returns the stall speed in mph. height in metres'''
        vs = math.sqrt(2.0*self.weight/(self.AirDensity(h)*self.S*1.5)) # CL_max to 1.5 ? (1-2,  with flaps - no idea ?)
        print("Stall Speed =", vs*self.convert.get('fps2mph'))
        return vs*self.convert.get('fps2mph')

    def CheckSpeed(self, h=0.0):
        '''Check that speed is within level flight bounds, given h(m), & internal speeds in mph.'''
        if self.GetStall(h) > self.GetMaxVelocityBounds(h=h):
            print("Warning: not enough power for level flight.")
            return
        self.chkspeed = self.speed
        self.speed = max(self.GetStall(h), self.speed)
        print(self.speed)
        self.speed = min(self.GetMaxVelocityBounds(h=h), self.speed)
        print(self.speed)
        if (self.speed-self.chkspeed) > 1.0E-4:
            print("Speed outwith bounds (stall or max), & has been set to ", self.speed, "from ", self.chkspeed)

    # Evaluate the Thrust/Power required for level flight at velocity Vf
    def ThrustReq(self, Vf, h=0.0):
        '''Evaluates the thrust(lbf) needed for a given velocity-TAS(fps) and height(m).'''
        Thr = self.weight / (self.CL(Vf, h)/self.CD(Vf, h))   # W/(L/D), where L/D = CL/CD
        return Thr

    def PowerReq(self, Vf, h=0.0):
        '''Evaluates the power(f.lb/s) needed for level flight, given velocity-TAS(fps) and height(m).'''
        PReq = self.ThrustReq(Vf, h) * Vf
        return PReq

    def ThrustReqSI(self, Vf, h=0.0):
        '''Evaluates the thrust(N) needed for level flight, given velocity-TAS(fps) and height(m).'''
        return self.ThrustReq(Vf, h) * 4.448  # lbf -> Newtons

    def PowerReqSI(self, Vf, h=0.0):
        '''Evaluates the power(W) needed for level flight, given velocity-TAS(fps) and height(m).'''
        return self.PowerReq(Vf, h)*1.36 # Feet.lb/s -> Watts

    def PowerReqHP(self, Vf, h=0.0):
        '''Evaluates the power(hp) needed for level flight, given velocity-TAS(fps) and height(m).'''
        return self.PowerReq(Vf, h)/550.0 # Feet.lb/s -> hp

    def CL(self, Vf, h=0.0):
        '''Lift coefficient given vf(fps) and h(m)'''
        CL = self.weight / (0.5 * self.AirDensity(h) * self.S * Vf**2)
        #print("CL = ", CL)
        return CL

    def CD(self, Vf, h=0.0):
        '''Drag coefficient given vf(fps) and h(m)'''
        CD = self.CD0 + self.CL(Vf, h)*self.CL(Vf, h) / (math.pi * self.e *self.AR)
        return CD

    def AirDensity(self, h=0.0): # h in metres
        '''ISA Standard Atm. given h(m). Returns air density in slugs per ft^3. Only good to 11,000m'''
        # rho = rho_0*(T/T_0)^alpha , where alpha = -[g_0/(a*R)+1] , 
        # a=dT/dh=-0.0065 Km^-1 for the 1st adb layer, and T=T_0+a(h-h0). rho_0 = 1.225 kgm^-3, h0=0m for this, T0=288.6 K
        g0 = 9.81 # m/s2
        rho0 = 1.225 # (h=0 density) kg/m3
        T0 = 288.16 # (h=0 Std Temp) Kelvin (o dg = 273.15)
        a = -0.0065 # (adb layer 1 Lapse rate) Kelvin/m
        R = 287.0 # J/kgK
        alpha = -1.0*(g0/(a*R) + 1.0)
        T = self.T(T0, a, h)
        rho = rho0*(T/T0)**alpha
        if gDEBUG:
            print("Density = ", rho, "@", h, "m", " T=", T)
        density = rho*self.convert.get("kgpm32slugspft3")
        return density
    
    def T(self, T0=288.16, a=-0.0065, h=0): # fix this properly @ not 8am. KJS
        '''Temp as ftn of h(m). T0(K) & a(K/m) define the troposphere (ISA St.Atm.)'''
        T = T0 + a*h
        return T

