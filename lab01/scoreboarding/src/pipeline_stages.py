from src.parsers import *

_UNT_TYPE = 0 
_AV = 1
_RD = 2
_F1 = 3
_F2 = 4
_Q1 = 5
_Q2 = 6
_R1 = 7
_R2 = 8
_CLS = 9
_INIT_CLC = 10
_INSTUC_READ = 11

_INT_REG = dict.fromkeys(['r' + str(i) for i in range(0, 32)])
_FLOAT_REG = dict.fromkeys(['f' + str(i) for i in range(0, 32)])
_X_REG = dict.fromkeys(['x' + str(i) for i in range(0, 32)])
_REG = {'r': _INT_REG, 'f': _FLOAT_REG, 'x':_X_REG}

_ISSUED = "ISSUE"
_READ = "READ"
_EXECUTION = "EXECUTE"
_WRITE = "WRITE"

_FUNIT_INF = {}
_FUNITS_STATUS_TBL = []

def init_funit_status_table(funits: dict):
    global _FUNIT_INF
    _FUNIT_INF = funits.copy()
    tbl_ind = 0
    for ukey in _FUNIT_INF:
        _FUNIT_INF[ukey]['unt_avaibles'] = []
        for j in range(_FUNIT_INF[ukey]['qtt']):
            _FUNITS_STATUS_TBL.append([None] * 12)
            _FUNITS_STATUS_TBL[tbl_ind][_UNT_TYPE] = ukey
            _FUNITS_STATUS_TBL[tbl_ind][_CLS] = _FUNIT_INF[ukey]['cls']
            _FUNITS_STATUS_TBL[tbl_ind][_INIT_CLC] = -1
            _FUNITS_STATUS_TBL[tbl_ind][_INSTUC_READ] = False
            _FUNIT_INF[ukey]['unt_avaibles'].append(tbl_ind)
            tbl_ind += 1

def issue(instruc, clc) -> bool:
    #check reg table
    if not (instruc['opcode'] == OPCODES['fsd']) and\
          _REG[instruc['rd'][:1]][instruc['rd']] != None:
        return False

    if _FUNIT_INF[instruc['unit']]['unt_avaibles'] == []:
        return False

    tbl_pos = _FUNIT_INF[instruc['unit']]['unt_avaibles'].pop(0)
    _FUNITS_STATUS_TBL[tbl_pos][_AV] = False
    _FUNITS_STATUS_TBL[tbl_pos][_INSTUC_READ] = False
    _FUNITS_STATUS_TBL[tbl_pos][_INIT_CLC] = clc

    _FUNITS_STATUS_TBL[tbl_pos][_F1] = instruc["rs1"]
    unit_from_reg_src = _REG[instruc['rs1'][:1]][instruc['rs1']]
    _FUNITS_STATUS_TBL[tbl_pos][_Q1] = unit_from_reg_src 
    _FUNITS_STATUS_TBL[tbl_pos][_R1] =  True if unit_from_reg_src == None else False

    if not(instruc['opcode'] == OPCODES['fld']):
        _FUNITS_STATUS_TBL[tbl_pos][_F2] = instruc["rs2"]
        unit_from_reg_src = _REG[instruc['rs2'][:1]][instruc['rs2']]
        _FUNITS_STATUS_TBL[tbl_pos][_Q2] = unit_from_reg_src 
        _FUNITS_STATUS_TBL[tbl_pos][_R2] =  True if unit_from_reg_src == None else False

    if not(instruc['opcode'] == OPCODES['fsd']):
        _FUNITS_STATUS_TBL[tbl_pos][_RD] = instruc['rd']
        _REG[instruc['rd'][:1]][instruc['rd']] = tbl_pos

    instruc["status"] = _ISSUED
    instruc["unit_addr"] = tbl_pos
    return True

def read(instruc) -> bool:
    tbl_pos = instruc["unit_addr"]
    ri_is_av, rj_is_av = False, False
    ri_is_av = _FUNITS_STATUS_TBL[tbl_pos][_Q1] == None or\
          _REG[instruc['rs1'][:1]][instruc['rs1']] != _FUNITS_STATUS_TBL[tbl_pos][_Q1]

    rj_is_av = _FUNITS_STATUS_TBL[tbl_pos][_Q2] == None or\
        instruc['opcode'] == OPCODES['fld'] or\
          _REG[instruc['rs2'][:1]][instruc['rs2']] != _FUNITS_STATUS_TBL[tbl_pos][_Q2]    

    if ri_is_av:
        _FUNITS_STATUS_TBL[tbl_pos][_Q1] = None
        _FUNITS_STATUS_TBL[tbl_pos][_R1] = False
 
    #Register src 2 is not used by a unit
    if rj_is_av:
            _FUNITS_STATUS_TBL[tbl_pos][_Q2] = None
            _FUNITS_STATUS_TBL[tbl_pos][_R2] = False


    if rj_is_av and ri_is_av:
        instruc["status"] = _READ
        return True

    return False

def execute(instruc) -> bool:
    tbl_pos = instruc["unit_addr"]
    _FUNITS_STATUS_TBL[tbl_pos][_CLS] -= 1
    instruc["status"] = _EXECUTION
    _FUNITS_STATUS_TBL[tbl_pos][_INSTUC_READ] = True

    if _FUNITS_STATUS_TBL[tbl_pos][_CLS] == 0:
        return True

    return False

def write(instruc) -> bool:
    can_write = True
    tbl_pos = instruc["unit_addr"]

    for i in range(len(_FUNITS_STATUS_TBL)):
        if tbl_pos == i or\
              _FUNITS_STATUS_TBL[tbl_pos][_INIT_CLC] < -1 or\
              _FUNITS_STATUS_TBL[tbl_pos][_INIT_CLC] < _FUNITS_STATUS_TBL[i][_INIT_CLC]:
            continue

        if _FUNITS_STATUS_TBL[i][_AV] == False and\
            (_FUNITS_STATUS_TBL[i][_F1] == instruc['rd'] or\
            _FUNITS_STATUS_TBL[i][_F2] == instruc['rd']) and\
                not(_FUNITS_STATUS_TBL[i][_INSTUC_READ]):
            can_write = False

    if can_write:
        if not(instruc['opcode'] == OPCODES['fsd']):
            _REG[instruc['rd'][:1]][instruc['rd']] = None
        
        un_type = _FUNITS_STATUS_TBL[tbl_pos][_UNT_TYPE] 
        _FUNITS_STATUS_TBL[tbl_pos][_CLS] = _FUNIT_INF[un_type]['cls']
        _FUNITS_STATUS_TBL[tbl_pos][_Q1] = None
        _FUNITS_STATUS_TBL[tbl_pos][_Q2] = None
        _FUNITS_STATUS_TBL[tbl_pos][_R1] = None
        _FUNITS_STATUS_TBL[tbl_pos][_R2] = None
        _FUNITS_STATUS_TBL[tbl_pos][_F1] = None
        _FUNITS_STATUS_TBL[tbl_pos][_F2] = None
        _FUNITS_STATUS_TBL[tbl_pos][_RD] = None
        _FUNITS_STATUS_TBL[tbl_pos][_AV] = True
        _FUNIT_INF[un_type]['unt_avaibles'].append(tbl_pos)
        _FUNITS_STATUS_TBL[tbl_pos][_INSTUC_READ] = False
        _FUNITS_STATUS_TBL[tbl_pos][_INIT_CLC] = -1
        instruc["status"] = _WRITE

    return can_write