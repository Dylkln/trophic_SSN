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


#================================== Modules ==================================#

import argparse
from Bio import SeqIO
import copy
import csv
import glob
import gzip
import igraph as ig
import math
import os
import pandas as pd
import re
import subprocess
from subprocess import DEVNULL
import sys
import tarfile
import tempfile

#=============================================================================#

#=============================================================================#
#============================= General functions =============================#
#=============================================================================#


def determine_fieldnames(files, fieldnames):
    """
    Determine field names from the top line of each input files
    
    Parameters
    ----------

        files : one file or a list of files
        fieldnames : an empty list where the fieldnames will be stored

    Returns
    -------

        fieldnames : a list containing the fieldnames
    """

    if type(files) == str:
        

        with open(files, "r", newline = "") as f_in:
            dialect = csv.Sniffer().sniff(f_in.readline(), delimiters = ",\t")
            f_in.seek(0)
            reader = csv.reader(f_in, dialect)
            headers = next(reader)
            for h in headers:
                if h not in fieldnames:
                    fieldnames.append(h)
            return fieldnames

    else:
        for file in files:
            fieldnames = determine_fieldnames(file, fieldnames)
        return fieldnames


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


def get_id(f):
    """
    Retrieves the ID contained in a file name

    Parameters
    ----------

        f : a file name

    Returns
    -------

        "-".join(name) : the ID
        idts : a list of ID
    """

    if type(f) == str:
        name = f.split("/")[-1].replace("_", "-").split("-")[0:3]
        return "-".join(name)

    else:
        idts = []
        for file in f:
            name = get_id(file)
            idts.append(name)
        return idts


def isfile(path):
    """
    Check if path is an existing file
    
    Parameters
    ----------

        path : a path to a file

    Returns
    -------

        path : a path to a file
    """

    if not os.path.isfile(path):

        if os.path.isdir(path):
            err = f"{path} is a directory"
        else:
            err = f"{path} does not exist"

        raise argparse.ArgumentTypeError(err)

    return path


def read_as_tsv_file(file):
    """
    Reads a CSV file with a tabulation delimiter

    Parameters
    ----------

        file : a CSV file

    Yields
    -------

        row : a row of the CSV file
    """

    with open(file, "r") as f_in:
        reader = csv.DictReader(f_in, delimiter = "\t")
        for row in reader:
            yield row


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

    with gzip.open(file, "r") as f_in:
        for line in f_in:
            line = line.decode()
            yield line.strip()


def read_csv(file):
    """
    Reads a CSV file with a comma delimiter

    Parameters
    ----------

        file : a CSV file

    Yields
    -------

        row : a row of the CSV file
    """

    with open(file, "r") as f_in:
        dialect = csv.Sniffer().sniff(f_in.readline(), delimiters = ",;")
        f_in.seek(0)
        reader = csv.DictReader(f_in, dialect = dialect)
        for row in reader:
            yield row


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


#=============================================================================#
#============================ Functions for add.py ===========================#
#=============================================================================#


def get_fname(n, files):
    """
    Retrieves the file name containing the attributes of an ORF ID

    Parameters
    ----------

        n : an ORF ID
        files : a list of filenames

    Returns
    -------

        file : the file containing the attributes of the ORF ID
    """

    for file in files:
        i = "-".join(n.split("-")[0:2])
        if re.search(i, file):
            return file


def get_prefix(n):
    """
    Retrieves the ORF prefix based on an ORF ID

    Parameters
    ----------

        n : an ORF ID

    Returns
    -------

        an ORF ID prefix
    """

    pr = n.replace("-", ".").split(".")[0:5]

    if pr[3] == "Transcript":
        return "-".join(pr)
    else:
        del pr[-1]
        return "-".join(pr)


def get_rows(nset, file):
    """
    Retrieves a list of rows containing the ORF name, prefix and attributes

    Parameters
    ----------

        nset : a set of ORF IDs
        file : the file where to search the ORFs

    Returns
    -------

        rlist : a list of rows
    """

    rlist = []
    
    for row in read_csv(file):
        if row["peptides"] in nset:
            row["name"] = row["peptides"]
            row["prefix"] = get_prefix(row["peptides"])
            row.pop("peptides")
            rlist.append(row)

    return rlist


