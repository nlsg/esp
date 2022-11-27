#!/usr/bin/env python
"""this python script extracts signature and docstring, of given functions.
Recogniseing decoratores is yet not implemented.
The data is then outputed to a json or org file,
later is especially usefull, if this script is
implemented in a org file. In that case, make
sure that the src_block has the ':results raw' option added
"""

from os import popen
from json import dump
from datetime import datetime as dt

SRC_PATH = "./src/"
OUT_FILE = "./docs.json"

def pop_keys(keys, *dicts):
    """removes all keys in dicts and returns a list of the resulting dicts"""
    res_dict = []
    for b in dicts:
        [b.pop(k) for k in keys]
        res_dict.append(b)
    return res_dict

def extract_docs(files):
    """outputs a dict with given filenames as keys,
    whose values are dicts with function signature
    and docstring key value pairs"""
    docs = {}
    for file in files:
        functions = {}
        for f in "".join(open(file, "r").readlines()).split("def "):
            try:
                doc = f.split('"""')[1]
            except IndexError:
                doc = "N/A"
            functions.update({f.split("\n")[0]: doc})
        docs.update({file: functions})
    return docs

def dict_to_org(d, indent=1):
    """
    * TODO add support for lists!
    * TODO add print format input ( eg fmt="{}\n{}" )
    recursivly transforms a dict to an org-file.
    The heading level is controled by the indent parameter
    e.g.
    >>> dict_to_org({"foo":"bar","bar"{"oof":"baz"}}, indent=2)"""
    # ** foo
    #    bar
    # ** bar
    # *** off
    #     baz
    return "\n".join([
        "\n".join((
            "*"*(indent) + " " + str(k),
            dict_to_org(d[k], indent+1)
            if isinstance(d[k], dict)
            else " "*(indent+1) + str(d[k])))
        for k in d])

# for org src_block output
# return "** -> docstrings (" \
#         + dt.now().strftime("%Y-%m-%d - %H:%M:%S") \
#         + ")\n" \
#         + dict_to_org(extract_docs([SRC_PATH + f
#                                     for f in popen("ls ./src").read().split("\n") if ".py" in f]),
#                       indent=3)
# dump(docs, open(OUT_FILE, "w"), indent=2)
