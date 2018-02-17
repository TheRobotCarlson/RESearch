import re


def gene_search(seq, pat, end=0):
    results = []
    if end != 0:
        seq = seq[:end+1]
    pat = re.compile(pat)
    return len(pat.findall(seq))


print(gene_search('astcastgastastaaaaaaa', 'ast', 10))
