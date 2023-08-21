#!/usr/bin/python3

import os
import sys
import re

def descend_tree(directory) :
    """
descend_tree
------------

Descends a directory tree and returns all of the files.
"""
    dirs = [directory]
    out = []

    while len(dirs) != 0 :
        # Pop the last entry.
        curr = dirs.pop()

        # If the entry is a file, then add it and stop.
        if os.path.isfile(curr) :
            out.append(curr)
            continue

        # If it is not a directory, continue on.
        if not os.path.isdir(curr) :
            continue

        # Find the files within it.
        neighbors = map(lambda x: curr + "/" + x, os.listdir(curr))

        # We can assume that all files are new.
        for entry in neighbors :
            if os.path.isdir(entry) :
                # Add directories to the search list.
                dirs.append(entry)
            elif os.path.isfile(entry) :
                # Add files to the out list.
                out.append(entry)
            else :
                # Otherwise, ignore it.
                pass
    # Found all files.
    return out

def filter_includes(files, patterns) :
    """
filter_includes
---------------

Filters a list of files to only include those that match the patterns.
"""

    out = []

    for file in files :
        # Check if it matches at least one pattern.
        if any(re.match(reg, file) is not None for reg in patterns) :
            out.append(file)
    return out

def filter_excludes(files, patterns) :
    """
filter_excludes
---------------

Filters a list of files to exclude those that match the patterns.
"""

    out = []

    for file in files :
        # Check to see if it matches no pattern.
        if all(re.match(reg, file) is None for reg in patterns) :
            out.append(file)
    return out

def binary_insert(lst, item, compare = lambda x, y : x < y) :
    """
binary_insert
-------------

Use a binary search to insert an element into a list.
"""
    # Check for the degenerate case.
    if len(lst) == 0 :
        lst.append(item)
        return

    # Check if the item is outside the list.
    if compare(item, lst[0]) :
        lst.insert(0, item)
        return
    if item == lst[-1] :
        return
    
    if not compare(item, lst[-1]) :
        lst.insert(len(lst), item)
        return

    # Binary search.
    a = 0
    b = len(lst) - 1
    c = (a + b) // 2

    while b - a > 1 :
        if compare(item, lst[c]) :
            b = c
        else :
            a = c
        c = (a + b) // 2
    if compare(item, lst[a]) :
        lst.insert(a, item)
    elif item == lst[a] or item == lst[b] :
        # Already in list. Don't add.
        return
    else :
        lst.insert(b, item)
    

def collect_tree(input_dirs) :
    """
collect_tree
------------

Collects files from the directory tree.
"""

    out = []

    for d in input_dirs :
        # Collect all files.
        files = descend_tree(d)
        
        # Add to the output, but only if it was not seen before.
        # Keep the list sorted for fast insertion.
        for file in files :
            binary_insert(out, file)
    return out

def collect_from_file(input_files) :
    """
collect_from_file
-----------------

Go line by line and collect inputs from a file.
"""
    files = []
    dirs = []
    for file in input_files :
        with open(file, "r") as fp :
            for line in fp :
                if line[0] == "#" :
                    # Skip a comment.
                    continue
                # Strip line and check what it is.
                line = line.strip()
                if os.path.isdir(line) :
                    dirs.append(line)
                elif os.path.isfile(line) :
                    files.append(line)
    return files, dirs
                    
            

def collect_inputs(input_dirs, patterns, input_files, exclude_dirs,
                   exclude_patterns, exclude_files) :
    """
collect_inputs
--------------

Collects input scripts and returns them as a list.
"""
    files = []
    dirs = []

    # Collect all possible inputs.
    dirs = collect_tree(input_dirs)
    files = input_files

    files_collected, dirs_collected = collect_from_file(input_files)
    files_exclude, dirs_exclude = collect_from_file(exclude_files)

    dirs_exclude += exclude_dirs

    # Filter out excluded directories.
    for d in dirs_collected :
        if all(re.match(ex, d) is None for ex in dirs_exclude) :
            dirs.append(d)
            
    # Filter through the directories for included and excluded files.
    filter_files = collect_tree(dirs)
    incl_files = []
    for file in filter_files :
        if any(re.fullmatch(pat, file) is not None for pat in patterns) or \
           len(patterns) == 0:
            incl_files.append(file)

    for file in incl_files :
        if all(re.fullmatch(pat, file) is None for pat in exclude_patterns) or \
           all(re.fullmatch(pat, file) is None for pat in files_exclude) :
            files.append(file)

    # Found all files.
    return files
