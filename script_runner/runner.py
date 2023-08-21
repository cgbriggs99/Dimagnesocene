#!/usr/bin/python3

import os
import sys
try :
    import mpi4py.futures
    do_mpi = True
except ImportError as err :
    do_mpi = False
    print(err.msg + "\nWill run as concurrent instead.", sys.stderr)
import concurrent.futures

def transform_command(command, in_file, out_file) :
    """
transform_command
-----------------

Transforms a command by replacing symbols.
"""
    out = ""

    symbol = False
    file = False
    directory = False
    suffix = False
    
    for ch in command :
        if ch == "#" :
            symbol = True
        elif symbol and not file and not directory and not suffix and ch == "I" :
            out += in_file
        elif symbol and not file and not directory and not suffix and ch == "O" :
            out += out_file
        elif symbol and not file and not directory and not suffix and ch == "F" :
            file = True
        elif symbol and not file and not directory and not suffix and ch == "D" :
            directory = True
        elif symbol and not file and not directory and not suffix and ch == "S" :
            suffix = True
        elif symbol and file and not directory and not suffix and ch == "I" :
            out += os.path.basename(in_file)
        elif symbol and file and not directory and not suffix and ch == "O" :
            out += os.path.basename(out_file)
        elif symbol and not file and directory and not suffix and ch == "I" :
            out += os.path.dirname(in_file)
        elif symbol and not file and directory and not suffix and ch == "O" :
            out += os.path.dirname(out_file)
        elif symbol and not file and not directory and suffix and ch == "I" :
            out += "".join(map(lambda x: "." + x,
                               os.path.basename(in_file).split(".")[1:]))
        elif symbol and not file and not directory and suffix and ch == "O" :
            out += "".join(map(lambda x: "." + x,
                               os.path.basename(out_file).split(".")[1:]))
        elif symbol and (file or directory or suffix) and ch not in ["I", "O"] :
            symbol = False
            file = False
            directory = False
            suffix = False
        elif symbol and not file and not directory and not suffix and ch not in \
             ["D", "F", "I", "O", "S"] :
            symbol = False
            file = False
            directory = False
            suffix = False
        else :
            out += ch
    return out
        

def run_sequential(command, in_files, out_files) :
    """
run_sequential
--------------

Runs a command on several files sequentially.
"""
    for in_file, out_file in zip(in_files, out_files) :
        os.system(transform_command(command, in_file, out_file))

    
def run_parallel(command, in_files, out_files, max_workers = None) :
    """
run_parallel
------------

Runs a command in parallel.

"""
    commands = map(lambda inf, outf : \
                   transform_command(command, inf, outf),
                   in_files, out_files)
    with concurrent.futures.ProcessPoolExecutor(max_workers) as executor :
        res = executor.map(os.system, commands)
        #concurrent.futures.wait(res)

def run_mpi(command, in_files, out_files, max_workers = None) :
    """
run_mpi
-------

Runs a command in parallel using MPI.
"""
    if do_mpi :
        commands = map(lambda inf, outf : \
                       transform_command(command, inf, outf),
                       in_files, out_files)
        with mpi4py.futures.MPIPoolExecutor(max_workers) as executor :
            res = executor.map(os.system, commands)
            #mpi4py.futures.wait(res)
    else :
        run_parallel(command, in_files, out_files, max_workers)


    
