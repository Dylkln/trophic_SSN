"""
This module file contains all the functions necessary for the operation of
programs capable of managing tables

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
import sys
import gzip
import csv
from itertools import chain
import re
import pandas as pd
from Bio import SeqIO
import fileinput

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


def get_files_from_argument(file):
    """
    Retrieves a list of filenames
    
    Parameters
    ----------

        file : a file given with the argument -f

    Returns
    -------

        files : a list of files contained in the file
    """

    files = []
    with open(file, "r") as f_in:
        for line in f_in:
            files.append(line.strip())

    return files


def save_data_from_dict_in_file(dictionary, file):
    """
    save data contained in a dict in a file

    Parameters
    ----------

        dictionary : a dictionary containing the data
        file : a file name
    """

    with open(file, "w") as f_out:
        for key, value in dictionary.items():
            f_out.write(f"{key} {value}\n")


def read_compressed_file(file):
    """
    Reads a compressed file

    Parameters
    ----------

        file : a compressed file given with the argument -f

    Yields
    -------

        line : a line of the file
    """

    with gzip.open(file, "rb") as f_in:
        for line in f_in:
            line = line.decode()
            yield line.strip()


def read_file(file):
    """
    Reads a file

    Parameters
    ----------

        file : a file given with the argument -f

    Yields
    -------

        line : a line of the file
    """

    with open(file, "r") as f_in:
        for line in f_in:
            yield line.strip()


def read_file_without_first_line(file):
    """
    Reads a file, skip the first line of the file

    Parameters
    ----------

        file : a compressed file given with the argument -f

    Yields
    -------

        line : a line of the file
    """

    with open(file, "r") as f_in:
        next(f_in)
        for line in f_in:
            yield line.strip()


def get_key_from_dict(dictionary, val):
    """
    Retrieves the key matching the value

    Parameters
    ----------

        dictionary : a dictionary
        val : a value contained in the dictionary

    Returns
    -------

        key : the key associated vith val
    """

    for key, value in dictionary.items():
        if value == val:
            return key


#============= Functions for the program "merge_table.py" ====================#


def read_table_file(file_1, file_2):
    """
    Reads csv files and retrieves pandas dataframes
    
    Parameters
    ----------

        file_1 : file entered in -f1 argument
        file_2 : file entered in -f2 argument
    
    Returns
    -------

        df1 : Pandas dataframe containing data from file_1
        df2 : Pandas dataframe containing data from file_2
    """

    df1 = pd.read_table(file_1, sep = "[\t,;]", engine = "python")
    df2 = pd.read_table(file_2, sep = "[\t,;]", engine = "python")

    return df1, df2


#========== Functions for the program "merge_table_memorysaving.py" ==========#


def get_delimiters(delimiter):
    """
    Retrieves delimiter based on the one entered as argument
    """

    t_list = ["tab", "t", "\t", "tabulation"]
    s_list = ["space", "espace"]

    if args.delimiter.lower() in t_list:
        return "\t"
    
    elif args.delimiter.lower() in s_list:
        return " "
    
    else:
        return args.delimiter


def determine_fieldnames(inputs, delimiter):
    """
    Determine field names from the top line of each input files

    Parameters
    ----------

        inputs : files given with -f argument
        delimiter : delimiter given with -d argument

    Returns
    -------

        Fieldnames : List of fieldnames
    """

    fieldnames = []

    for filename in inputs:
        with open(filename, "r", newline = "") as f_in:
            reader = csv.reader(f_in, delimiter = delimiter)
            headers = next(reader)
            for h in headers:
                if h not in fieldnames:
                    fieldnames.append(h)
        f_in.close()

    return fieldnames


def get_key_from_nested_dict(nested_dict, wanted_value):
    """
    Get the first key of a nested dictionary if the wanted value is
    present in the dictionary

    Parameters
    ----------

        nested_dict : a nested dictionary
        wanted_value : the value you want to search for in the nested dict

    Returns
    -------

        key : the first key associated with the wanted value of the nested dict
    """

    for key, value in nested_dict.items():
        for key2, value2 in value.items():
            if value2 == wanted_value:
                return key


def data_in_values(nested_dict, data):
    """
    Check if a variable data is in a nested dictionary, retrieves True
    or False

    Parameters
    ----------

        nested_dict : a nested dictionary
        data : a dataframe data

    Returns
    -------

        colname_in_values : boolean
    """

    values = set(chain.from_iterable(i.values() for i in nested_dict.values()))
    colname_in_values = data in values

    return colname_in_values


def replace_empty_string_by_NA(dictionary):
    """
    Replace empty values of a dictionary by "NA"

    Parameters
    ----------

        dictionary : a dictionary

    Returns
    -------

        dictionary : a dictionary where empty string are now "NA"
    """

    return {cle: val if val else "NA" for cle, val in dictionary.items()}


def copy_data(inputs, fieldnames, column_name, delimiter):
    """
    copy the data into a dictionary, remove redundancies and merge data
    
    Parameters
    ----------

        inputs : files given with -f argument
        fieldnames : a list of fieldnames
        column_name : column name given with -cn argument
        delimiter : delimiter given with -d argument

    Returns
    -------

        csv_data : a nested dictionary containing merged data from csv file(s)
    """

    csv_data = {}
    index = -1

    for filename in inputs:
        with open(filename, "r", newline = "") as f_in:
            reader = csv.DictReader(f_in, delimiter = delimiter)
            for row in reader:
                index += 1
                tmp = row[column_name]
                colname_in_values = data_in_values(csv_data, tmp)

                if colname_in_values:
                    cle_index = get_key_from_nested_dict(csv_data, tmp)
                    for key, value in row.items():
                        if key not in csv_data[cle_index]:
                            csv_data[cle_index][key] = value
                        if value not in csv_data[cle_index][key]:
                            csv_data[cle_index][key] = value
                    
                else:
                    if not index in csv_data:
                        csv_data[index] = row
                    for key, value in row.items():
                        if key not in csv_data[index]:
                            csv_data[index][key] = value
                        if value not in csv_data[index][key]:
                            csv_data[index][key] = value

    return csv_data


def write_csv(file, fieldnames, csv_data):
    """
    save the data in a new csv file

    Parameters
    ----------

        file : a filename
        fieldnames : a list of fieldnames
        csv_data : a nested dictionary containing merged data from csv file(s)

    Returns
    -------

        create a file and fill it with the data contained in csv_data
    """
    
    with open(file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for index, row in csv_data.items():
            row = replace_empty_string_by_NA(row)
            writer.writerow(row)



#============ Functions for the program "get_db_count_by_file.py" ============#


def read_table(file):
    """
    Retrieves a pandas dataframe created from a file

    Parameters
    ----------

        file : a file contained in the list of files

    Returns
    -------

        dataframe : a pandas dataframe containing the data of the file
    """

    return pd.read_table(file)


def get_filename(path):
    """
    Retrieves the last filename of a path

    Parameters
    ----------

        path : an absolute path

    Returns
    -------

        filename : a filename where the path leads to
    """

    return os.path.basename(os.path.normpath(path))


def get_db_count_by_file(files):
    """
    Retrieves a dictionary containing database count by file

    Parameters
    ----------

        files : a list of files

    Returns
    -------

        db_count : a dictionary containing the count of each database for
        each file
    """

    db_count = {}

    for file in files:
        file_df = read_table(file)
        tmp = [i for i in file_df["database"]]
        key = get_filename(file)
        db_count[key] = {}

        for db in tmp:
            if db not in db_count[key].keys():
                db_count[key][db] = 0
            db_count[key][db] += 1

    return db_count


def save_db_count_by_file(file, db_count):
    """
    Save the db_count dictionary into a file
    
    Parameters
    ----------

        file : a filename
        db_count : a dictionary containing the count of each database for
        each file

    Returns
    -------

        create a file and fill it with the data contained in db_count
    """

    with open(file, "w") as f_out:
        for key, value in db_count.items():
            for key2, value2 in value.items():
                f_out.write(f"{key} {key2} {value2}\n")


#=============== Functions for the program "count_node.py" ===================#


def create_id_dict(file):
    """
    Reads a file and create a dictionary

    Parameters
    ----------

        files : a file containing IDs

    Returns
    -------

        id_dic : a dictionary containing IDs as keys and 0 as values
    """

    id_dic = {}

    with open(file, "r") as f_in:
        for line in f_in:
            id_dic[line.strip().lower()] = 0

    return id_dic


def check_id(id_dic, idt):
    """
    Checks if an id is in the id_dic

    Parameters
    ----------

        idt : an ID
        id_dic : a dictionary containing IDs as keys and 0 as values
    """

    if idt in id_dic.keys():
        if id_dic[idt] == 0:
            id_dic[idt] += 1
        else:
            pass


def count_nodes(id_dic):
    """
    Counts the number of nodes in the id_dic

    Parameters
    ----------

        id_dic : a dictionary containing IDs as keys and 0 as values

    Returns
    -------

        count : the number of nodes contained in the id_dic
    """

    count = 0
    for value in id_dic.values():
        count += value

    return count

def save_node_count(count, file):
    """
    Saves the node count in a file

    Parameters
    ----------

        nodes : a list of nodes without duplicates
        file : a filename

    Returns
    -------

        create a file and fill it with the number of nodes
    """

    with open(file, "w") as f_out:
        f_out.write(f"{count}")


#=============== Functions for the program "count_seq.py" ====================#


def count_seq_in_files(files):
    """
    Retrieves a count of all sequences contained in all fasta files

    Parameters
    ----------

        files : a list of fasta files

    Returns
    -------

        seq_count : the number of sequences in all fasta files
        record : IDs of all fasta sequences
    """
    
    seq_count = 0
    record = []

    for file in files:
        fasta_sequences = SeqIO.parse(open(file), 'fasta')
        for fasta in fasta_sequences:
            seq_count += 1
            record.append(fasta.id)

    return seq_count, record


def save_seq_count(file, seq_count):
    """
    save the seq_count in a file

    Parameters
    ----------

        file : a filename
        seq_count : the number of sequences in all fasta files
    
    Returns
    -------

        create a file and fill it with the number of sequences
    """

    with open(file, "w") as f_out:
        f_out.write(f"{seq_count}")


def save_record(file, record):
    """
    Saves all IDs in a file

    Parameters
    ----------

        file : the file where to save the IDs
        record : a list of IDs
    """

    with open(file, "w") as f_out:
        for ID in record:
            f_out.write(f"{ID}\n")


#=========== Functions for the program "count_transcript.py" =================#


def check_id_in_list(transcript_files, key):
    """
    Checks if the ID is in a list and how many times the ID appears
    if it is in the list

    Parameters
    ----------

        transcript_files : a list of transcript files
        key : a key from a dictionary

    Returns
    -------

        nb_of_transcripts : the number of transcripts for a key given
        in argument
    """
    nb_of_transcripts = 0
    
    for file in transcript_files:
        file_list = file.split("/")
        if key == file_list[7]:
            nb_of_transcripts += 1

    return nb_of_transcripts


def count_transcript(idts, transcript_files):
    """
    Creates a dictionary with the number of transcripts by ID

    Parameters
    ----------

        idts : a list of IDs
        transcript_files : a list of transcript files

    Returns
    -------

        count_dict : a dictionary with the number of transcripts by ID
    """

    count_dict = {}
    
    for name in idts:
        count_dict[name] = check_id_in_list(transcript_files, name)
        if not count_dict[name]:
            count_dict[name] = 1

    return count_dict


#============ Functions for the program "find_strain_id.py" ==================#


def get_strain_id(file_names):
    """
    Retrieves strains IDs

    Parameters
    ----------

        file_names : a list of file name

    Returns
    -------

        strain_id : a list of strain IDs
    """

    strain_id = []
    
    for f in file_names:
        f = get_filename(f).strip("-paired_cut.cleaned.fasta.transdecoder.pep")
        strain_id.append(f.lower() + "-paired")

    return strain_id


#==== Functions for the program "add_annotation_to_uncompressed_file.py" =====#


def check_line(lines_to_check, line_list):
    """
    Checks if a line is exactly the same as another

    Parameters
    ----------

        lines_to_check : a list of lines
        line_list : a line converted in a list

    Returns
    -------

        True or False : a boolean if the line is exactly the same or not
        lines_to_check : a list of lines
    """

    if line_to_check:
        i = len(set(lines_to_check[0]) & set(line_list))
        if i == len(line_list):
            line_to_check = []
            return True, line_to_check
    
    line_to_check.append(line_list)
    return False, line_to_check

#    i = 0
#    if line_to_check:
#        for col in line_list:
#            if col in line_to_check[0]:
#                i += 1
#                if i == len(line_list):
#                    line_to_check = []
#                    return True, line_to_check
#    
#    line_to_check.append(line_list)
#    return False, line_to_check



def uniform_string(string):
    """
    Uniforms a string

    Parameters
    ----------

        string : a string

    Returns
    -------

        string : the same string as the one given in arguments except that tabs
        and carriage returns are replaced by space
    """

    replacements = ["\t", "\n"]
    for r in replacements:
        string = string.replace(r, " ")
    return string


def get_replaced_line(line_list, peptides, df, lines_to_check):
    """
    Retrieves the line that needs to overwrite the one in the file

    Parameters
    ----------

        line_list : a line converted to a list
        peptides : a list of peptides
        df : a pandas dataframe
        lines_to_check : a list of lines

    Returns
    -------

        out_line : the line that replaces the one in the file
    """

    j = list(df[df.peptides == line_list[0]].index)        
    tmp_len = [df.iloc[i]["length"] for i in j]
    tmp_db = [df.iloc[i]["database"] for i in j]
    tmp_id = [df.iloc[i]["identifiant"] for i in j]
    tmp = list(set(tmp_len)) + list(set(tmp_db) + list(set(tmp_id)))
    line_list.extend(tmp)
    line_list = [str(i) for i in line_list]

    isline_in_file, lines_to_check = check_line(lines_to_check, line_list)

    if isline_in_file:
        out_line = " ".join(lines_to_check)
        return out_line
        
    else:
        out_line = " ".join(line_list)
        return out_line


def replace_line(line, out_line):           
    """
    Overwrite the line in the file by the out_line

    Parameters
    ----------

        line : the line already in the file
        out_line : the line that replaces the one in the file
    """

    if out_line:
        print(line.replace(line, out_line), end = "\n")
        out_line = ""
        return out_line

#==== Functions for the program "add_annotation_to_compressed_file.py" =====#


def check_prev_and_node_line(prev_line, node_list):
    """
    Checks if the previous line is exactly the same as the node line

    Parameters
    ----------

        prev_line : the previous line
        node_list : the node line

    Returns
    -------

        True or False
    """

    i = set(prev_line) & set(node_list)
    if len(i) == len(node_list):
        return True
    return False


def get_interproscan(an_list):
    """
    Retrieves the Interproscan ID of a list

    Parameters
    ----------

        an_list : the annotation line

    Returns
    -------

        data or "NA" : the interproscan ID or "NA" if the ID is not found
    """

    for data in an_list:
        if data.startswith("IPR"):
            return data  
    return "NA"


def line_to_write(length, db, ipr, node_list):
    """
    Retrieves the line to be written in a file

    Parameters
    ----------

        length : a list of length
        db : a list of database ID
        ipr : a list of interproscan ID
        node_list : the node line

    Returns
    -------

        out_line : the line to be written in the file
    """

    line_list = node_list + length + db + ipr
    out_line = " ".join(line_list)
    return out_line


def assemble_all_files(filename, files):
    """
    Merges all files into one compressed file

    Parameters
    ----------

        filename : a file name
        files : a list of files to merge
    """

    with gzip.open(filename, "wb") as f:
        for file in files:
            for line in read_file_without_first_line(file):
                f.write(line.encode())
                f.write(b"\n")


def add_info_to_lists(length, db, ipr, an_list):
    """
    add informations of the length, database and interproscan to
    their lists respectively

    Parameters
    ----------

        length : a list of length
        db : a list of database ID
        ipr : a list of interproscan ID
        an_list : an annotation line

    Returns
    -------

        length : a list of length
        db : a list of database ID
        ipr : a list of interproscan ID
    """

    if an_list[1] not in length:
        length.append(an_list[1])
    if an_list[3] not in db:
        db.append(an_list[3])
    interpro = get_interproscan(an_list)
    if interpro not in ipr:    
        ipr.append(interpro)

    return length, db, ipr


def write_line_to_compressed_file(length, db, ipr, node_list, f):
    """
    Writes the line into a compressed file

    Parameters
    ----------

        length : a list of length
        db : a list of database ID
        ipr : a list of interproscan ID
        node_list : a node line
        f : the compressed file
    """

    out_line = line_to_write(length, db, ipr, node_list)
    f.write(out_line.encode())
    f.write(b"\n")


if __name__ == '__main__':
    sys.exit()