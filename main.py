import xml.etree.ElementTree as et
import re
import blast
import sys

CHUNK = 10


def main():
    data = sys.stdin.read()
    chunk = data[:CHUNK]
    blast.blast_n(chunk, 'fasta.xml', 'AWRI1631_ABSV01000000_cds.fsa')
    blast_results = xml_parse()


def xml_parse():
    iters = et.parse("fasta2.xml").getroot().find(
        'BlastOutput_iterations').find('Iteration')

    hits = iters.find('Iteration_hits').findall('Hit')
    results = []
    for r in hits:
        result = r.find('Hit_hsps').find('Hsp').find('Hsp_hseq')
        gene = r.find('Hit_id').text
        results.append((gene, result.text))
    return results


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

    print(img_ba[0])

    return img_ba


if __name__ == "__main__":
    main()
