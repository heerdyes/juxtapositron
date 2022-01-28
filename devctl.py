import os

class MidiDev:
  def __init__(self,desc='generic midi device',mf=None):
    self.desc=desc
    self.midifile=mf
    self.midifh=None
    
  def midion(self,ch,note,velo):
    midimsg=[0x90+ch,note,velo]
    midiseq=bytearray(midimsg)
    if self.midifh:
      os.write(self.midifh,midiseq)
    
  def midioff(self,ch,note,velo):
    midimsg=[0x80+ch,note,velo]
    midiseq=bytearray(midimsg)
    if self.midifh:
      os.write(self.midifh,midiseq)
      
  def closeio(self):
    if self.midifh:
      os.close(self.midifh)
      
  def __str__(self):
    return '[%s] target: %s'%(self.desc,self.midifile)

