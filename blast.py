import subprocess


def create_blast_database(fasta_str, save_path):
    """

    :param fasta_str:
    :param save_path:
    :return:
    """
    with open(save_path + 'fasta.txt', 'w') as f:
        f.write(fasta_str)
        f.close()
    database_filename = save_path + '_database'

    # creation of the makeblastdb command line
    makeblastdb_cline = subprocess.Popen(['C:/Users/Christian/Desktop/RESearch/ncbi-blast-2.7.1+/bin/makeblastdb.exe',
                                          '-in', save_path + 'fasta.txt', '-parse_seqids', '-dbtype', 'nucl', '-out',
                                          database_filename], stdout=subprocess.PIPE)

    # calls the makeblastdb command line and cleans up unnecessary files
    makeblastdb_cline.communicate()

    return database_filename


def blast_n(fasta_str, save_path, database_filename):
    """

    :param fasta_str:
    :param save_path:
    :param database_filename:
    :return:
    """
    with open(save_path, 'w') as f:
        f.write(fasta_str)
        f.close()

    # generate unique filename for query
    blast_output_file_path = save_path[:-4] + '.xml'

    print(blast_output_file_path)
    print(save_path)

    # creation of the blast command line
    blastp_cline = subprocess.Popen(['C:/Users/Christian/Desktop/RESearch/ncbi-blast-2.7.1+/bin/blastn.exe', '-out', blast_output_file_path, '-outfmt', '5', '-query',
                                     save_path, '-db', database_filename], stdout=subprocess.PIPE)

    # calling of the blast command line and cleans up unnecessary files
    blastp_cline.communicate()

    return blast_output_file_path
