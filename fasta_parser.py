
def fasta_parse(seq_id, fasta_path):
    with open(fasta_path, 'r') as fasta_file:
        fasta_str = fasta_file.read()
        fasta_file.close()

    fasta_entries = fasta_str.split('\n>')
    entry_str = [entry for entry in fasta_entries if seq_id in entry][0]

    seq_lines = entry_str.split('\n')
    entry_seq = "".join(seq_lines)

    return entry_seq
