from py2neo import Node, Relationship, Graph
from copy import deepcopy
from time import sleep
from datetime import datetime
import re

from neo4j_manager import insert_node, label_word


# M = A or C
# W = A or T
# H = not G (A or C or T)

# Y = C or T
# K = G or T
# B = not A (C or G or T)

# R = G or A
# S = G or C
# V = not T (A or C or G)

# D = not C (A or G or T)

# N = A or C or G or T

ambiguous_replacements = {
    "N": "ACGT",
    "M": "AC",
    "W": "AT",
    "H": "ACT",
    "Y": "CT",
    "K": "GT",
    "B": "CGT",
    "R": "GA",
    "S": "GC",
    "V": "ACG",
    "D": "AGT"
}


def pattern_to_regex(pattern):
    regex_string = ""
    for c in pattern:
        if c in ambiguous_replacements:
            regex_string += "[" + ambiguous_replacements[c] + "]"
        else:
            regex_string += re.escape(c)

    return regex_string


def expand_chars(og_entry, pos, replacement_chars):
    expanded_seqs = set()
    # print(og_entry)
    # sleep(1)

    for c in replacement_chars:
        temp_str = list(og_entry)
        temp_str[pos] = c
        # print(pos, og_entry, ''.join(temp_str))
        expanded_seqs.add(''.join(temp_str))

    # print(expanded_seqs)

    return expanded_seqs


def expand_seqs(dna_entry):
    seqs_location = []
    expanded_seqs = set()
    dna_entry_str = dna_entry
    expanded_seqs.add(dna_entry_str)
    # print(dna_entry_str)

    for i in range(len(dna_entry_str)):
        if dna_entry_str[i] in 'ACGT^':
            continue
        else:
            seqs_location.append(i)
    # if len(seqs_location) > 5:
    #     return []
    for i in seqs_location:
        expanded_seqs_list = []
        for item in expanded_seqs:
            # print(item)
            # print(list(ambiguous_replacements[dna_entry_str[i]]))
            # print(expand_chars(item, i, list(ambiguous_replacements[dna_entry_str[i]])))
            for seq in expand_chars(item, i, list(ambiguous_replacements[dna_entry_str[i]])):
                expanded_seqs_list.append(seq)

        expanded_seqs = set(expanded_seqs_list)

    return expanded_seqs


graph = Graph(password="pass")
graph.schema.create_uniqueness_constraint(label_word, "pattern")

pairs = ['A^A', 'A^C', 'A^G', 'A^T', 'C^A', 'C^C', 'C^G', 'C^T',
         'G^A', 'G^C', 'G^G', 'G^T', 'T^A', 'T^C', 'T^G', 'T^T']
for pair in pairs:
    parent = Node(label_word)
    parent["pattern"] = pair
    parent["real_enzyme"] = False
    graph.merge(parent)
uniques = set()
time_begin = datetime.now()

with open('data_files/allenz_altered.txt') as input_file:
    lines = input_file.readlines()
    for line in lines:
        line = line.strip('\n')
        name, pattern = line.split(",")
        node = Node(label_word)
        node["name"] = name
        node["pattern"] = pattern
        node["real_enzyme"] = True

        seq_list = expand_seqs(pattern)
        for seq in seq_list:
            if seq in uniques:
                continue
            uniques.add(seq)
            entry_copy = deepcopy(node)
            entry_copy["pattern"] = seq

            if not graph.exists(entry_copy):
                insert_node(entry_copy)


time_end = datetime.now()

print("time:", time_end - time_begin)
