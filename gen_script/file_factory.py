#!/usr/bin/python3

import math
import os
from . import variables

"""
file_factory
------------

Produces output files with the given specifications. Looks for lines that look
like

%varname $start$, $end$, $points$
or
%varname [items]

then collects all of these into a mesh and replaces instances of the variable
name in the code, generating new files for each combination.

For the list item, each element should be surrounded by dollar signs. Nesting is not
available at this time. For range items, each position also needs to be surrounded.
Any function or constant from math may be used in range items.
"""

def gather_variables(file) :
    """
gather_variables
----------------

Find variables in a file and put them into a dictionary.
"""
    out = []
    with open(file, "r") as fp :
        linenum = 1
        for l in fp :
            line = l
            skip = 1
            # Concatenate line continuations.
            while len(l) > 2 and l[-2] == "\\" :
                line += l[:-2]
                try :
                    l = next(fp)
                except StopIteration :
                    raise SyntaxError("Improperly formatted file. Ends in a backslash.")
                skip += 1
            if len(line) == 0 :
                linenum += 1
                continue
            if line[0] == "%" :
                # There is a variable.
                name = ""
                i = 1
                # Get the name.
                while not line[i].isspace() and i < len(line):
                    name += line[i]
                    i += 1
                # Skip space.
                while line[i].isspace() and i < len(line):
                    i += 1

                if i >= len(line) :
                    raise SyntaxError(f"Error on line {linenum} in file {file}:" +
                                      " Improperly formatted variable macro.")

                # Determine which kind of variable it is.
                var = None
                if line[i] == "[" :
                    # List variable.
                    try :
                        out.append(parse_list_var(name, line[i:]))
                    except SyntaxError as err :
                        raise SyntaxError(f"Error on line {linenum} in file {file}:" +
                                          " Improperly formatted variable macro list.")
                else :
                    # Range variable.
                    try :
                        out.append(parse_range_var(name, line[i:]))
                    except SyntaxError as err :
                        raise SyntaxError(f"Error on line {linenum} in file {file}:" +
                                          " Improperly formatted variable in macro range.")
            linenum += skip
    return out

def parse_list_var(name, definition) :
    """
parse_list_var
--------------

Parses a variable list.
"""
    vals = []

    quoted = "none"
    in_item = False
    escaped = False
    closed = False
    interrim_commas = 0
    i = 1 # First element is always [.
    item = ""
    while i < len(definition) :
        if closed and not definition[i].isspace() : # Stuff after the bracket
            raise SyntaxError
        elif not escaped and definition[i] == "$" and quoted == "none" :
            # Start or end of an item.
            if in_item :
                vals.append(item)
                item = ""
                interrim_commas = 0
            in_item = not in_item
        elif not in_item and definition[i] == "," :
            # There is a comma.
            if interrim_commas == 1 : # Too many commas!
                raise SyntaxError
            interrim_commas += 1
        elif not in_item and definition[i] == "]" :
            if interrim_commas > 0 :
                raise SyntaxError
            closed = True
        elif not in_item and definition[i].isspace() : # Ignore intervening spaces.
            pass
        elif not in_item :
            # Something else
            raise SyntaxError
        elif not escaped and definition[i] == "\"" : # Quoting. Ignore separators.
            if quoted == "double" :
                quoted = "none"
            elif quoted == "none" :
                quoted = "double"
            item += definition[i]
        elif not escaped and definition[i] == "'" : # Quoting again. Ignore separators.
            if quoted == "single" :
                quoted = "none"
            elif quoted == "none" :
                quoted = "single"
            item += definition[i]
        elif not escaped and definition[i] == "\\" : # Backslash escape.
            escaped = True
            item += definition[i]
        elif escaped and definition[i] == "\\" : # Need this for how escape is handled.
            escaped = False
            item += definition[i]
        else : # Handled all cases. Add the symbol.
            item += definition[i]

        # Handle escaping.
        if escaped and definition[i] != "\\" :
            escaped = False
        i += 1
    return variables.ListVariable(name, vals)

