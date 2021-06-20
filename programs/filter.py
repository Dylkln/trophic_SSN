"""
This script remove repeating nodes with the same information: if node pairs
A > B and B > A are present, only one of the two pairs is kept. In addition,
this scripts can also filters a diamond output if minimum coverage and identity
that are wanted are provided in arguments.

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


#================================== Modules ==================================#

import argparse
from modules.functions import *

#=============================================================================#


def arguments():
    """
    set arguments
    """

    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("-n", "--node_file", dest = "node_file",
        type = isfile, required = True,
        help = "The file containing all nodes")

    # Optional arguments
    parser.add_argument("-ov", "--overlap", dest = "overlap",
        type = float, required = False, default = None, nargs = "+",
        help = "the filtration wanted of a diamond output")
    parser.add_argument("-id", "--identity", dest = "identity",
        type = float, required = False, default = None, nargs = "+",
        help = "the filtration wanted of a diamond output")

    return parser.parse_args()


def save_stats(output, al_ssn, al_filt, nb_nssn, nb_nfilt):
    with open(output, "w") as f:
        f.write(f"nb of alignments in base SSN : {al_ssn}\n")
        f.write(f"nb of alignments in filtered SSN : {al_filt}\n")
        f.write(f"nb of aligments removed : {al_ssn - al_filt}\n")
        f.write(f"nb of nodes in base SSN : {nb_nssn}\n")
        f.write(f"nb of nodes in filtered SSN : {nb_nfilt}\n")
        f.write(f"nb of nodes removed : {nb_nssn - nb_nfilt}")


def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    if args.overlap and args.identity:
        print("filtering informations provided")
        print("*** FILTERING FILE ***")
        ov_len = len(args.overlap)
        id_len = len(args.identity)

        for i in args.identity:
            for j in args.overlap:
                print(f"filtering infos ||| coverage : {j}%, identity : {i}%")
                output = f"{args.node_file}_pcov{int(j)}_pident{int(i)}"
                al_ssn, al_filt, nb_nssn, nb_nfilt = filter_file(args.node_file, output, j, i)
                
                print(f"nb of alignments in base SSN : {al_ssn}")
                print(f"nb of alignments in filtered SSN : {al_filt}")
                print(f"nb of aligments removed : {al_ssn - al_filt}")
                print(f"nb of nodes in base SSN : {nb_nssn}")
                print(f"nb of nodes in filtered SSN : {nb_nfilt}")
                print(f"nb of nodes removed : {nb_nssn - nb_nfilt}")

                output_stats = f"{output}_stats"
                save_stats(output_stats, al_ssn, al_filt, nb_nssn, nb_nfilt)

    elif not args.overlap and not args.identity:
        # open the node file, and remove repeating nodes, saving each lines
        # in a new output file given in argument
        print("No filtering information provided, removing repeating nodes ...")
        output = f"{args.node_file}_filtered"
        remove_repeating_nodes(args.node_file, output)

    else:
        print("*** ERROR ***")
        print("You must provide overlap AND identity filtration parameters")
        quit()


if __name__ == '__main__':
    main()