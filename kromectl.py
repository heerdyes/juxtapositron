import os
from devctl import *

"""
  the korg krome synthesizer controller class
  tested for combi and sequencer modes
"""
class Krome61(MidiDev):
  def __init__(self,mdfl,sndfl):
    super().__init__('korg krome workstation',mdfl)
    self.sndfile=sndfl
    self.sndmap={}
    if self.midifile:
      self.midifh=os.open(self.midifile,os.O_WRONLY)
    if self.sndfile:
      self.loadsounds()

  def loadsounds(self):
    with open(self.sndfile) as sndf:
      sndlns=sndf.readlines()
      sndlns=[sndln.strip() for sndln in sndlns]
    for sln in sndlns:
      lr=sln.split('=')
      evtlst=[]
      for evt in lr[1].split():
        elr=evt.split('/')
        evtlst.append((int(elr[0]),int(elr[1])))
      self.sndmap[lr[0]]=evtlst
      
  # setup krome in seq mode with some drum kit on midi ch 10 (0x09)
  def getmidiinfo(self,sndnm,vol):
    if sndnm not in self.sndmap:
      raise Exception('no such sound %s'%sndnm)
    return [(cn[0],cn[1],vol) for cn in self.sndmap[sndnm]]


# program flow
if __name__=='__main__':
  kk=Krome61()
  print(str(kk))

