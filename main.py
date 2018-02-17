import xml.etree.ElementTree as et
import re


def xml_parse():
    iters = et.parse("fasta2.xml").getroot().find(
        'BlastOutput_iterations').find('Iteration')

    hits = iters.find('Iteration_hits').findall('Hit')
    results = []
    for r in hits:
        result = r.find('Hit_hsps').find('Hsp').find('Hsp_hseq')
        gene = r.find('Hit_def').text
        return (gene, result.text)


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
