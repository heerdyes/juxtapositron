[global]
bpm=90
bardur=16
activetrack=t00
[end]

[seq]
bd00=10..............
hh00=10..10..10..10..
sn00=........10......

bd01=10..10..........
hh01=10..10..10..1010
sn01=........10....10

hh02=....10......1010
rl00=..10....10....10
rl01=..10....10101010
rd01=10....10........
rd00=10..............
[end]

[ptn]
bp00=bd00/bd,bd00/bd
bh00=hh00/hh,hh01/hh
sp00=sn00/sn,sn01/sn

bp01=bd00/bd,bd01/bd
sp01=sn01/sn,sn01/sn
hp01=hh02/hh,hh02/hh

fl00=rl00/sn,rl01/sn
fl01=rd00/cy,rd01/cy
[end]

[loop]
dl00=bp00,bh00,sp00
dl01=bp01,sp01
dl02=bp01,sp01,hp01
ff00=hp01,fl00,fl01
[end]

[traq]
t00=dl00
t01=dl01
t02=dl02
t03=ff00
[end]

[padmap]
pad1=t00
pad2=t01
pad3=t02
pad4=t03
pad5=na
[end]

