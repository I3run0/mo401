from parsers import OPCODES

table_printer = {}
#'''

def update_create_a_iten(instruc, cls):
    if not(instruc):
        return
    
    key = ""
    if instruc['opcode'] == OPCODES['fld']:
        key = f'{instruc["op"]} {instruc["rd"]} {instruc["imm"]}({instruc["rs1"]})'

    elif instruc["opcode"] == OPCODES["fsd"]:
        key = f'{instruc["op"]} {instruc["rs2"]} {instruc["imm"]}({instruc["rs1"]})'
    
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

def update_create_a_list(instrucs, cls):
    for instruc in instrucs:
        update_create_a_iten(instruc, cls)

def print_table():

    print(f'{" " * 7} ISSUE READ EXECUTE WRITE')
    for tkey in table_printer:
        print(f'{tkey}: {table_printer[tkey]["ISSUE"]} {table_printer[tkey]["READ"]} {table_printer[tkey]["EXECUTE"]} {table_printer[tkey]["WRITE"]}')
