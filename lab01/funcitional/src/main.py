from src.parsers import *
from src.printer import *
from src.pipeline_stages import *
import sys

def _exct_pipln_multfunit_stage(to_move: list, to_process: list, action):
    for instruc in to_process:
        if action(instruc):
            to_move.append(instruc)

def _transfer_process_queue(totransfer: list, src_queue: list, tgt_queue: list):
    while totransfer != []:
        item = totransfer.pop(0)
        src_queue.remove(item)
        tgt_queue.append(item)

def main():
    if len(sys.argv) < 3:
        sys.exit("Paramenter are missing")

    units = funit_parser(sys.argv[1])
    instructions = code_parser(sys.argv[2])

    init_queue = instructions
    processing_queue = [[], [], [], []]
    end_queue = []

    init_funit_status_table(units)
    update_create_a_list(init_queue, 0)

    cls = 1
    while init_queue != [] or processing_queue[0] != [] or\
        processing_queue[1] != [] or processing_queue[2] != []:
        instruc_to_issue = None

        if init_queue != [] and issue(init_queue[0]):
            instruc_to_issue = init_queue.pop(0) 

        issue_to_move = []
        exec_to_move = []
        write_to_move = []

        _exct_pipln_multfunit_stage(issue_to_move, processing_queue[0], read)
        _exct_pipln_multfunit_stage(exec_to_move, processing_queue[1], execute)
        _exct_pipln_multfunit_stage(write_to_move, processing_queue[2],  write)

        update_create_a_iten(instruc_to_issue, cls)
        update_create_a_list(processing_queue[0], cls)
        update_create_a_list(processing_queue[1], cls)
        update_create_a_list(processing_queue[2], cls)

        print(f'cls: {cls}')
        print_table( )

        if instruc_to_issue:
            processing_queue[0].append(instruc_to_issue)

        _transfer_process_queue(issue_to_move, processing_queue[0], processing_queue[1])
        _transfer_process_queue(exec_to_move, processing_queue[1], processing_queue[2])
        _transfer_process_queue(write_to_move, processing_queue[2], end_queue)

        cls += 1
