import xml.etree.ElementTree as et

iters = et.parse("fasta2.xml").getroot().find(
    'BlastOutput_iterations').findall('Iteration')

for item in iters:
    hits = item.find('Iteration_hits').find('Hit')
    result = hits.find('Hit_hsps').find('Hsp').find('Hsp_hseq')
    print(result.text)
    print(hits.find('Hit_def').text)
