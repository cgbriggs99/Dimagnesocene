#!/usr/bin/python3

"""
gen_script
----------

Generates Psithon scripts for computing potential energy surfaces.
"""

import argparse
from . import file_factory

def main() :
    """
main
----

The main function for gen_script. Handles argument parsing then passes execution to other parts of the program.
"""
    parser = argparse.ArgumentParser("gen_script", "Generates Psithon scripts for computing potential energy surfaces.")

    parser.add_argument("-f", "--file", help = "Input Python file.")
    parser.add_argument("-o", "--out", help = "Output directory.", default = ".")
    parser.add_argument("-p", "--prefix", help = "Prefix for files. Defaults to the input file name.", default = None)
    parser.add_argument("-s", "--suffix", help = "Suffix for files. Defaults to .in", default = ".in")

    args = vars(parser.parse_args())

    if "prefix" not in args or args["prefix"] is None:
        args["prefix"] = os.path.basename(in_file).split('.')[0]

    variables = file_factory.gather_variables(args["file"])
    print(f"Variables: {[var.name for var in variables]}")
    file_factory.generate_files(args["file"], args["out"], args["prefix"], args["suffix"], variables)

if __name__ == "__main__":
    main()
