#!/usr/bin/python3

"""
script_runner
-------------

Runs several Psithon scripts (or otherwise) in parallel, especially on a cluster.
"""

import os
import argparse

from . import file_collector
from . import file_transformer
from . import runner

def main() :
    """
main
----

Main method for running the scripts.
"""

    parser = argparse.ArgumentParser(prog = "script_runner",
                                     description = "Runs several scripts in parallel.")
    parser.add_argument("-i", "--input-dir", help = "The directory where input "+
                        "files are placed.", action = "extend",
                        type = lambda x: [str(x)], default = [])
    parser.add_argument("-o", "--output-dir", help = "The directory where output "+
                        "files are placed.", type = str)

    parser.add_argument("-p", "--pattern", help = "Regex pattern for files to run.",
                        action = "extend", type = lambda x: [str(x)], nargs = 1,
                        default = [])
    parser.add_argument("-f", "--file", help = "File containing script names to run." +
                        " One script per line.",
                        type = lambda x: [str(x)], action = "extend",
                        default = [])
    parser.add_argument("--exclude-dir", help = "Exclude a directory from the search.",
                        action = "extend", type = lambda x: [str(x)],
                        default = [])
    parser.add_argument("--exclude-regex", help = "Exclude a regex from the search.",
                        action = "extend", type = lambda x: [str(x)],
                        default = [])
    parser.add_argument("--exclude-file", help = "Exclude all files, patterns, and " +
                        "and directories contained within the file. One entry per line.",
                        action = "extend", type = lambda x: [str(x)],
                        default = [])
    parser.add_argument("--runner", help = "The method to use to run the files.",
                        choices = ["mpi", "parallel", "sequential"],
                        default = "mpi", type = str)
    parser.add_argument("-n", help = "Number of workers for parallel execution.",
                        type = int, default = -1)
    parser.add_argument("-r", "--replace", help = """Replacement pattern. \
This is formatted something like ".in:.out". In this instance, this replaces \
any instance of ".in" in the input file with ".o". Using dollar signs and carets \
to indicate the end and start of the file name will also work. In this case, \
if the replacement is ".in$:.out", then the filename "a.in.in" will be \
transformed into "a.in.out". With the first, it would instead be transformed \
into "a.out.out". If the string does not match any of the first parts, then \
it will simply get a ".out" at the end.
""", action = "extend", type = lambda x: [str(x)], default = [])

    parser.add_argument("--command", help = """The command to use to run each script. \
Instances of #I are replaced with the input file name. #O is replaced with the \
output file name. #FI and #FO are replaced with the file part of the input and \
output respectively. #DI and #DO are replaced with the directory part of the \
input and output respectively. #SI and #SO are replaced with the file suffix \
of the input and output. The output suffix is, by default, ".out".
""", default = "psi4 -i #I -o #O", type = str)

    args = vars(parser.parse_args())

    if "output_dir" not in args :
        args["output_dir"] = args["input_dir"]

    in_files = file_collector.collect_inputs(args["input_dir"], args["pattern"], args["file"],
                              args["exclude_dir"], args["exclude_regex"],
                              args["exclude_file"])
    out_files = file_transformer.transform_all(in_files, args["replace"],
                                               args["output_dir"])

    if args["runner"] == "sequential" :
        print("Running sequentially")
        runner.run_sequential(args["command"], in_files, out_files)
    elif args["runner"] == "parallel" :
        runner.run_parallel(args["command"], in_files, out_files,
                            args["n"] if args["n"] > 0 else None)
    elif args["runner"] == "mpi" :
        runner.run_mpi(args["command"], in_files, out_files,
                       args["n"] if args["n"] > 0 else None)

if __name__ == "__main__" :
    main()
    
    