def write_rows(writer, rows):
    """
    Writes all rows contained in a list of rows in a file

    Parameters
    ----------

        writer : a csv.DictWriter
        rows : a list of rows
    """

    for row in rows:
        writer.writerow(row)


#=============================================================================#
#======================== Functions for attributes.py ========================#
#=============================================================================#


def add_keys_to_seq_dict(k, name, table_file):
    """
    Create a dictionary containing taxonomy and trophic information

    Parameters
    ----------

        k : a list of fieldnames
        name : an ID
        table_file : a CSV file

    Returns
    -------

        seq_dict : a dictionary containing all keys, the taxonomy, and the 
        trophy information
    """

    seq_dict = {}.fromkeys(set(k))

    for row in read_csv(table_file):
        if row["1_Metdb_ID"] == name.upper():
            for key, v in row.items():
                if key in seq_dict.keys():
                    seq_dict[key] = v

    for key, val in seq_dict.items():
        if not val and key != "peptides":
            seq_dict[key] = []

    return seq_dict


def check_value_in_row(row, seq_dict):
    """
    Fill a dictionary where values of specific keys are initiated lists

    Parameters
    ----------

        row : a dictionary containing the data
        seq_dict : the dictionary we want to fill

    Returns
    -------

        seq_dict : the dictionary filled
    """

    for key, value in row.items():
        if key in seq_dict and value not in seq_dict[key]:
            if value == None:
                if "NA" not in seq_dict[key]:
                    seq_dict[key].append("NA")
            else:
                seq_dict[key].append(value)

    return seq_dict


def fill_seq_dict(seq_dict, an_file, seq):
    """
    Fill the dictionary with the annotation linked to the sequence ID

    Parameters
    ----------

        seq_dict : the dictionary we want to fill
        an_file : the file containing the data
        seq : the ID

    Returns
    -------

        seq_dict : the dictionary filled
    """

    seq_dict["peptides"] = seq
    for an in read_as_tsv_file(an_file):
        if an["peptides"] == seq:
            seq_dict = check_value_in_row(an, seq_dict)

    seq_dict = replace_values(seq_dict)

    return seq_dict


def get_an_file(seq_file, an_filenames):
    """
    Retrives the ID and annotation file linked to the seq_file

    Parameters
    ----------

        seq_file : the dictionary we want to fill
        an_filenames : the file containing the data

    Returns
    -------

        file : the annotation file linked to the seq_file
        name : the ID linked to the seq_file
    """

    name = seq_file.split("/")[-1].strip("_records.txt")
    
    for file in an_filenames:
        i = get_id(file)
        if i == name:
            return file, name


def replace_values(seq_dict):
    """
    Replace values of a sequence dictionary

    Parameters
    ----------

        seq_dict : a dictionary

    Returns
    -------

        seq_dict : the dictionary completed
    """

    for k, v in seq_dict.items():
        if not seq_dict[k]:
            seq_dict[k] = "NA"
        elif seq_dict[k] and type(v) == list:
            seq_dict[k] = "|".join(v)

    return seq_dict


#=============================================================================#
#========================== Functions for count.py ===========================#
#=============================================================================#


def db_by_an_file(an_files):
    """
    Retrieves the count of each database for each annotation files

    Parameters
    ----------

        an_files : all annotation files

    Returns
    -------

        db_count : a dictionary containing the count of each database by file
    """

    db_count = {}

    for file in an_files:
        name = get_id(file)
        db_count[name] = {}
        for row in read_as_tsv_file(file):
            db = row["database"]
            if db not in db_count[name].keys():
                db_count[name][db] = 0
            db_count[name][db] += 1

    return db_count


def fill_dan(dan, an_files):
    """
    Fill the annotation dictionary with data contained in annotation files
    
    Parameters
    ----------

        dan : initiated annotation dictionary
        an_files : all annotation files

    Returns
    -------

        dan : annotation dictionary filled
    """

    for file in an_files:
        
        name = get_id(file)
        if name not in dan.keys():
            dan[name] = {}
        
        for index, row in enumerate(read_as_tsv_file(file)):
            
            pep = row["peptides"]
            
            if index == 0:
                ilist = set([pep])
                dan[name][pep] = 1
            
            else:
                if pep not in ilist:
                    ilist.add(pep)
                    dan[name][pep] = 0
                dan[name][pep] += 1

    return dan


