#!/usr/bin/python3

import os

def transform(fname, repl) :
    """
transform
---------

Transforms a file name with one of the given replacements.
"""
    is_transformed = False
    for pattern in repl :
        # Separate the to and from.
        pat = pattern.split(":")
        # Start and end.
        if pat[0][0] == "^" and pat[0][-1] == "$" :
            if fname == pat[0][1:-1] :
                # Substitute.
                if pat[1][0] == "^" :
                    pat[1] = pat[1][1:]
                if pat[1][-1] == "$" :
                    pat[1] = pat[1][:-1]
                fname = pat[1]
                is_transformed = True
                continue
        # End of a string.
        if pat[0][-1] == "$" :
            # Check to see that fname matches.
            if fname.endswith(pat[0][:-1]) :
                if pat[1][0] == "^" :
                    pat[1] = pat[1][1:]
                if pat[1][-1] == "$" :
                    pat[1] = pat[1][:-1]
                fname = fname[:len(pat[0]) - 1] + pat[1]
                is_transformed = True
                continue
        # Start of a string.
        if pat[0][0] == "^" :
            # Check to see that fname matches.
            if fname.startswith(pat[0][1:]) :
                if pat[1][0] == "^" :
                    pat[1] = pat[1][1:]
                if pat[1][-1] == "$" :
                    pat[1] = pat[1][:-1]
                fname = pat[1] + fname[len(pat[0]) - 1:]
                is_transformed = true
                continue

        # Strip the from and to of their special characters.
        if pat[0][0] == "^" :
            pat[0] = pat[0][1:]
        if pat[0][-1] == "$" :
            pat[0] = pat[0][:-1]
        if pat[1][0] == "^" :
            pat[1] = pat[1][1:]
        if pat[1][-1] == "$" :
            pat[1] = pat[1][:-1]

        # Check to see if the file name matches.
        if fname.count(pat[0]) != 0 :
            # Replace.
            fname = fname.replace(pat[0], pat[1])
            is_transformed = True
    if not is_transformed :
        fname += ".out"
    return fname

def transform_all(files, patterns, out_dir) :
    """
transform_all
-------------

Transforms all files in a list using the given replacements.
"""

    out = []
    for file in files :
        out.append((out_dir if out_dir is not None else "")
                   + transform(os.path.basename(file), patterns))
    return out
    
