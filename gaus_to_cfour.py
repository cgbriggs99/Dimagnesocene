import os
import argparse

def fix_file(in_file, out_file) :
    with open(in_file, "r") as infp :
        with open(out_file, "w+") as outfp :
            for line in infp :
                ignore_space = True

                for ch in line :
                    if ch == "=" :
                        ignore_space = True
                        outfp.write(ch)
                    elif ignore_space and ch.isspace() :
                        ignore_space = True
                    elif ch.isspace() :
                        ignore_space = True
                        outfp.write(ch)
                    else :
                        ignore_space = False
                        outfp.write(ch)
                        
                        
def run() :
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help = "The input file name.")
    parser.add_argument("--output", help = "The output file name.")

    args = vars(parser.parse_args())

    fix_file(args["input"], args["output"])

if __name__ == "__main__" :
    run()
