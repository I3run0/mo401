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
tbl_ind = 0
for ukey in units:
    units[ukey]['unt_avaibles'] = []
    for j in range(units[ukey]['qtt']):
        funits_states.append([None] * 10)
        funits_states[tbl_ind][UNT_TYPE] = ukey
        funits_states[tbl_ind][CLS] = units[ukey]['cls']
        units[ukey]['unt_avaibles'].append(tbl_ind)
        tbl_ind += 1



#extend the intructions dictionary
UNISSU = 0
ISSUED = "ISSUE"
READ = "READ"
EXECUTION = "EXECUTE"
WRITE = "WRITE"

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
        print("chegou aqui")
        return False
    
    print("units")
    print(units[instruc['unit']]['unt_avaibles'])
    if units[instruc['unit']]['unt_avaibles'] == []:
        return False

    #change tbl
    tbl_pos = units[instruc['unit']]['unt_avaibles'].pop(0)
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

    instruc["status"] = ISSUED
    instruc["unit_addr"] = tbl_pos
    return True

def read(instruc) -> bool:
    tbl_pos = instruc["unit_addr"]
    #print(funits_states[tbl_pos])
    ri_is_av = not(REG[instruc['rs1'][:1]][instruc['rs1']])
    rj_is_av = True if instruc['opcode'] == OPCODES['fld'] \
        else True if not(REG[instruc['rs2'][:1]][instruc['rs2']]) else False
    
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
        return True

    return False

def execute(instruc) -> bool:
    tbl_pos = instruc["unit_addr"]
    funits_states[tbl_pos][CLS] -= 1
    if instruc["status"] != EXECUTION:
        instruc["status"] = EXECUTION

    if funits_states[tbl_pos][CLS] == 0:
        return True

    return False


def write(instruc) -> bool:
    tbl_pos = instruc["unit_addr"]
    if not(instruc['opcode'] == OPCODES['fsd']):
        REG[instruc['rd'][:1]][instruc['rd']] = None
    
    un_type = funits_states[tbl_pos][UNT_TYPE] 
    funits_states[tbl_pos][CLS] = units[un_type]['cls']
    funits_states[tbl_pos][Q1] = None
    funits_states[tbl_pos][Q2] = None
    funits_states[tbl_pos][R1] = None
    funits_states[tbl_pos][R2] = None
    funits_states[tbl_pos][F1] = None
    funits_states[tbl_pos][F2] = None
    funits_states[tbl_pos][RD] = None
    funits_states[tbl_pos][AV] = True
    units[un_type]['unt_avaibles'].append(tbl_pos) 
    instruc["status"] = WRITE
    return True

#printers key is a instruc and the value is its status
#
table_printer = {}
#'''

def update_create_a_iten(instruc, cls):
    if not(instruc):
        return
    
    key = ""
    if instruc['opcode'] == OPCODES['fld']:
        key = f'{instruc["op"]} {instruc["rd"]} {instruc["imm"]}({instruc["rs1"]})'

    elif instruc["opcode"] == OPCODES["fsd"]:
        key = f'{instruc["op"]} {instruc["rs1"]} {instruc["imm"]}({instruc["rs2"]})'
    
    else:
        key = f'{instruc["op"]} {instruc["rd"]} {instruc["rs1"]} {instruc["rs2"]}'
    
    if not(key in table_printer.keys()):
        table_printer[key] = {
            "ISSUE": 0,
            "READ": 0,
            "EXECUTE": 0,
            "WRITE": 0,
        }

    if instruc["status"] in table_printer[key].keys():
        table_printer[key][instruc["status"]] = cls
    else:
        print(instruc["status"])

def update_create_a_list(indices ,instrucs, cls):
    for ind in indices:
        update_create_a_iten(instrucs[ind], cls)

#'''
cls = 1

while cls < 26:
    print(cls)
    instruc_to_issue = None

    if init_queue != [] and issue(init_queue[0]):
        instruc_to_issue = init_queue.pop(0) 

    issue_to_move = []
    for ind in range(len(processing_queue[0])):
        read(processing_queue[0][ind])
        if processing_queue[0][ind]["status"] == READ:
            issue_to_move.append(ind)

    exec_to_move = []
    for ind in range(len(processing_queue[1])):
        if execute(processing_queue[1][ind]):
            exec_to_move.append(ind)
    
    write_to_move = []
    for ind in range(len(processing_queue[2])):
        if write(processing_queue[2][ind]):
            write_to_move.append(ind)

    update_create_a_iten(instruc_to_issue, cls)
    update_create_a_list(issue_to_move, processing_queue[0], cls)
    update_create_a_list(exec_to_move, processing_queue[1], cls)
    update_create_a_list(write_to_move, processing_queue[2], cls)

    print(table_printer)
    #print(instructions)
    print(issue_to_move)
    if instruc_to_issue:
        processing_queue[0].append(instruc_to_issue)

    while issue_to_move != []:
        processing_queue[1].append(processing_queue[0].pop(issue_to_move.pop(0)))

    while exec_to_move != []:
        processing_queue[2].append(processing_queue[1].pop(exec_to_move.pop(0)))

    while write_to_move != []:
        end_queue.append(processing_queue[2].pop(write_to_move.pop(0)))

    cls += 1
    print(processing_queue[0] != [] or processing_queue[1] != [] or processing_queue[2] != [])
    

