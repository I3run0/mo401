from parsers import *


units = funit_parser("exemaples/example.txt")
instructions = code_parser("exemaples/example.s")

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

INT_REG = dict.fromkeys(['r' + str(i) for i in range(1, 33)])
FLOAT_REG = dict.fromkeys(['f' + str(i) for i in range(1, 33)])
X_REG = dict.fromkeys(['x' + str(i) for i in range(1, 33)])
REG = {'r': INT_REG, 'f': FLOAT_REG, 'x':X_REG}

UNISSU = 0
ISSUED = "ISSUE"
READ = "READ"
EXECUTION = "EXECUTE"
WRITE = "WRITE"

for instruc in instructions:
    instruc["status"] = UNISSU
    instruc["unit_addr"] = None


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



def issue(instruc) -> bool:
    #check reg table
    if not (instruc['opcode'] == OPCODES['fsd']) and\
          REG[instruc['rd'][:1]][instruc['rd']]:
        print("chegou aqui")
        return False
    
    #print("units")
    #print(units[instruc['unit']]['unt_avaibles'])
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
    ri_is_av, rj_is_av = False, False
    if funits_states[tbl_pos][Q1] == None:
        ri_is_av = True
    else: 
        ri_is_av = not(REG[instruc['rs1'][:1]][instruc['rs1']])
    
    if funits_states[tbl_pos][Q2] == None:
        rj_is_av = True
    else:
        rj_is_av = True if instruc['opcode'] == OPCODES['fld'] \
            else True if not(REG[instruc['rs2'][:1]][instruc['rs2']]) else False

    #Register src 1 is not used by a unit
    if ri_is_av:
        funits_states[tbl_pos][Q1] = None
        funits_states[tbl_pos][R1] = False
 
    #Register src 2 is not used by a unit
    if rj_is_av:
            funits_states[tbl_pos][Q2] = None
            funits_states[tbl_pos][R2] = False
    
    if rj_is_av and ri_is_av:
        instruc["status"] = READ
        return True

    return False

def execute(instruc) -> bool:
    tbl_pos = instruc["unit_addr"]
    funits_states[tbl_pos][CLS] -= 1
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
