import xml.etree.ElementTree as et
import re
import blast
import sys

CHUNK = 10


def main():
    target = sys.stdin.read()
    chunk = target[:CHUNK]
    blast.blast_n(chunk, 'fasta.xml', 'AWRI1631_ABSV01000000_cds.fsa')


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


def gene_search(seq, pat, end=0):
    results = []
    if end != 0:
        seq = seq[:end+1]
    pat = re.compile(pat)
    return len(pat.findall(seq))


def iterate(src, dst):
    ''' 
    Returns index of last letter before cut in genome should be made,
    returns None of either string hits the end. 
    '''
    base_pairs = 0
    wrong_pairs = 0
    bp_threshold = 5
    error_threshold = 0.25

    for x, y in zip(src, dst):
        base_pairs += 1
        if x != y:
            wrong_pairs += 1
            if (base_pairs >= bp_threshold and
                    wrong_pairs / base_pairs >= error_threshold):
                return base_pairs - 1
    return None


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


if __name__ == "__main__":
    main()
