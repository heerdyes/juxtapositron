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
bp00/bd=bd00,bd00
bh00/hh=hh00,hh01
sp00/sn=sn00,sn01

bp01/bd=bd00,bd01
sp01/sn=sn01,sn01
hp01/hh=hh02,hh02

fl00/sn=rl00,rl01
fl01/cy=rd00,rd01
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

