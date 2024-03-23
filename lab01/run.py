import logging as lgg
from pipeline_stages import *
from parsers import *
from printer import *

def exct_pipln_multfunit_stage(to_move: list, to_process: list, action):
    for instruc in to_process:
        if action(instruc):
            to_move.append(instruc)

def transfer_process_queue(totransfer: list, src_queue: list, tgt_queue: list):
    while totransfer != []:
        item = totransfer.pop(0)
        src_queue.remove(item)
        tgt_queue.append(item)

def main():
    init_queue = instructions
    processing_queue = [[], [], [], []]
    end_queue = []

    cls = 1

    while cls < 40 and (init_queue != [] or processing_queue[0] != [] or\
        processing_queue[1] != [] or processing_queue[2] != []):

        print(cls)
        instruc_to_issue = None

        if init_queue != [] and issue(init_queue[0]):
            instruc_to_issue = init_queue.pop(0) 

        issue_to_move = []
        exec_to_move = []
        write_to_move = []
        
        exct_pipln_multfunit_stage(issue_to_move, processing_queue[0], read)
        exct_pipln_multfunit_stage(exec_to_move, processing_queue[1], execute)
        exct_pipln_multfunit_stage(write_to_move, processing_queue[2],  write)

        update_create_a_iten(instruc_to_issue, cls)
        update_create_a_list(processing_queue[0], cls)
        update_create_a_list(processing_queue[1], cls)
        update_create_a_list(processing_queue[2], cls)

        print_table( )

        if instruc_to_issue:
            processing_queue[0].append(instruc_to_issue)

        transfer_process_queue(issue_to_move, processing_queue[0], processing_queue[1])
        transfer_process_queue(exec_to_move, processing_queue[1], processing_queue[2])
        transfer_process_queue(write_to_move, processing_queue[2], end_queue)

        cls += 1

if __name__ == "__main__":
    main()