import xml.etree.ElementTree as et

root = et.parse("test.xml").getroot()
stats = root.find('BlastOutput_iterations').find(
    'Iteration').find('Iteration_stat')
print(stats.text)
