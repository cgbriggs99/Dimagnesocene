#!/usr/bin/python3

"""
gen_script
----------

Generates Psithon scripts for computing potential energy surfaces.
"""

import argparse
from . import file_factory
import os

def main() :
    """
main
----

The main function for gen_script. Handles argument parsing then passes execution to other parts of the program.
"""
    parser = argparse.ArgumentParser("gen_script", description = """\
Generates Psithon scripts for computing potential energy surfaces. To use it,
add lines to your file specifying array variables. These are lines that begin
with % and are set up in one of the following ways.

# Range specification. 50 points.
%var1 $0$, $10$

# Range specification. Specify the points.
%var2 $0$, $10$, $100$

# List specification. These are inserted exactly as written. If you
# want to substitute a string, add quotes inside. Otherwise, they will be
# treated as a line of code.
%var3 [$x = 10$, $"Hello, World!"$]

Then, anytime there is a reference to $var1$, $var2$, or $var3$, the appropriate
value will be substituted. It is important to note that for ease of use, after
the scripts are generated, the variables var1, var2, and var3 will be available
as well to the programmer. So the following two lines will print the same thing
for each possible value.

print($var1$)
print(var1)

The following two will not. The first will throw an error when $var2$ is $x = 10$,
but will print "Hello, World!" without quotes, while the second will print
"x = 10" without quotes, then ""Hello, World!"" with quotes.

print($var3$)
print(var3)

When evaluating the range values, the math module can be used. This means that

%var3 $0$, $math.sqrt(2)$, $10$

will produce a result as expected. However, outside of math constants and functions,
no variables may be used.

This script is intended to be used to generate Psithon scripts for computing
potential energy surfaces, but its utility may extend beyond that.
""")

    parser.add_argument("-o", "--out", help = "Output directory.", default = ".")
    parser.add_argument("-p", "--prefix", help = "Prefix for files. Defaults to the input file name.", default = None)
    parser.add_argument("-s", "--suffix", help = "Suffix for files. Defaults to .in", default = ".in")
    parser.add_argument("--numbering", help = "Numbering scheme for output files.",
                        choices = ["sequential", "indexed"], default = "indexed")
    parser.add_argument("file", help = "Input file.")

    args = vars(parser.parse_args())

    if "prefix" not in args or args["prefix"] is None:
        # Filter out leading periods.
        args["prefix"] = list(filter(lambda x: x != '',
                                     os.path.basename(args["file"]).split('.')))[0]

    variables = file_factory.gather_variables(args["file"])
    print(f"Variables: {[var.name for var in variables]}")
    file_factory.generate_files(args["file"], args["out"], args["prefix"], args["suffix"],
                                variables, args["numbering"])

if __name__ == "__main__":
    main()
