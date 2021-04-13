"""
This program is used to add informations to nodes from a sequence similarity
network uncompressed file. 

USAGE : {MANDATORY} -n [NODE_FILE] -a [ANNOTATION_FILES]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
A copy of the GNU General Public License is available at
http://www.gnu.org/licenses/gpl-3.0.html
"""

__author__ = "KLEIN Dylan"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "klein.dylan@outlook.com"


########################## MODULES TO IMPORT ##################################

from modules.functions_for_table import *
import argparse

###############################################################################


def arguments():
    """
    set arguments
    """

    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("-n", "--network_file", dest = "network_file",
        type = isfile, required = True,
        help = "File containing the sequence similarity network")
    parser.add_argument("-a", "--annotation_files", dest = "annotation_files",
        type = isfile, required = True,
        help = "File containing all annotations files")

    return parser.parse_args()


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # get file names
    file_names = get_files_from_argument(args.annotation_files)

    # add all genomic annotation corresponding to each node of the file
    for file in file_names:
        df = pd.read_table(file)
        peptides = [i for i in df["peptides"]]
        lines_to_check = []
        
        with fileinput.FileInput(args.network_file, inplace = True, backup = ".bak") as f:  
            for line in f:
                line = uniform_string(line)
                line_list = line.split()
                if line_list[0] in peptides:
                    out_line = get_replaced_line(line_list, peptides, df, lines_to_check)
                    out_line = replace_line(line, out_line)
                else:
                    out_line = line
                    out_line = replace_line(line, out_line)
            

if __name__ == '__main__':
    main()