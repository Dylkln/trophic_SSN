"""
This module file contains all functions needed by main programs.

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

########################## MODULE TO IMPORT ###################################

import os
import glob

###############################################################################

#============================= General functions =============================#

def isfile(path):
    """
    Check if path is an existing file
    """

    if not os.path.isfile(path):

        if os.path.isdir(path):
            err = f"{path} is a directory"
        else:
            err = f"{path} does not exist"

        raise argparse.ArgumentTypeError(err)

    return path


#================= Functions for the program "find_path.py" ==================#

def find_file(pattern, path):
    """
    Find all matches of a pattern and save them in a list
    """
    result = glob.glob(f"{path}/*/{pattern}")
    return result


def save_to_txt(result, file):
    """
    save a list into a txt file
    """

    with open(file, "w") as f:
        for i in result:
            f.write(f"{i}\n")



if __name__ == '__main__':
	sys.exit()