#!/usr/bin/env python3

import os
import sys
import time


''' the sequence abstraction '''
class Seq:
  def __init__(self,seqstr):
    self.data=seqstr
    self.seqlen=len(self.data)

  def __str__(self):
    return '[%s]'%self.data

  def getevt(self,frame):
    return self.data[frame%self.seqlen]


''' a sound sequence '''
class Sndseq(Seq):
  def __init__(self,seq,sndnm):
    super().__init__(seq.data)
    self.sndnm=sndnm

  def __str__(self):
    return '[%s|%s]'%(self.sndnm,self.data)


''' sequence of (possibly different) sound sequences (Sndseq), a Heterogeneous Pattern '''
class Ptn:
  def __init__(self,sndsqlst):
    self.data=sndsqlst
    self.length=len(self.data)
    self.seqlen=self.data[0].seqlen

  def __str__(self):
    fmts=''
    for sq in self.data:
      fmts=fmts+str(sq)+' '
    return fmts

  def getframe(self,frame):
    ptn=self.data[(frame//self.seqlen)%self.length]
    evt=ptn.getevt(frame)
    return evt,ptn.sndnm


''' a loop, made up of layers of HPtns '''
class Loop:
  def __init__(self,ptnlyrs):
    self.layers=ptnlyrs

  def __str__(self):
    fmts='[loop]\n'
    for i,lyr in enumerate(self.layers):
      fmts+='layer_%02d=%s\n'%(i,str(lyr))
    fmts+='[end]'
    return fmts

  def playframe(self,frameptr,inst,volmap,coeff):
    for lptn in self.layers:
      ctlsig,sndnm=lptn.getframe(frameptr)
      ivol=volmap[sndnm] if sndnm in volmap else 127
      snvlst=inst.getmidiinfo(sndnm,int(ivol*coeff))
      if ctlsig=='1':
        for snv in snvlst:
          status,note,velo=snv
          inst.midion(status,note,velo)
      elif ctlsig=='0':
        for snv in snvlst:
          status,note,velo=snv
          inst.midioff(status,note,velo)

  def getduration(self):
    mxlen=0
    for lyr in self.layers:
      actdur=lyr.length*lyr.seqlen
      if actdur>mxlen:
        mxlen=actdur
    return mxlen


''' a (jam) tra(q|ck), made up of layers of loops running in parallel '''
class Traq:
  def __init__(self,loopset):
    self.loops=loopset
    self.tapehead=0
    self.activector=[True for i in loopset]
    self.subdivs=8.0
    self.duration=self.getmeasure()
    
  def playframe(self,frameptr,delay,inst,volmap,coeff):
    for i,loop in enumerate(self.loops):
      if self.activector[i]:
        loop.playframe(frameptr,inst,volmap,coeff)
    time.sleep(delay/self.subdivs)

  def getmeasure(self):
    mxlen=0
    for lp in self.loops:
      lpdur=lp.getduration()
      if lpdur>mxlen:
        mxlen=lpdur
    return mxlen

  def __str__(self):
    fmts='activector=%s\n'%str(self.activector)
    fmts+='tgap=%.4f\n'%self.tgap
    fmts+='bpm=%.2f\n'%self.bpm
    fmts+='[traq]\n'
    for i,loop in enumerate(self.loops):
      fmts+='loop_%02d=%s\n'%(i,str(loop))
    fmts+='[end]'
    return fmts


''' the midi arrangement abstraction '''
class MidArr:
  def __init__(self,arrf):
    self.sstak=[]
    self.symtab={}
    self.seqtab={}
    self.ptntab={}
    self.looptab={}
    self.traqtab={}
    self.padmap={}
    self.voltab={}
    self.tapectr=0
    self.paused=False
    self.parsearr(arrf)
    self.actvtrknm=self.symtab['activetrack']
    self.actvtrkvelo=80
    self.tgap=60.0/float(self.symtab['bpm'])

  def __str__(self):
    fmts='[traqtab]\n'
    for k,v in self.traqtab.items():
      fmts+='%s=%s\n'%(k,str(v))
    fmts+='[end]'
    return fmts

  def procsect(self,ln):
    sectnm=ln[1:-1]
    if sectnm=='end' and len(self.sstak)==0:
      raise Exception('[parse_error] illegal end when stack is empty!')
    if sectnm=='end' and len(self.sstak)>0:
      currsect=self.sstak.pop()
    if sectnm!='end':
      self.sstak.append(sectnm)

  def parseptn(self,lr):
    sqlst=[]
    for hsq in lr[1].split(','):
      if '/' in hsq:
        sqnm,sndnm=hsq.split('/')
        sqlst.append(Sndseq(self.seqtab[sqnm],sndnm))
      elif hsq in self.ptntab:
        for sndsq in self.ptntab[hsq].data:
          sqlst.append(sndsq)
      else:
        raise Exception('boom! unknown pattern %s encountered in rhs!'%hsq)
    self.ptntab[lr[0]]=Ptn(sqlst)

  def getlns(self,farr):
    with open(farr) as fa:
      arrlns=fa.readlines()
    arrlns=[ln.strip() for ln in arrlns]
    return arrlns

  def parsearr(self,farr):
    print('parsing arrangement file: %s'%farr)
    for ln in self.getlns(farr):
      if len(ln)==0 or ln.startswith('#'):
        continue
      if ln.startswith('[') and ln.endswith(']'):
        self.procsect(ln)
      else:
        lr=ln.split('=')
        if self.sstak[-1]=='global':
          self.symtab[lr[0]]=lr[1]
        elif self.sstak[-1]=='seq':
          self.seqtab[lr[0]]=Seq(lr[1])
        elif self.sstak[-1]=='ptn':
          self.parseptn(lr)
        elif self.sstak[-1]=='loop':
          self.looptab[lr[0]]=Loop([self.ptntab[ptnm] for ptnm in lr[1].split(',')])
        elif self.sstak[-1]=='traq':
          self.traqtab[lr[0]]=Traq([self.looptab[lpnm] for lpnm in lr[1].split(',')])
        elif self.sstak[-1]=='padmap':
          self.padmap[lr[0]]=lr[1]
        elif self.sstak[-1]=='vol':
          self.voltab[lr[0]]=int(lr[1])

  def play(self,krome):
    print('active traq: %s, duration: %d'%(self.actvtrknm,self.traqtab[self.actvtrknm].duration))
    while not self.paused:
      if self.actvtrknm not in self.traqtab:
        continue
      actrk=self.traqtab[self.actvtrknm]
      actrk.playframe(self.tapectr,self.tgap,krome,self.voltab,self.actvtrkvelo/127.0)
      self.tapectr=(self.tapectr+1)%actrk.duration


if __name__=='__main__':
  if len(sys.argv)!=2:
    print('[usage] ./midiarr.py <song>.arr')
    raise SystemExit

  mar=MidArr(sys.argv[1])
  print(str(mar))

