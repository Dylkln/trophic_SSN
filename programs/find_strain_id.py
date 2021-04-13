"""
This program is used to find strain ID in a txt file containing the names of transdecoded files,
then it will add these names to the table containing strains informations.

USAGE : {MANDATORY} -f [FILE] -s [STRAIN_FILE]

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
    parser.add_argument("-f", "--file", dest = "file",
        type = isfile, required = True,
        help = "the file containing the names of transdecoded files")
    parser.add_argument("-s", "--strain_file", dest = "strain_file",
        type = isfile, required = True,
        help = "the file containing strains information")

    return parser.parse_args()

def main():
    """
    Main program function
    """

    # get arguments
    args = arguments()

    # create pandas dataframe from the -s argument
    df = pd.read_table(args.strain_file, sep = ",")

    # get all filenames from -f argument
    file_names = get_files_from_argument(args.file)
    
    # get strain names from the dataframe
    strain_names = [i for i in df["Strain name"]]
    
    # get strain IDs from all files contained in file_names
    strain_id = get_strain_id(file_names)

    # add strain names to the pandas dataframe
    for pair in strain_id:
        for index, name in enumerate(strain_names):
            if str(name).lower() in pair:
                if type(pair) == str:    
                    pair = pair.split("-")
                    df.at[index, "metDB_ID"] = "_".join(pair[:2])
                else:
                    df.at[index, "metDB_ID"] = "_".join(pair[:2])

    # save the dataframe into a csv file
    df.to_csv("data_metDB_full.csv", index = False)


if __name__ == '__main__':
    main()