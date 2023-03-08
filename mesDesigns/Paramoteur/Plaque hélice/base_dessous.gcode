(Exported by FreeCAD)
(Post Processor: grbl_post)
(Output Time:2022-06-12 22:35:00.909751)
(Begin preamble)
G17 G90
G21
(Begin operation: Fixture)
(Path: Fixture)
G54
G0 Z25.000
(Finish operation: Fixture)
(Begin operation: TC: 12.7 V90deg Q009)
(Path: TC: 12.7 V90deg Q009)
(TC: 12.7 V90deg Q009)
(Begin toolchange)
( M6 T13.0 )
M3 S10000.0
(Finish operation: TC: 12.7 V90deg Q009)
(Begin operation: Deburr001)
(Path: Deburr001)
(Deburr001)
G0 Z25.000
G0 X76.000 Y37.445
G0 Z23.000
G1 X76.000 Y37.445 Z18.500 F100.002
G2 X76.000 Y37.445 Z18.500 I-38.500 J-0.000 K0.000 F349.998
G0 Z25.000
G0 Z25.000
G0 X49.050 Y37.445
G0 Z23.000
G1 X49.050 Y37.445 Z18.500 F100.002
G2 X49.050 Y37.445 Z18.500 I-11.550 J0.000 K0.000 F349.998
G0 Z25.000
G0 Z25.000
(Finish operation: Deburr001)
(Begin postamble)
M5
G17 G90
M2
