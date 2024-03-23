# Define opcode constants
OPCODES = {
    'fld': 0,
    'fsd': 1,
    'fadd': 2,
    'fsub': 3,
    'fmul': 4,
    'fdiv': 5
}

# Define register prefix constants
REG_PREFIXES = {
    'x': 'int',
    'f': 'float',
    'r': 'int'
}

# Define fucntion units type constants
FUNITS = ['int', 'mult', 'add', 'div']

def code_parser(filename):
    instructions = []
    with open(filename, 'r') as f:
        for line in f:
            fields = line.lower().strip().replace(',', ' ').split()
            opcode = fields[0]
            if opcode not in OPCODES:
                raise ValueError(f'Invalid opcode: {opcode}')
            opcode = OPCODES[opcode]
            rs1, rs2, rd, imm = None, None, None, None  # Set imm to None by default
            unit, rs1_type, rs2_type, rd_type = None, None, None, None
            if opcode == 0:  # fld format: "instruction rd imm(rs1)"
                rd = fields[1]
                rd_type = REG_PREFIXES[fields[1][0].lower()]
                rs1_imm = fields[2].split('(')
                imm = int(rs1_imm[0])
                rs1 = rs1_imm[1][:-1]
                unit = FUNITS[0]
                rs1_type = REG_PREFIXES[rs1_imm[1][0:1].lower()]
            elif opcode == 1:  # fsd format: "instruction rs2 imm(rs1)"
                rs2 = fields[1]
                rs2_type = REG_PREFIXES[fields[1][0].lower()]
                rs1_imm = fields[2].split('(')
                imm = int(rs1_imm[0])
                rs1 = rs1_imm[1][:-1]
                unit = FUNITS[0]
                rs1_type = REG_PREFIXES[rs1_imm[1][0:1].lower()]
            else:  # Other instructions format: "instruction rd rs1 rs2"
                rd = fields[1]
                rd_type = REG_PREFIXES[fields[1][0].lower()]
                rs1 = fields[2]
                rs1_type = REG_PREFIXES[fields[2][0].lower()]
                if len(fields) > 3:
                    rs2 = fields[3]
                    rs2_type = REG_PREFIXES[fields[3][0].lower()]
                else:
                    rs2 = 0
                    rs2_type = None       
                if opcode == 2 or opcode == 3:
                    unit = FUNITS[2] #ADD
                elif opcode == 4:
                    unit = FUNITS[1] #MULT
                else:
                    unit = FUNITS[3] #DIV
            instructions.append({
                'opcode': opcode,
                'op': fields[0],
                'rs1': rs1,
                'rs1_type': rs1_type,
                'rs2': rs2,
                'rs2_type': rs2_type,
                'rd': rd,
                'rd_type': rd_type,
                'imm': imm,
                'unit': unit,
                'status': None,
                'unit_addr': None,
            })
    return instructions

#print(code_parser("../exemaples/example.s"))

def funit_parser(filename):
    funits = {}
    with open(filename, 'r') as f:
        for line in f:
            fields = line.lower().replace(',', ' ').split()
            funit = fields[0]
            if funit not in FUNITS:
                raise ValueError(f'Invalid function unit: {funit}')
            funits[funit] = {
                'qtt': int(fields[1]),
                'cls': int(fields[2])
            }

    
    return funits