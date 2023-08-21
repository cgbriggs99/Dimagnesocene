#!/usr/bin/python3

import os
import sys
import mpy4py.futures
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

    with concurrent.futures.ProcessPoolExecutor(max_workers) as executor :
        res = executor.map(lambda inf, outf : \
                     os.system(transform_command(command, inf, outf)),
                     in_files, out_files)
        concurrent.futures.wait(res)

def run_mpi(command, in_files, out_files, max_workers = None) :
    """
run_mpi
-------

Runs a command in parallel using MPI.
"""
    with mpi4py.futures.MPIPoolExecutor(max_workers) as executor :
        res = executor.map(lambda inf, outf : \
                           os.system(transform_command(command, inf, outf)),
                           in_files, out_files)
        mpi4py.futures.wait(res)


    