def fill_dtr(dtr, transdecoder_files):
    """
    Fill transdecoder dictionary, create a transcript dictionary containing
    the length of each ID, count the number of sequences for all transdecoder
    files

    Parameters
    ----------

        dtr : initiated transdecoder dictionary
        transdecoder_files : all transdecoder files

    Returns
    -------

        dtr : transdecoder dictionary filled
        transcript : dictionary containing the length by sequence ID
        seq_count : the total number of sequences
    """

    transcript = {}
    seq_count = 0

    for file in transdecoder_files:

        name = get_id(file) 
        
        if name not in transcript.keys():
            transcript[name] = {}

        fasta_sequences = SeqIO.parse(open(file), 'fasta')
        
        for index, fasta in enumerate(fasta_sequences):
            
            dtr[name]["nb_orf"] += 1
            seq_count += 1

            if index == 0:
                ilist = set([fasta.id])
                transcript[name][fasta.id] = len(fasta)
                dtr[name]["records"].append(fasta.id)

            else:
                if fasta.id not in ilist:
                    ilist.add(fasta.id)
                    transcript[name][fasta.id] = len(fasta)
                    dtr[name]["records"].append(fasta.id)


    return dtr, transcript, seq_count


def save_dan(dan):
    """
    Saves the annotation dictionary into a file

    Parameters
    ----------

        dan : annotation dictionary filled
    """

    for k, v in dan.items():
        
        p = f"../results/{k}"
        if not os.path.exists(p):
            os.mkdir(p)

        output = f"../results/{k}/{k}_annotation_count.txt"
        with open(output, "w") as f_out:
            f_out.write("orf\tnb_annotation\n")
        
            for key, val in v.items():
                f_out.write(f"{key}\t{val}\n")


def save_db_count(file, db_count):
    """
    Saves the db_count dictionary into a file
    
    Parameters
    ----------

        file : a filename
        db_count : a dictionary containing the count of each database for
        each file
    """

    with open(file, "w") as f_out:
        for key, value in db_count.items():
            for key2, value2 in value.items():
                f_out.write(f"{key} {key2} {value2}\n")


def save_dtr(dtr):
    """
    Saves the transdecoder dictionary into several specific files

    Parameters
    ----------

        dtr : transdecoder dictionary filled
    """

    records = []

    for k, v in dtr.items():
        
        p = f"../results/{k}"
        if not os.path.exists(p):
            os.mkdir(p)

        output = f"../results/{k}/{k}_orf_nb.txt"
        with open(output, "w") as f_out:
            f_out.write("ORF_number\n")
            orf = v["nb_orf"]
            f_out.write(f"{orf}\n")
        
        p = "../results/records"
        if not os.path.exists(p):
            os.mkdir(p)
        
        output = f"../results/records/{k}_records.txt"
        with open(output, "w") as f_out:
            for r in v["records"]:
                f_out.write(f"{r}\n")
        
        records.append(os.path.abspath(output))
    
    files = "../data/records_files"
    save_ids(records, files)


def save_ids(seq_ids, ids_file):
    """
    Saves all sequence IDs into a file

    Parameters
    ----------

        seq_ids : sequence IDs
        ids_file : the output file
    """

    with open(ids_file, "w") as f_out:
        for i in seq_ids:
            f_out.write(f"{i}\n")


def save_seq_count(file, seq_count):
    """
    Saves the seq_count in a file

    Parameters
    ----------

        file : the output file
        seq_count : the number of sequences in all fasta files
    """

    with open(file, "w") as f_out:
        f_out.write(f"{seq_count}")


def save_transcript(transcript):
    """
    Saves transcript dictionary in a file

    Parameters
    ----------

        transcript : dictionary containing the length by sequence ID
    """
    for k, v in transcript.items():
        
        output = f"../results/{k}/{k}_len_by_transcript.txt"
        with open(output, "w") as f_out:
            f_out.write("transcript\tlength\n")
        
            for key, val in v.items():
                f_out.write(f"{key}\t{val}\n")


