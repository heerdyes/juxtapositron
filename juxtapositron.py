#!/usr/bin/env python3

import midiarr
import kromectl
import mpd218ctl
import threading
import time
import sys

# globals
ma=None  # the software arranger itself (midiarr.MidArr)
mpd=None # akai mpd 218 pad controller
kk=None  # korg krome 61 workstation

''' the akai mpd pad controller handler/sensor '''
def mpdhandler(mmsg):
  print('received midi msg: %s'%mmsg)
  if len(mmsg)!=3:
    print('non triplet midi msg. ignoring.')
    return
  status,note,velo=mmsg
  # bank AB pad 1 quits the program
  if note==64 and status==128:
    print('stop scanning!')
    mpd.togglescan()
    ma.paused=True
  if note>=36 and note<=60 and status//16==0x9:
    padid=mpd.getpadid(note)
    if padid in ma.padmap:
      ma.actvtrknm=ma.padmap[mpd.getpadid(note)]
      ma.actvtrkvelo=velo
      print('[activetraq] %s'%ma.actvtrknm)

''' the akai mpd monitor thread flow '''
def mpdmon():
  global mpd
  mpd.notifymidi(mpdhandler)

''' the arranger thread flow '''
def arrangerctl(arrfile):
  global ma
  print('[arr] initial sleep for 1s')
  time.sleep(1)
  print('beginning play')
  ma.play(kk) # play loops till pad exit ctrl detected
  kk.closeio()


print('welcome to the juxtapositron!')

# the gate
if len(sys.argv)!=2:
  print('[usage] ./juxtapositron.py <arrangementfile>.arr')
  raise SystemExit

arrfile=sys.argv[1]
with open('dev.cfg') as cfg:
  cfglns=cfg.readlines()
  cfg=[cln.strip() for cln in cfglns]
mpdfile=cfg[0]
krmfile=cfg[1]
sndfile=cfg[2]
ma=midiarr.MidArr(arrfile)
mpd=mpd218ctl.MPD218(mpdfile)
kk=kromectl.Krome61(krmfile,sndfile)

# thread it
tmon=threading.Thread(target=mpdmon)
tarr=threading.Thread(target=arrangerctl,args=(arrfile,))

tmon.start()
tarr.start()

tmon.join()
tarr.join()

