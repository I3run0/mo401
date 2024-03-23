import logging as lgg
from pipeline_stages import *
from parsers import *
from printer import *

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
        for ind in range(len(processing_queue[0])):
            if read(processing_queue[0][ind]):
                issue_to_move.append(processing_queue[0][ind])

        exec_to_move = []
        for ind in range(len(processing_queue[1])):
            if execute(processing_queue[1][ind]):
                exec_to_move.append(processing_queue[1][ind])
        
        write_to_move = []
        for ind in range(len(processing_queue[2])):
            if write(processing_queue[2][ind]):
                write_to_move.append(processing_queue[2][ind])

        update_create_a_iten(instruc_to_issue, cls)
        update_create_a_list(processing_queue[0], cls)
        update_create_a_list(processing_queue[1], cls)
        update_create_a_list(processing_queue[2], cls)

        print_table( )

        if instruc_to_issue:
            processing_queue[0].append(instruc_to_issue)

        while issue_to_move != []:
            item = issue_to_move.pop(0)
            processing_queue[0].remove(item)
            processing_queue[1].append(item)

        while exec_to_move != []:
            item = exec_to_move.pop(0)
            processing_queue[1].remove(item)
            processing_queue[2].append(item)

        while write_to_move != []:
            item = write_to_move.pop(0)
            processing_queue[2].remove(item)
            end_queue.append(item)

        cls += 1

if __name__ == "__main__":
    main()