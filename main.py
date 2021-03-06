import xml.etree.ElementTree as et
import re
import blast
import sys
import os
from neo4j_manager import get_enzyme
from encoder import bits_to_nucleobase, encode


def main():
    CHUNK = 10
    data = encode(png_to_binary("data_files/visitlex_logo2.png"))
    print(data)
    counter = CHUNK
    end = len(data)
    dna_str = ""
    print(counter, end, CHUNK)
    while counter < end + CHUNK:
        chunk = data[counter-CHUNK:counter]

        blast.blast_n(chunk, 'fasta.fsa', 'databases')
        print('parsing')
        results = xml_parse()
        print('parsed')

        found = False
        i = 0

        print('getting enzymes...')
        while not found and i < len(results):
            result = results[i]

            (bp_left, name_left) = get_enzyme(result.gene, result.hit_to)
            (bp_right, name_right) = get_enzyme(result.gene, result.hit_from)

            if name_left is None or name_right is None:
                i += 1
                continue
            else:
                found = True

        if found:
            print('got enzymes')
            print('Enzymes:\n  ' + name_left + '\n  ' + name_right)
            dna_str += results[i].hseq
            print(dna_str)
        else:
            print("failed to find enzymes at this time")
            break

        counter += CHUNK
    print(dna_str)
    print("WORKED: ", data == dna_str)


class Result:
    def __init__(self):
        self.hseq = None
        self.hit_from = None
        self.hit_to = None
        self.id = None
        self.gene = None


def xml_parse():
    iters = et.parse("fasta.xml").getroot().find(
        'BlastOutput_iterations').find('Iteration')

    hits = iters.find('Iteration_hits').findall('Hit')
    results = []
    for r in hits:
        res = Result()
        result = r.find('Hit_hsps').find('Hsp')
        res.hseq = result.find('Hsp_hseq').text
        res.hit_from = int(result.find('Hsp_hit-from').text)
        res.hit_to = int(result.find('Hsp_hit-to').text)
        res.id = r.find('Hit_id').text
        res.gene = fasta_parse(res.id, 'AWRI1631_ABSV01000000_cds.fsa')
        results.append(res)

    return results


def fasta_parse(seq_id, fasta_path):
    with open(fasta_path, 'r') as fasta_file:
        fasta_str = fasta_file.read()
        fasta_file.close()

    fasta_entries = fasta_str.split('\n>')
    entry_str = [entry for entry in fasta_entries if seq_id in entry][0]

    seq_lines = entry_str.split('\n')
    entry_seq = "".join(seq_lines[1:])

    return entry_seq


def cluster_enzymes(li):
    pairs = ['A^A', 'A^C', 'A^G', 'A^T', 'C^A', 'C^C', 'C^G', 'C^T',
             'G^A', 'G^C', 'G^G', 'G^T', 'T^A', 'T^C', 'T^G', 'T^T']
    ends = ['A^', 'C^', 'G^', 'T^']
    starts = ['^A', '^C', '^G', '^T']
    d = {}
    for pair in pairs:
        d[pair] = []
    for s in starts:
        d[s] = []
    for e in ends:
        d[e] = []
    for enzyme in li:
        enzyme = enzyme['pattern']
        for pair in pairs:
            if pair in enzyme:
                d[pair].append(enzyme)
                break
        for start in starts:
            if enzyme.startswith(start):
                d[start].append(enzyme)
                break
        for end in ends:
            if enzyme.endswith(end):
                d[end].append(enzyme)
                break
    return d


def png_to_binary(img_path):
    with open(img_path, 'rb') as img_f:
        img = img_f.read()
        img_ba = bytes(img)

    # print(img_ba[0])

    return img_ba


def prRed(skk): print("\033[91m {}\033[00m" .format(skk), end='')


def prGreen(skk): print("\033[92m {}\033[00m" .format(skk), end='')


def prYellow(skk): print("\033[93m {}\033[00m" .format(skk), end='')


def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk), end='')


def prPurple(skk): print("\033[95m {}\033[00m" .format(skk), end='')


def prCyan(skk): print("\033[96m {}\033[00m" .format(skk), end='')


def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk), end='')


def prBlack(skk): print("\033[98m {}\033[00m" .format(skk), end='')


if __name__ == "__main__":
    main()
