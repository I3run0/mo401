FUNITS = {
    'int': 1,
    'mult': 2,
    'add': 3,
    'div': 4,
}

def funit_parser(filename):
    funits = []
    with open(filename, 'r') as f:
        for line in f:
            fields = line.replace(',', ' ').split()
            funit = fields[0]
            if funit not in FUNITS:
                raise ValueError(f'Invalid function unit: {funit}')
            funits.append({
                'type': fields[0],
                'qtt': int(fields[1]),
                'cls': int(fields[2]),
            })
    
    return funits