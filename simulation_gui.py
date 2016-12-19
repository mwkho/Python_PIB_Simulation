from simulation_calc import OneD_simulate
import gi
import numpy as np
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

# creating the gui for the simulation
hbar="HBar"
mass="Mass"
L = "Length of box"
numPoints="Number of quadratures"
numBasis="Number of basis functions"
gx= "Wavefunction to simulate\n (in python syntax)"
time="Time duration"

class Windows(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="PIB/HO Simulations")
        
        # grid settings
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(20)
        self.grid.set_row_spacing(10)
        self.add(self.grid)
        
        #creating text entries and labels
        self.hbar = Gtk.Entry()
        self.hbar_label  = Gtk.Label(hbar)
        self.hbar_label.set_justify(Gtk.Justification.LEFT)
        
        self.mass = Gtk.Entry()
        self.mass_label  = Gtk.Label(mass)
        self.mass_label.set_justify(Gtk.Justification.LEFT)
        
        self.L = Gtk.Entry()
        self.L_label  = Gtk.Label(L)
        self.L_label.set_justify(Gtk.Justification.LEFT)
        
        self.numPoints = Gtk.Entry()
        self.numPoints_label  = Gtk.Label(numPoints)
        self.numPoints_label.set_justify(Gtk.Justification.LEFT)
        
        self.numBasis = Gtk.Entry()
        self.numBasis_label=Gtk.Label(numBasis)
        
        self.gx = Gtk.Entry()
        self.gx_label=Gtk.Label(gx)
        
        self.time= Gtk.Entry()
        self.time_label = Gtk.Label(time)
        
        # creating basis choice
        self.hbox = Gtk.Box(spacing=10)
        self.PIB = Gtk.RadioButton.new_with_label_from_widget(None,"PIB")
        self.PIB.connect("toggled",self.basis_select ,"PIB")
        self.hbox.pack_start(self.PIB, False, False, 0)
        
        '''
        self.HO = Gtk.RadioButton.new_from_widget(self.PIB)
        self.HO.set_label("HO")
        self.HO.connect("toggled", self.basis_select, "HO")
        self.hbox.pack_start(self.HO, False, False, 0)
        '''
        self.basis_label = Gtk.Label("Basis functions")
        
        # creating simulate button
        self.simulate = Gtk.Button(label = "Simulate")   
        self.simulate.connect("clicked",self.button_click)

        #putting the window together
        self.grid.add(self.hbar_label)
        self.grid.attach_next_to(self.mass_label,self.hbar_label, Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.L_label,self.mass_label, Gtk.PositionType.BOTTOM,1,1)
       # self.grid.attach_next_to(self.Max_label,self.Min_label, Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.numPoints_label,self.L_label, Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.numBasis_label,self.numPoints_label, Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.gx_label,self.numBasis_label, Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.time_label,self.gx_label, Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.basis_label,self.time_label, Gtk.PositionType.BOTTOM,1,1)
        
        self.grid.attach_next_to(self.hbar, self.hbar_label, Gtk.PositionType.RIGHT,1,1)
        self.grid.attach_next_to(self.mass, self.mass_label, Gtk.PositionType.RIGHT,1,1)
        self.grid.attach_next_to(self.L, self.L_label, Gtk.PositionType.RIGHT,1,1)
        #self.grid.attach_next_to(self.Max, self.Max_label, Gtk.PositionType.RIGHT,1,1)
        self.grid.attach_next_to(self.numPoints, self.numPoints_label, Gtk.PositionType.RIGHT,1,1)
        self.grid.attach_next_to(self.numBasis, self.numBasis_label, Gtk.PositionType.RIGHT,1,1)
        self.grid.attach_next_to(self.gx, self.gx_label, Gtk.PositionType.RIGHT,1,1)
        self.grid.attach_next_to(self.time, self.time_label, Gtk.PositionType.RIGHT,1,1)
        self.grid.attach_next_to(self.hbox, self.basis_label, Gtk.PositionType.RIGHT,1,1)
        
        self.grid.attach_next_to(self.simulate,self.basis_label,Gtk.PositionType.BOTTOM,1,1)
        
        #animation attributes
        self.simulator = OneD_simulate()
        
    def button_click(self, widget):
        '''(WIndows, Gtk.Widget) -> None
        Function that simulates upon button click
        '''
        # create dictionary of entry name to value w/o gx
        entry_to_value = dict()
        entry_to_value[hbar] = self.hbar.get_text()
        entry_to_value[mass] = self.mass.get_text()
        entry_to_value[L] = self.L.get_text()
        #entry_to_value[Max] = self.Max.get_text()
        entry_to_value[numPoints] = self.numPoints.get_text()
        entry_to_value[numBasis] = self.numBasis.get_text()
        entry_to_value[time] = self.time.get_text()
        
        # check for valid entries 
        test = checkAll(entry_to_value)
        if(not test):
            entry_to_value.clear()
            return
            
        #check Min and Max values
       # test = checkMinMax(entry_to_value[Min], entry_to_value[Max])
       # if(not test):
       #     print("Min must be strictly less than Max\n")
       #     return

        #final adjustments to dict of items
        entry_to_value[numBasis] =int(entry_to_value[numBasis])
        entry_to_value[numPoints] = int(entry_to_value[numPoints])
    
        x = np.linspace(0,entry_to_value[L],entry_to_value[numPoints])
        #x = np.linspace(0,10,1000)
        #gx = eval("x**2")
        
        # parse wavefunction
        gx =self.gx.get_text()
        try:
            ## use eval(learn to do it safely) or use pyparsing
            wf = eval(gx)
            
            if(type(wf) == int):
                raise ValueError
        except ValueError:
            print("please do not put in numbers as the wavefunction")
            entry_to_value.clear()
            return
        except Exception:
            print("invalid wavefunction, please type it with proper syntax.\n"+ 
            "NOTE: numpy has been imported as np")
            entry_to_value.clear()
            return        

        #simulate when button pressed
        try:
            ani = self.simulator.simulate(entry_to_value[hbar],entry_to_value[mass],
                                      entry_to_value[L],entry_to_value[numPoints],
                                      x, entry_to_value[numBasis], wf,
                                      entry_to_value[time])
        except AttributeError:
            print("check your parameters again")
            return
        return

    def basis_select(self, button, name):
        ##TODO##           
        return

def checkAll(mydict):
    truth = checkFloat(mydict)
    if(not truth):
        return truth
    truth = checkPositive(mydict)
    if (not truth):
        return truth
    truth = checkMorePoints(mydict)
    if(not truth):
        return truth
    return True

def checkFloat(mydict):
    '''(dict) -> bool
    Returns False if all values in mydict are not float strings, otherwise
    return True.
    '''
    for key in mydict.keys():
        try:
            mydict[key] = float(mydict[key])
        except ValueError:
            print(key+ " is in an invalid form, please revise it")
            return False
    return True

def checkPositive(mydict):
    '''(dict)->bool
    Check if the values for the keys, 
    "hbar, mass, numPoints, numBasis, time, L"
    are postive. Returns True if they are, otherwise return False.
    '''
    for key in [hbar, mass, numPoints, numBasis, time, L]:
        if (mydict[key] < 0):
            print(key+ " must be nonegative")
            return False
    return True

def checkMorePoints(mydict):
    '''(dict)-bool
    Returns True if mydict[numPoints] is >=2, returns False otherwise.
    '''
    if (mydict[numPoints] < 2):
        print("Number of quadratures must be >=2")
        return False
    return True

# calling the simulation once 
win=Windows()
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()
