import xml.etree.ElementTree as et

iters = et.parse("fasta2.xml").getroot().find(
    'BlastOutput_iterations').find('Iteration')

hits = iters.find('Iteration_hits').findall('Hit')
for r in hits:
    result = r.find('Hit_hsps').find('Hsp').find('Hsp_hseq')
    print(result.text)
    print(r.find('Hit_def').text)
