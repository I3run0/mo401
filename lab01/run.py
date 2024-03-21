import logging as lgg
from parsers.code_parser import code_parser
from parsers.unit_parser import funit_parser

#lgg.basicConfig(level=lgg.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

units = funit_parser("exemaples/example.txt")
instrs = code_parser("exemaples/example.s")
#lgg.info(units, instrs)

#create function table

#indices to unit status table
UNT_TYPE = 0 
AV = 1
D1 = 2
R1 = 3
R3 = 4
Q1 = 6
Q2 = 7
R1 = 8
R2 = 9
cls = 10

#Tuple list that indicates the range of it unit type
funits_states = []
tbl_sz = 0
for i in range(len(units)):
    init_tbl_sz = tbl_sz
    for j in range(units[i]['qtt']):
        funits_states.append([None] * 11)
        funits_states[tbl_sz][UNT_TYPE] = units[i]["type"]
        funits_states[tbl_sz][cls] = units[i]['cls']
        tbl_sz += 1   
    units[i]['range'] = (init_tbl_sz, tbl_sz)
print(funits_states, units)
