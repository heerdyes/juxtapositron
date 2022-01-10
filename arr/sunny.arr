[global]
bpm=120
bardur=16
activetrack=t00
[end]

[vol]
D5=100
bD2=90
bF2=90
bBb2=90
bE2=90
bA2=90
bC2=90
F7=100
BbM7=100
G5E=100
A7=100
[end]

[seq]
# drum sequences
drkk00=10..10..
drsn00=10......
drkk01=....10..

# bass sequences
bs00=10..10..........
bs01=10....10........
bs02=..10..10..10....
rest=................

# el piano sequences
ep00=10......10......
ep01=1.0.....10..10..
ep03=1...0.........10
ep02=1..0....1..0....
ch00=..10....10......
ch01=10....1010......
ch02=10....10........
[end]

[ptn]
# drum patterns
drumintro00=drkk00/bd,drsn00/sn,drkk01/bd,drsn00/sn

# bass patterns
bsd200=bs00/bD2,bs01/bD2
versebs00=bs00/bD2,bs01/bD2,bs00/bF2,bs01/bF2,bs00/bBb2,bs01/bBb2,bs00/bE2,bs00/bA2
versebs01=bs00/bD2,bs01/bD2,bs00/bF2,bs01/bF2,bs00/bBb2,bs01/bBb2,bs00/bEb2,bs00/bEb2
versebs02=bs01/bE2,bs01/bE2,bs00/bA2,bs00/bA2,bs00/bD2,bs00/bD2,bs00/bA2,bs00/bC2
versebs=versebs00,versebs00,versebs01,versebs02
improvbs=bs00/bD2,rest/bD2,bs02/bD2,rest/bD2

# el piano patterns
verseep00=ep00/D5,rest/D5,ep00/F7,rest/F7,ep00/BbM7,rest/BbM7,ep02/G5E,ep02/A7
verseep01=ep01/D5,rest/D5,ep03/F7,rest/F7,ep01/BbM7,rest/BbM7,ep02/G5Eb,rest/G5Eb
verseep02=ep02/G5E,rest/G5E,ep02/A7,rest/A7,ep03/D5,rest/D5,ep02/A7,rest/A7
verseep=verseep00,verseep00,verseep01,verseep02
improvep=ep00/D5,rest/D5,ep02/D5,rest/D5
[end]

[loop]
dl00=drumintro00
bD200=bsd200
verseloop=versebs,verseep
improvloop=improvbs,improvep
[end]

[traq]
t00=dl00,bD200
t01=dl00,verseloop
t02=dl00,improvloop
[end]

[padmap]
pad1=t00
pad2=t01
pad3=t02
pad4=na
[end]