#=============================================================================#
#========================= Functions for filter.py ===========================#
#=============================================================================#


def filter_file(inputfile, outputfile, cov, ident):
    """
    filter the file based on coverage and identity percentage.

    Parameters
    ----------

        inputfile : the file needed to be read
        outputfile : the file where to write outputs
        cov : the coverage percentage
        ident : the identity percentage

    Returns
    -------

        al_ssn : number of alignments in inputfile
        al_filt : number of alignment in output file
        nb_nssn : number of nodes in inputfile
        nb_nfilt : number of nodes in outputfile
    """
    al_ssn, al_filt, nb_nssn, nb_nfilt = 0, 0, 0, 0
    n_ssn = set([])
    n_filt = set([])

    fieldnames = ["qseqid", "qlen", "qstart", "qend", "sseqid", "slen",
    "sstart", "send", "length", "pident", "ppos", "score", "evalue",
    "bitscore"]
    
    writer = csv.DictWriter(open(outputfile, "w"), delimiter = "\t",
        fieldnames = fieldnames)
    reader = csv.DictReader(open(inputfile), delimiter = "\t",
        fieldnames = fieldnames)
    
    for index, row in enumerate(reader):
        
        al_ssn += 1
        n = [row["qseqid"], row["sseqid"]]
        
        if n[0] not in n_ssn:
            n_ssn.add(n[0])
            nb_nssn += 1


        if not row["pident"] or not row["ppos"]:
            print(index)
            print(row)
            continue
        
        else:
            if float(row["pident"]) >= ident and float(row["ppos"]) >= cov:
                if n[0] == n[1]:
                    continue
                else:
                    writer.writerow(row)
                    al_filt += 1
                    if n[0] not in n_filt:
                        n_filt.add(n[0])
                        nb_nfilt += 1

    return al_ssn, al_filt, nb_nssn, nb_nfilt




def remove_repeating_nodes(inputfile, outputfile):
    """
    Opens the node file, and remove repeating nodes, saving each lines
    in a new output file given in argument

    Parameters
    ----------

        file : the input node file
        output : the output node file
    """

    fieldnames = ["qseqid", "qlen", "qstart", "qend", "sseqid", "slen",
    "sstart", "send", "length", "pident", "ppos", "score", "evalue", "bitscore"]
    
    writer = csv.DictWriter(open(outputfile, "w"), delimiter = "\t",
        fieldnames = fieldnames)
    reader = csv.DictReader(open(inputfile), delimiter = "\t",
        fieldnames = fieldnames)

    for index, row in enumerate(reader):

        n = [row["qseqid"], row["sseqid"]]
        ns = sorted(n)
        n_l = f"{n[0]} {n[1]}"

        if index == 0:
            slist = set([n_l])
            writer.writerow(row)
    
        else:
            if n_l not in slist:
                slist.add(n_l)
                writer.writerow(row)


#=============================================================================#
#========================== Functions for find.py ============================#
#=============================================================================#


def find_file(pattern, path):
    """
    Find all matches of a pattern in a path and save them in a list
    
    Parameters
    ----------

        pattern : the pattern to search for
        path : the path where to search for the pattern

    Returns
    -------

        result : a list of files found
    """

    result = glob.glob(f"{path}/*/{pattern}")
    return result


def save_to_txt(result, file):
    """
    Saves a list into a txt file
    
    Parameters
    ----------

        result : the list of files found
        file : the output file
    """

    with open(file, "w") as f:
        for i in result:
            f.write(f"{i}\n")


#=============================================================================#
#======================== Functions for network.py ===========================#
#=============================================================================#


def db(string):
    """
    Retrieves the name of the database based on the string provided in argument

    Parameters
    ----------

        string : a database ID

    Returns
    -------

        k : the database associated to the database ID
    """
    ll = [["PFAM", "PF"], ["SMART", "SM"], ["PROSITEPROFILES", "PS5"], 
         ["GENE3D", "G3DSA"], ["PROSITEPATTERNS", "PS0"], ["SUPERFAMILY", "SSF"],
         ["CDD", "cd"], ["TIGRFAM", "TIGR"], ["PIRSF", "PIRSF"],
         ["PRINTS", "PR"], ["HAMAP", "MF"], ["PRODOM", "PD"],
         ["SFLD", "SFLD"], ["PANTHER", "PTHR"], ["NA", "nan"]]
    
    d = {}
    for l in ll:
        d[l[0]] = l[1]
    
    for k, v in d.items():
        if string.startswith(v):
            return k


