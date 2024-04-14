from src.parsers import OPCODES

table_printer = {}

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
        if table_printer[key][instruc["status"]] == 0:
            table_printer[key][instruc["status"]] = cls

def update_create_a_list(instrucs, cls):
    for instruc in instrucs:
        update_create_a_iten(instruc, cls)

def _format_table():
    a = f'{" " * 18} ISSUE READ EXECUTE WRITE\n'
    for tkey in table_printer:
        n = len(tkey)
        i = len(str(table_printer[tkey]["ISSUE"]))
        r = len(str(table_printer[tkey]["READ"]))
        e = len(str(table_printer[tkey]["EXECUTE"]))
        a += f'{tkey}:{" " * (18 - n)}{table_printer[tkey]["ISSUE"]}{" " * (6 - i)}{table_printer[tkey]["READ"]}{" " * (5 - r)}{table_printer[tkey]["EXECUTE"]}{" " * (8 - e)}{table_printer[tkey]["WRITE"]}\n'
    return a

def print_table():
    print(_format_table())

def print_table_in_file(path):
    tbl = _format_table()
    with open(path, 'w') as f:
        f.write(tbl)

