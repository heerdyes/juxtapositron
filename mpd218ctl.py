import time
import os
from devctl import *

"""
  input abstraction for the akai mpd218 pad controller
"""
class MPD218(MidiDev):
  def __init__(self,mdfl=None):
    super().__init__('akai mpd218 pad controller',mdfl)
    self.scanning=True
    if self.midifile:
      self.midifh=os.open(self.midifile,os.O_RDWR)

  def togglescan(self):
    self.scanning=not self.scanning

  def readmidimsg(self):
    if self.midifh:
      return os.read(self.midifh,3)

  def notifymidi(self,callback):
    if self.midifh:
      while self.scanning:
        mmsg=os.read(self.midifh,3)
        callback(list(mmsg))

  def getpadid(self,note):
    if note==36:
      return 'pad1'
    if note==38:
      return 'pad2'
    if note==40:
      return 'pad3'
    if note==41:
      return 'pad4'
    if note==43:
      return 'pad5'
    if note==45:
      return 'pad6'


def midihandler(mmsg):
  print('received midi msg: %s'%mmsg)
  status,note,velo=mmsg
  # bank AB pad 1 quits the program
  if note==64 and status==128:
    print('stop scanning!')
    mpd.togglescan()

def greet(mdev,dly):
  print('greeting pattern')
  padlst=[36,38,40,41,43,45,47,48,50,52,53,55,57,59,60]
  for i in padlst:
    mdev.midion(0,i,64)
  time.sleep(dly)
  for i in padlst:
    mdev.midioff(0,i,64)

# program flow
if __name__=='__main__':
  mpd=MPD218('/dev/midi2')
  print(str(mpd))
  greet(mpd,1.0)
  print('[delay] 0.5s')
  time.sleep(0.5)
  print('monitoring...')
  mpd.notifymidi(midihandler)
  mpd.closeio()

