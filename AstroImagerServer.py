import time

import PyIndi

class AstroImagerServer(PyIndi.BaseClient):

    cmonitor = None

    '''
    Initialises a new Astro Imager server.
    '''
    def __init__(self):
        super(AstroImagerServer, self).__init__()
        self.setServer("localhost", 7624)

    def connectToINDIServer(self):
        self.connectServer()
        # wait CONNECTION property be defined
        while not(self.cmonitor):
            time.sleep(0.05)
    '''
    INDI Base Client methods - receiving INDI data
    '''
    def newDevice(self, d):
        global dmonitor
        # We catch the monitored device
        dmonitor=d
        print("New device ", d.getDeviceName())

    def newProperty(self, p):
        global monitored
        global cmonitor
        # we catch the "CONNECTION" property of the monitored device
        if (p.getName() == "CONNECTION"):
            cmonitor=p.getSwitch()
        print("New property ", p.getName(), " for device ", p.getDeviceName())

    def removeProperty(self, p):
        pass

    def newBLOB(self, bp):
        pass

    def newSwitch(self, svp):
        pass

    def newNumber(self, nvp):
        global newval
        global prop
        # We only monitor Number properties of the monitored device
        prop=nvp
        newval=True

    def newText(self, tvp):
        pass

    def newLight(self, lvp):
        pass

    def newMessage(self, d, m):
        pass

    def serverConnected(self):
        pass

    def serverDisconnected(self, code):
        pass

monitored="Telescope Simulator"
dmonitor=None

server = AstroImagerServer()
server.connectToINDIServer()

# we are only interested in the telescope device properties
#indiclient.watchDevice(monitored)


# if the monitored device is not connected, we do connect it
if not(dmonitor.isConnected()):
    # Property vectors are mapped to iterable Python objects
    # Hence we can access each element of the vector using Python indexing
    # each element of the "CONNECTION" vector is a ISwitch
    cmonitor[0].s=PyIndi.ISS_ON  # the "CONNECT" switch
    cmonitor[1].s=PyIndi.ISS_OFF # the "DISCONNECT" switch
    server.sendNewSwitch(cmonitor) # send this new value to the device

newval=False
prop=None

while (1):
    # we poll the newval global variable
    if (newval):
        print("newval for property", prop.name, " of device ",prop.device)
        # prop is a property vector, mapped to an iterable Python object
        for n in prop:
            # n is a INumber as we only monitor number vectors
            print(n.name, " = ", n.value)
        newval=False