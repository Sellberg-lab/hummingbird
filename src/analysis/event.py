import collections
import datetime
import ipc

def printKeys(evt):
    print evt.keys()    

def printNativeKeys(evt):
    print evt.nativeKeys()

def printID(eventID):
    for k,v in eventID.iteritems():
        print "%s = %s" %(k, v.data)
        try:
            print "datetime64 = %s" %(v.datetime64)
        except AttributeError:
            pass
        try:
            print "fiducials = %s" %(v.fiducials)
        except AttributeError:
            pass
        try:
            print "run = %s" %(v.run)
        except AttributeError:
            pass
        try:
            print "ticks = %s" %(v.ticks)
        except AttributeError:
            pass
        try:
            print "vector = %s" %(v.vector)
        except AttributeError:
            pass

eventFiducialDeque = collections.deque([],100)
def plotFiducial(eventID):
    for k,v in eventID.iteritems():
        eventFiducialDeque.append(v.fiducials)
        ipc.set_data("Event Fiducials", eventFiducialDeque)

processingTimes = collections.deque([], 100)

def printProcessingRate(evt = None):
    processingTimes.appendleft(datetime.datetime.now())
    dt = processingTimes[0] - processingTimes[-1]
    if(len(processingTimes) > 1):
        print "Processing at %g Hz" % ((len(processingTimes)-1)/dt.total_seconds())
    
