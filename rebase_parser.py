from py2neo import Node, Relationship, Graph
from copy import deepcopy
from time import sleep
from datetime import datetime
import re

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
graph.schema.create_uniqueness_constraint("rebase_enzyme", "pattern")
uniques = set()
time_begin = datetime.now()

with open('data_files/allenz.txt') as input_file:
    temp_entry = None
    for line in input_file:
        temp_str = line.strip()
        clipped_str = temp_str[3:]

        if temp_str[:3] == "<1>":
            temp_entry = Node("rebase_enzyme")
            temp_entry["name"] = clipped_str
        elif temp_str[:3] == "<5>":
            cleave_num = clipped_str.find("(")

            nums = None

            if cleave_num != -1:
                cleave_num_end = clipped_str.find(")")
                nums = (clipped_str[cleave_num + 1:cleave_num_end]).split("/")
                clipped_str = clipped_str[:cleave_num]

            temp_entry["nums"] = nums

            if "?" in clipped_str or "," in clipped_str:
                continue

            seq_list = expand_seqs(clipped_str)
            for seq in seq_list:
                if seq in uniques:
                    continue
                uniques.add(seq)
                entry_copy = deepcopy(temp_entry)
                entry_copy["pattern"] = seq
                entry_copy["regex"] = pattern_to_regex(seq)
                entry_copy["real_enzyme"] = True

                if not graph.exists(entry_copy):
                    graph.merge(entry_copy)

            temp_entry = {}

#
# for res in graph.run("MATCH (n) RETURN n"):
#     print(res)
    # temp_str = result[1]
    #
    # search_pos = temp_str.find("^")
    # if search_pos != -1:
    #     result.append([-1, search_pos, -1])
    # elif

time_end = datetime.now()

print("time:", time_end - time_begin)
