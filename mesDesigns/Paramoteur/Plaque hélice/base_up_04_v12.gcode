(Exported by FreeCAD)
(Post Processor: grbl_post)
(Output Time:2022-06-05 10:56:08.114395)
(Begin preamble)
G17 G90
G21
(Begin operation: TC: 12.7 V90deg Q8)
(Path: TC: 12.7 V90deg Q8)
(TC: 12.7 V90deg Q8)
(Begin toolchange)
( M6 T13.0 )
M3 S10000.0
(Finish operation: TC: 12.7 V90deg Q8)
(Begin operation: Fixture)
(Path: Fixture)
G54
G0 Z25.000
(Finish operation: Fixture)
(Begin operation: Deburr)
(Path: Deburr)
(Deburr)
G0 Z25.000
G0 X53.500 Y40.000
G0 Z23.000
G1 X53.500 Y40.000 Z18.500 F100.002
G2 X53.500 Y40.000 Z18.500 I-13.500 J0.000 K0.000 F400.002
G0 Z25.000
G0 Z25.000
G0 X78.500 Y40.000
G0 Z23.000
G1 X78.500 Y40.000 Z8.500 F100.002
G2 X78.500 Y40.000 Z8.500 I-38.500 J-0.000 K0.000 F400.002
G0 Z25.000
G0 Z25.000
G0 X43.250 Y40.000
G0 Z23.000
G1 X43.250 Y40.000 Z18.500 F100.002
G2 X43.250 Y40.000 Z18.500 I-3.250 J0.000 K0.000 F400.002
G0 Z25.000
G0 Z25.000
(Finish operation: Deburr)
(Begin postamble)
M5
G17 G90
M2
