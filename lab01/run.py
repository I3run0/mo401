import logging as lgg
from parsers.parsers import funit_parser, code_parser, OPCODES

#lgg.basicConfig(level=lgg.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

units = funit_parser("exemaples/example.txt")
instructions = code_parser("exemaples/example.s")
#lgg.info(units, instruction)

#create function table

#indices to unit status table
UNT_TYPE = 0 
AV = 1
RD = 2
F1 = 3
F2 = 4
Q1 = 5
Q2 = 6
R1 = 7
R2 = 8
CLS = 9

#Tuple list that indicates the range of it unit type
funits_states = []
tbl_sz = 0

for ukey in units:
    init_tbl_sz = tbl_sz
    for j in range(units[ukey]['qtt']):
        funits_states.append([None] * 10)
        funits_states[tbl_sz][UNT_TYPE] = ukey
        funits_states[tbl_sz][CLS] = units[ukey]['cls']
        tbl_sz += 1   
    units[ukey]['range'] = [init_tbl_sz, init_tbl_sz ,tbl_sz]
    units[ukey]['avaible'] = True


#extend the intructions dictionary
UNISSU = 0
ISSUED = 1
READ = 2
EXECUTED = 3
WRITED = 4
DONE = 5

for instruc in instructions:
    instruc["status"] = UNISSU
    instruc["unit_addr"] = None

init_queue = instructions
processing_queue = [[], [], [], []]
end_queue = []


#reg

INT_REG = dict.fromkeys(['r' + str(i) for i in range(1, 33)])
FLOAT_REG = dict.fromkeys(['f' + str(i) for i in range(1, 33)])
X_REG = dict.fromkeys(['x' + str(i) for i in range(1, 33)])
REG = {'r': INT_REG, 'f': FLOAT_REG, 'x':X_REG}


def issue(instruc) -> bool:
    #check reg table
    if not (instruc['opcode'] == OPCODES['fsd']) and\
          REG[instruc['rd'][:1]][instruc['rd']]:
        return False
    
    if not units[instruc['unit']]['avaible']:
        return False

    #change tbl
    tbl_pos = units[instruc['unit']]['range'][1]
    funits_states[tbl_pos][AV] = False
    
    if not (instruc['opcode'] == OPCODES['fsd']):
        funits_states[tbl_pos][RD] = instruc['rd']
        REG[instruc['rd'][:1]][instruc['rd']] = funits_states[tbl_pos][UNT_TYPE]

    funits_states[tbl_pos][F1] = instruc["rs1"]
    unit_from_reg_src = REG[instruc['rs1'][:1]][instruc['rs1']]
    funits_states[tbl_pos][Q1] = unit_from_reg_src 
    funits_states[tbl_pos][R1] =  False if unit_from_reg_src else True

    if not(instruc['opcode'] == OPCODES['fld']):
        funits_states[tbl_pos][F2] = instruc["rs2"]
        unit_from_reg_src = REG[instruc['rs2'][:1]][instruc['rs2']]
        funits_states[tbl_pos][Q2] = unit_from_reg_src 
        funits_states[tbl_pos][R2] =  False if unit_from_reg_src else True
    
    units[instruc['unit']]['range'][1] += 1
    if units[instruc['unit']]['range'][1] == units[instruc['unit']]['range'][2]:
        units[instruc['unit']]['avaible'] = False

    instruc["status"] = ISSUED
    instruc["unit_addr"] = tbl_pos
    return True

def read(instruc):
    tbl_pos = instruc["unit_addr"]
    ri_is_av = not(REG[instruc['rs1'][:1]][instruc['rs1']])
    rj_is_av = not(instruc['opcode'] == OPCODES['fld']) and\
          REG[instruc['rs2'][:1]][instruc['rs2']]
    
    #Register src 1 is not used by a unit
    if ri_is_av:
        funits_states[tbl_pos][Q1] = None
        funits_states[tbl_pos][R1] = None
 
    #Register src 2 is not used by a unit
    if rj_is_av:
            funits_states[tbl_pos][Q1] = None
            funits_states[tbl_pos][R1] = None
    
    if rj_is_av and ri_is_av:
        instruc["status"] = READ

def execute(instruc):
    tbl_pos = instruc["unit_addr"]
    funits_states[tbl_pos][CLS] -= 1
    if funits_states[tbl_pos][CLS] == 0:
        if not(instruc['opcode'] == OPCODES['fsd']):
            REG[instruc['rd'][:1]][instruc['rd']] = None
        
        un_type = funits_states[tbl_pos][UNT_TYPE] 
        funits_states[tbl_pos][CLS] = units[un_type]['range'][0]
        funits_states[tbl_pos][Q1] = None
        funits_states[tbl_pos][Q2] = None
        funits_states[tbl_pos][R1] = None
        funits_states[tbl_pos][R2] = None
        funits_states[tbl_pos][F1] = None
        funits_states[tbl_pos][F2] = None
        funits_states[tbl_pos][RD] = None
        funits_states[tbl_pos][AV] = True

        instruc["status"] = WRITED

#para lançar a issue verificar se alguém está escrevendo no registrador

'''
def issue_func(insruc):
    if check_table(instruc)

while init_queue:
    issue_func()

ex_cls = 1
while init_queue == [] and processing_queue = []:

    #ISSUE 
    ind_to_move = []
    for ind in range(len(processing_queue[0])):
        execute(processing_queue[0][ind])
        if processing_queue[0][ind]["status"] == READ:
            ind_to_move.append(ind)

    while ind_to_move != []:
        end_queue.append(processing_queue[3].pop(ind_to_move.pop(0)))
    
    #READ 
    ind_to_move = []
    for ind in range(len(processing_queue[2])):
        execute(processing_queue[2][ind])
        if processing_queue[2][ind]["status"] == READ:
            ind_to_move.append(ind)
    
    while ind_to_move != []:
        end_queue.append(processing_queue[3].pop(ind_to_move.pop(0)))

    #execute the ex_cls
    ind_to_move = []
    for ind in range(len(processing_queue[3])):
        execute(processing_queue[3][ind])
        if processing_queue[3][ind]["status"] == WRITED:
            ind_to_move.append(ind)
    
    while ind_to_move != []:
        end_queue.append(processing_queue[3].pop(ind_to_move.pop(0)))
    
    if issue_func(init_queue[0]):
        processing_queue.append(init_queue.pop(0)) # [a1, a2, a3] <- [a6, A5] | [a1, a2, a3, a6] <- [A5]

    
''' 
#print(issue(instructions[4]))
#execute(instructions[4])

#'''
cls = 1
while init_queue != [] and cls < 20:    
    
    
    #READ 
    ind_to_move = []
    for ind in range(len(processing_queue[0])):
        read(processing_queue[0][ind])
        if processing_queue[0][ind]["status"] == READ:
            ind_to_move.append(ind)
    
    while ind_to_move != []:
        processing_queue[1].append(processing_queue[0].pop(ind_to_move.pop(0)))
    
    if issue(init_queue[0]):
        processing_queue[0].append(init_queue.pop(0))

    print(cls)
    print(processing_queue[0])
    print(init_queue)
    print(len(processing_queue))
    print()
    cls += 1
#'''

    