def parse_range_var(name, definition) :
    vals = []

    quoted = "none"
    in_item = False
    escaped = False
    interrim_commas = 0
    i = 0
    item = ""
    while i < len(definition) :
        if not escaped and definition[i] == "$" and quoted == "none" :
            # Start or end of an item.
            if in_item :
                vals.append(item)
                item = ""
                interrim_commas = 0
            in_item = not in_item
        elif not in_item and definition[i] == "," :
            # There is a comma.
            if interrim_commas == 1 : # Too many commas!
                raise SyntaxError
            interrim_commas += 1
        elif not in_item and definition[i].isspace() : # Ignore intervening spaces.
            pass
        elif not in_item :
            # Something else
            raise SyntaxError
        elif not escaped and definition[i] == "\"" : # Quoting. Ignore separators.
            if quoted == "double" :
                quoted = "none"
            elif quoted == "none" :
                quoted = "double"
            item += definition[i]
        elif not escaped and definition[i] == "'" : # Quoting again. Ignore separators.
            if quoted == "single" :
                quoted = "none"
            elif quoted == "none" :
                quoted = "single"
            item += definition[i]
        elif not escaped and definition[i] == "\\" : # Backslash escape.
            escaped = True
            item += definition[i]
        elif escaped and definition[i] == "\\" : # Need this for how escape is handled.
            escaped = False
            item += definition[i]
        else : # Handled all cases. Add the symbol.
            item += definition[i]

        # Handle escaping.
        if escaped and definition[i] != "\\" :
            escaped = False
        i += 1
    if len(vals) > 3 :
        raise SyntaxError
    if len(vals) == 3 :
        return variables.RangeVariable(name, eval(vals[0]), eval(vals[1]),
                                       eval(vals[2]))
    elif len(vals) == 2 :
        return variables.RangeVarialbe(name, eval(vals[0]), eval(vals[1]),
                                       50)
    else :
        raise SyntaxError
        
def generate_files(in_file, out_dir, out_prefix, out_suffix, variables) :
    """
generate_files
--------------

Preprocesses a file with the given variable replacements.
"""
    indices = [0 for i in range(len(variables))]
    max_vals = [len(var) for var in variables]

    # Generate the file name format string.
    fmt_str = "".join([out_dir, "/", out_prefix] +
                      ["-{}" for i in range(len(variables))] + [out_suffix])

    exit_cond = False

    names = [var.name for var in variables]

    # Check to see if the directory exists. If not, create it.
    if not os.path.isdir(out_dir) :
        os.mkdir(out_dir)
    while not exit_cond :
        # Generate the values.
        vals = [variables[i][indices[i]] for i in range(len(variables))]
        # Generate the file.
        generate_file(fmt_str.format(*indices), in_file, vals, names)

        # Increment the values.
        indices[0] += 1
        j = 0
        while j < len(indices) - 1 and indices[j] >= max_vals[j] :
            indices[j] = 0
            indices[j + 1] += 1
        # Gone through all possibilities.
        if indices[-1] == max_vals[-1] :
            exit_cond = True

def generate_file(fname, infile, vals, names) :
    """
generate_file
-------------

Generates a single file.
"""
    # Open files.
    infp = open(infile, "r")
    # In case the output prefix is a directory name, make sure the directory exists.
    if not os.path.isdir(os.path.dirname(fname)) :
        os.mkdir(os.path.dirname(fname))
    outfp = open(fname, "w+")
    
    for line in infp :
        if line[0] == "%" : # Skip these.
            continue
        # Replace occurrences.
        for val, name in zip(vals, names) :
            if isinstance(val, str) :
                line = line.replace(name, val)
            else :
                line = line.replace(name, str(val))
        # Output transformed line.
        print(line, end = "", file = outfp)
    infp.close()
    outfp.close()