def get_abund(l):
    """
    Retrieves the abundance of each element of a list

    Parameters
    ----------

        l : a list of transcript

    Returns
    -------

        d : a dictionary representing the abundance of each trancript in the list
    """
    d = {}
    
    for i in l:
        iid = "-".join(i.split("-")[0:2])
    
        if iid not in d.keys():
            d[iid] = 0
        d[iid] += 1

    return d


def get_abund_distrib(d):
    """
    Retrieves the distribution of the abundance of a dictionary

    Parameters
    ----------

        d : a dictionary with the abundance of each transcript

    Returns
    -------

        ad : a dictionary containing the distribution of the abundance
    """
    
    ad = {}
    
    for k, v in d.items():
        if len(v) == 1:
    
            for k2 in v.keys():
                if k2 not in ad.keys():
                    ad[k2] = 0
                ad[k2] += 1
    return ad


def get_cc_len(fn):
    """
    Retrieves the number of nodes contained in a CC

    Parameters
    ----------

        fn : a dictionary containing all Databases in the CC

    Returns
    -------

        cl : a dictionary containing all nodes number of each CC
    """
    
    l, cl = {}, {}
    
    for k, v in fn.items():
        l[k] = len(v)


    for k, v in l.items():
        if v not in cl.keys():
            cl[v] = 0
        cl[v] += 1

    return cl


def get_count(l):
    """
    Retrieves the count of each value on a list
    
    Parameters
    ----------

        l : a list

    Returns
    -------

        c : a dictionary containing the count of each value of the list
    """

    c = {}
    
    for i in l:
        if i not in c.keys():
            c[i] = 0
        c[i] += 1
    
    return c


def get_data_from_cc(g_cc):
    """
    Retrives all wanted data from a connected component (CC)

    Parameters
    ----------

        g_cc: a connected componant of a graph

    Returns
    -------

        fn : a dictionary containing all Databases in the CC
        tp : a dictionary containing all Phylums in the CC
        tg : a dictionary containing all Genus in the CC
        tr : a dictionary containing all Trophies information in the CC
        ab : a dictionary containing the abundance of transcript in the CC
    """

    fn, tp, tg, tr, ab, db_sp = {}, {}, {}, {}, {}, {}

    for index, cc in enumerate(g_cc):
        f = get_db_id(cc.vs["identifiant"])
        fn[index] = get_db(f)
        tp[index] = cc.vs["Phylum_Metdb"]
        tg[index] = cc.vs["Genus_Metdb"]
        tr[index] = cc.vs["Trophy"]
        ab[index] = get_abund(cc.vs["name"])
        db_sp[index] = get_db_sp(f)

    return fn, tp, tg, tr, ab, db_sp


def get_data_from_cc_dicts(tr, db_sp, fn_p):
    """
    Retrieves different data from the several connected components dictionaries
    
    Parameters
    ----------

        tr : a dictionary containing all Trophies information in the CC
        db_sp : 
        fn_p : a dictionary containing the percentage of all Databases
        in the CC

    Returns
    -------

        tr_c : a dictionary containing the number of trophies in each CC
        u_tr : a dictionary containing the number CC with only one trophy
        hi : a dictionary containing the homogeneity score from each Database
        of each CC
        f_en : a dictionary containing the entropy of all Databases on each CC

    """

    tr_c, u_tr, hi, f_en = {}, {}, {}, {}

    for k, v in tr.items():
        if k not in tr_c.keys():
            tr_c[k] = get_count(v)

    for k, v in tr_c.items():
        c = len(v)
        if c == 1:
            for key in v.keys():
                if key not in u_tr.keys():
                    u_tr[key] = 0
                u_tr[key] += 1
        else:
            if "not_unique" not in u_tr.keys():
                u_tr["not_unique"] = 0
            u_tr["not_unique"] += 1

    for k, v in db_sp.items():
        for k2, v2 in v.items():
            if k not in hi.keys():
                hi[k] = {}
            if k2 not in hi[k].keys():
                hi[k][k2] = get_homogeneity_score(v2)

    for k, v in fn_p.items():
        if k not in f_en.keys():
            f_en[k] = get_entropy(v)

    return tr_c, u_tr, hi, f_en


