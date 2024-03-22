import logging as lgg
from parsers.parsers import funit_parser, code_parser, OPCODES

#lgg.basicConfig(level=lgg.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

units = funit_parser("exemaples/example.txt")
instructions = code_parser("exemaples/example.s")
print(units)
#lgg.info(units, instruction)

#create function table

#indices to unit status table
UNT_TYPE = 0 
AV = 1
RD = 2
F1 = 3
F2 = 4
Q1 = 6
Q2 = 7
R1 = 8
R2 = 9
CLS = 10

#Tuple list that indicates the range of it unit type
funits_states = []
tbl_sz = 0

for ukey in units:
    init_tbl_sz = tbl_sz
    for j in range(units[ukey]['qtt']):
        funits_states.append([None] * 11)
        funits_states[tbl_sz][UNT_TYPE] = ukey
        funits_states[tbl_sz][CLS] = units[ukey]['cls']
        tbl_sz += 1   
    units[ukey]['range'] = (init_tbl_sz, init_tbl_sz ,tbl_sz)
    units[ukey]['avaible'] = True


#extend the intructions dictionary
unissue = 0
issue = 1
read = 2
execute = 3
write = 4
done = 5

for instruc in instructions:
    instruc["status"] = unissue

init_queue = instructions
processing_queue = []
end_queue = []

#reg

INT_REG = dict.fromkeys(['r' + str(i) for i in range(1, 33)])
FLOAT_REG = dict.fromkeys(['f' + str(i) for i in range(1, 33)])
X_REG = dict.fromkeys(['x' + str(i) for i in range(1, 33)])
REG = {'r': INT_REG, 'f': FLOAT_REG, 'x':X_REG}


def issue_func(instruc) -> bool:
    #check reg table
    print(REG[instruc['rd'][:1]][instruc['rd']])
    if REG[instruc['rd'][:1]][instruc['rd']]:
        return False
    
    print(instruc['unit'], units[instruc['unit']]['avaible'])
    if not units[instruc['unit']]['avaible']:
        return False

    #change tbl
    tbl_pos = units[instruc['unit']]['range'][1]
    funits_states[tbl_pos][AV] = False
    
    if not (instruc['opcode'] == OPCODES['fsd']):
        funits_states[tbl_pos][RD] = instruc['rd']
        REG[instruc['rd'][:1]][instruc['rd']] = funits_states[tbl_pos][UNT_TYPE]
    
    funits_states[tbl_pos][RD]

#para lançar a issue verificar se alguém está escrevendo no registrador


'''
def issue_func(insruc):
    if check_table(instruc)

while init_queue:
    issue_func()

'''
print(units)

print("\n\n\n\n\n")
issue_func(instructions[0])