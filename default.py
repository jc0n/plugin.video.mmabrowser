#!/usr/bin/env python

import os
import socket
import sqlite3
import sys
import urllib
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

import resources.lib.library as library
from resources.lib.utils import *
from resources.lib.navigation import *

### get addon info
__addon__             = xbmcaddon.Addon()
__addonidint__        = int(sys.argv[1])
__addondir__          = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__addonname__         = __addon__.getAddonInfo('name')


xbmcplugin.setContent(__addonidint__, 'tvshows') 

## parse plugin arguments
params = get_params()

## get path
try:
    path = urllib.unquote_plus(params["path"])
except:
    path = "/"

# Usermenu:
def menu():

    options = ['Browse by Promotion', 'Browse by Fighter', 'All Events', 'Search']

    select = xbmcgui.Dialog().select("MMA Browser", options)
    log("Select: " + str(select))
    if select == -1:
        log("menu quit by user")
        return
    else:
        if select == 0:
            ## populate list of organisations
            xbmcplugin.addSortMethod(__addonidint__, xbmcplugin.SORT_METHOD_VIDEO_TITLE)
            xbmcplugin.addSortMethod(__addonidint__, xbmcplugin.SORT_METHOD_EPISODE)
            browseByOrganisation()
        elif select == 1:
            ## populate list of fighters
            xbmcplugin.addSortMethod(__addonidint__, xbmcplugin.SORT_METHOD_EPISODE)
            xbmcplugin.addSortMethod(__addonidint__, xbmcplugin.SORT_METHOD_VIDEO_TITLE)
            browseByFighter()
        elif select == 2:
            ## populate list of all events
            xbmcplugin.addSortMethod(__addonidint__, xbmcplugin.SORT_METHOD_DATE)
            xbmcplugin.addSortMethod(__addonidint__, xbmcplugin.SORT_METHOD_VIDEO_TITLE)
            allEvents()
        elif select == 3:
            ## populate list of all events
            searchAll()


log('Script path: %s' % path)
log('Library path: %s' % __addon__.getSetting("libraryPath"))

## check path and generate desired list
if path == "/":
    xbmc.sleep(5000)
    library.dialog.create(__addonname__, "MMA Browser", "Loading")
    library.scanLibrary()
    library.getMissingData()
    if __addon__.getSetting("checkMissingExtras") == 'true':
        library.getMissingExtras()
    library.dialog.close()
    xbmc.sleep(1000)
    mainMenu()
elif path.startswith("/browsebyorganisation"):
    log("path:%s" % path)
    organisation = path.replace('/browsebyorganisation','')
    log("organisation:%s" % organisation)
    ## populate list of events for a given organisation
    xbmcplugin.addSortMethod(__addonidint__, xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.addSortMethod(__addonidint__, xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    getEventsByOrganisation(organisation.lstrip('/'))
elif path.startswith("/browsebyfighter"):
    log("path:%s" % path)
    fighterID = path.replace('/browsebyfighter','')
    log("fighterID:%s" % fighterID)
    ## populate list of all events a given fighter has fought in
    xbmcplugin.addSortMethod(__addonidint__, xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.addSortMethod(__addonidint__, xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    getEventsByFighter(fighterID.lstrip('/'))
elif path.startswith("/getEvent/"):
    eventID = path.replace('/getEvent/','')
    ## populate list of all video files for a given event
    getEvent(eventID)

## finish adding items to list and display
xbmcplugin.endOfDirectory(__addonidint__)