def get_data_percent(fn, tp, tg, tr):
    """
    Retrieves data percentage of each information extracted from a CC

    Parameters
    ----------

        fn : a dictionary containing all Databases in the CC
        tp : a dictionary containing all Phylums in the CC
        tg : a dictionary containing all Genus in the CC
        tr : a dictionary containing all Trophies information in the CC

    Returns
    -------

        fn_p : a dictionary containing the percentage of all Databases
        in the CC
        tp_p : a dictionary containing the percentage of all Phylums
        in the CC
        tg_p : a dictionary containing the percentage of all Genus
        in the CC
        tr_p : a dictionary containing the percentage of all Trophies 
        information in the CC
    """

    fn_p, tp_p, tg_p, tr_p = {}, {}, {}, {}

    for k in fn.keys():
        fn_p[k] = get_percent(fn[k])
        tp_p[k] = get_percent(tp[k])
        tg_p[k] = get_percent(tg[k])
        tr_p[k] = get_percent(tr[k])

    return fn_p, tp_p, tg_p, tr_p


def get_db(l):
    """
    Retrives a list of all database contained in a CC

    Parameters
    ----------

        l : a list of database IDs

    Returns
    -------

        db_l : a list of all database contained in a CC
    """

    db_l = []
    
    for i in l:
        db_l.append(db(i))
    
    return db_l


def get_db_id(l_o_l):
    """
    Retrieves a list of all database ID contained
    in a list of long string of database ID
    
    Parameters
    ----------

        l_o_l : a list of long string of database ID

    Returns
    -------

        a : a list of all database ID contained in l_o_l
    """

    a = []
    
    for l in l_o_l:
    
        if l == "nan":
            a.append(l)
    
        else:
            l = str(l)
            sl = l.split("|")
    
            for i in sl:
                a.append(i)
    
    return a


def get_db_sp(l):
    """
    Retrieves a dictionary containing all annotations for each CC
    
    Parameters
    ----------

        l : a list of IDs

    Returns
    -------

        db_sp : a dictionnary containing all IDs by database
    """
    
    db_sp = {}
    lt = transform_list(l)
    
    for i in lt:
        name = db(i)
        if name not in db_sp.keys():
            db_sp[name] = {}
        if i not in db_sp[name].keys():
            db_sp[name][i] = 0
        db_sp[name][i] += 1
    
    return db_sp


def get_entropy(d):
    """
    Retrieves the Shannon entropy of dictionary values

    Parameters
    ----------

        d : a dictionary containing values on databases

    Returns
    -------

        en : the entropy of the dict values
    """
    n = len(d)
    en = 0
    for v in d.values():
        val = v/100
        if val == 1:
            return val
        en += -val * math.log(val, n)
    return round(en, 3)


def get_homogeneity_score(d):
    """
    Retrieves an homogeneity score from a dictionary
    
    Parameters
    ----------

        d : a dictionary containing values on databases

    Returns
    -------

        hi : a dictionary containing the homogeneity score for each database
    """


    le = 0
    
    for k, v in d.items():
        le += v
    
    u = len(d)
    
    if u == 1:
        return 1
    
    hi = round(1 - (u / le), 3)
    
    return hi


def get_percent(l):
    """
    Retrieves a percentage dictionary of all elements in a list
    
    Parameters
    ----------

        l : a list of elements

    Returns
    -------

        d_percent : a dictionary containing all percentages of each element of
        the list given in argument
    """
    
    tot = len(l)
    d = {}
    
    for i in l:
        if i not in d.keys():
            d[i] = 0
        d[i] += 1
    
    d_percent = {}
    
    for k, v in d.items():
        d_percent[k] = round(v / tot * 100, 2)
    
    return d_percent


def save_dict(d, output):
    """
    Save all data contained in a dictionary in a file

    Parameters
    ----------

        d : a dictionary
        output : the file where to save the data from the dictionary
    """
    
    with open(output, "w") as f:
        for k, v in d.items():
            f.write(f"CC_{k}\t{v}\n")


