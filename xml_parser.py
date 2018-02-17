import xml.etree.ElementTree as et


def xml_parse():
    iters = et.parse("fasta2.xml").getroot().find(
        'BlastOutput_iterations').find('Iteration')

    hits = iters.find('Iteration_hits').findall('Hit')
    results = []
    for r in hits:
        result = r.find('Hit_hsps').find('Hsp').find('Hsp_hseq')
        gene = r.find('Hit_def').text
        return (gene, result.text)
