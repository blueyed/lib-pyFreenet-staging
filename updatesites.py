#!/usr/bin/env python

import sys, os, time, commands
import sitemgr

# time we wait after starting fred, to allow the node to 'warm up'
# and make connections to its peers
startupTime = 180

# directory where we have freenet installed,
# change it as needed
freenetDir = "/home/david/freenet"

# derive path of freenet pid file, the (non)existence
# of which is the easiest test of whether the freenet
# node is running
pidFile = os.path.join(freenetDir, "Freenet.pid")

# small wrapper which, if freenet isn't already running,
# starts it prior to inserting then stops it after
# inserting
def main(verbose=None):

    if verbose == None:
        verbose = ('-v' in sys.argv)

    print "--------------------------------------------"
    print "Start of site updating run"
    
    # start freenet and let it warm up, if it's not already running
    if not os.path.isfile(pidFile):
        startingFreenet = True
        os.chdir(freenetDir)
        print "Starting freenet..."
        print commands.getstatusoutput("%s/start.sh &" % freenetDir)
        print "Letting node settle for %s seconds..." % startupTime
        time.sleep(startupTime)
    else:
        print "Freenet node is already running!"
        startingFreenet = False

    # add verbosity argument if needed    
    if verbose:
        kw = {"verbosity" : sitemgr.fcp.DETAIL}
    else:
        kw = {}

    # get a site manager object, and perform the actual insertions
    s = sitemgr.SiteMgr(**kw)
    s.update()
    del s
    
    # kill freenet if it was dynamically started
    if startingFreenet:
        print "Waiting %s for inserts to finish..." % startupTime
        time.sleep(startupTime)
        print "Stopping node..."
        os.system("./run.sh stop")
        print "Node stopped"

if __name__ == '__main__':
    main()