def save_dict_of_dict(d, output):
    """
    Save all data contained in a dictionary of dictionary in a file

    Parameters
    ----------

        d : a dictionary of dictionary
        output : the file where to save the data from the dictionary
    """
    
    with open(output, "w") as f:
        for k, v in d.items():
            for k2, v2 in v.items():
                f.write(f"CC_{k}\t{k2}\t{v2}\n")


def save_list_in_dict(d, output):
    """
    Save all data contained in a dictionary of lists in a file

    Parameters
    ----------

        d : a dictionary of lists
        output : the file where to save the data from the dictionary
    """

    with open(output, "w") as f:
        for k, v in d.items():
            for i in v:
                f.write(f"CC_{k}\t{i}\n")


def save_value(v, output):
    """
    Save data from a variable in a file

    Parameters
    ----------

        d : a variable containg a value
        output : the file where to save the data from the variable
    """
    with open(output, "w") as f:
        f.write(v)


def transform_list(l):
    """
    Retrieves a list containing all values of another list separated by "|"

    Parameters
    ----------

        l : a list of long string separated by "|"

    Returns
    -------

        lt : list of all values contained in l
    """

    lt = []
    for i in l:
        j = i.split("|")
        for i in j:
            lt.append(i)
    return lt


#=============================================================================#
#======================== Functions for tables.py ============================#
#=============================================================================#


def add_id(row, file):
    """
    Creates a new row containing the METdb ID

    Parameters
    ----------

        row : a dictionary depicting a row of a CSV file
        file : a file where to search for the ID

    Returns
    -------

        new_row : the row with the ID added
    """

    for line in read_file(file):
        line = line.replace("_", "-").upper()
        gen, sp, strain = row["Genus_Metdb"].replace(" ", ""), row["Species_Metdb"], row["Strain name_Metdb"].replace(" ", "")
        check_r = "{}-{}-{}".format(gen, sp, strain)
        
        if check_r.lower() in line.lower():
            new_row = add_id_to_line(line, row)
            return new_row


def add_id_to_line(line, row):
    """
    Adds ID to a key in a dictionary

    Parameters
    ----------

        line : a line of a file
        row : a dictionary depicting a row of a CSV file

    Returns
    -------

        row : the dictionary with a value added
    """

    idt = line.split("-")[0:3]
    row["Metdb_ID"] = "-".join(idt)

    return row


def get_new_row(row, common_column, file):
    """
    Retrieves a new row, which is a merged row from two different rows
    
    Parameters
    ----------

        row : a dictionary depicting a row of a CSV file
        common_column : a common column found in two different rows
        files : a file

    Returns
    -------

        row : the dictionary with a value added
    """

    for r in read_csv(files[0]):
                    
        row_id = row[common_column]
        r_id = r[common_column]

        if r_id == row_id:
            new_row = merge_two_rows(row, r)
            return new_row


def merge_two_rows(row1, row2):
    """
    Merge two rows into one

    Parameters
    ----------

        row1 : a dictionary depicting a row of a CSV file
        row2 : a dictionary depicting a row of a CSV file

    Returns
    -------

        row1 : a dictionary containing informations of both rows given in arg
    """

    for k, v in row2.items():
        if k not in row1.keys() or not row1[k]:
            row1[k] = v

    return row1


def search_for_word(common_fieldnames, string):
    """
    Search a word in a list

    Parameters
    ----------

        common_fieldnames : a list of common fieldnames of two CSV files
        string : the word to search for

    Returns
    -------

        fn : the fieldname where the word is contained in
    """

    for fn in common_fieldnames:
        if string in fn:
            return fn


#=============================================================================#
#========================= Functions for tar.py ==============================#
#=============================================================================#


def extract_compress_tar_file(tar_file):
    """
    Extracts a tar.gz file and compress each file in the archive

    Parameters
    ----------

        tar_file : the tar.gz archive
    """

    tf = tarfile.open(tar_file)
    
    for file in tf:
        tf.extract(file, "./extracted_files")
        command_gzip = ["gzip", f"./extracted_files/{file.name}"]
        subprocess.call(command_gzip, stdout = DEVNULL)

    tf.close()
