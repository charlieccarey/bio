from __future__ import print_function
import sys


def filter_blastoutfmt6_file_to_min_match_len(outfmt6_fname, mlen):
    """
    ARGS:
        outfmt6_fname: blast results in outformat6.
        mlen: minimum length of a match to get reported.
    
    RETURNS: a generator of filtered lines at given minumum match length.
    
    DETAILS:
        outfmt6 has columns
            'qseqid sseqid pident length mismatch gapopen qstart qend sstart send
             evalue bitscore'
    """
    with open(outfmt6_fname) as f:
        for r in f.readlines():
            s = r.split()
            if int(s[3]) >= mlen:
                yield r.rstrip()

def filter_and_report(blast_file, match_len):
    blast_recs = filter_blastoutfmt6_file_to_min_match_len(blast_file, match_len)
    for br in blast_recs:
        print(br)

def main():
    """
    Filters blast outfmt6 by minimum length.
    
    
    note: bed files are 0 indexed and sliced like python files.
          (http://genome.ucsc.edu/FAQ/FAQformat#format1)
    
    Input file format is like this:
    
        
        'qseqid sseqid pident length mismatch gapopen qstart qend sstart send
         evalue bitscore'
    
    
        MISEQ06:19:000000000-A2P46:1:1101:12917:2737#AGCGATGCCTT;size=18027;	Nag2FF85group_Whyrligig_cloneBW303	100.00	253	0	0	1	253	473	725	1e-130	 457
    
    Usage:
        
        filter to a minimum length of match of 150 bp
        
        python ./filter_blast_outfmt6.py blastoutfmt6.txt 150
    
    TODO: add filtering by e-value
    """
    # For each range in the bed file, extract the corresponding range from the
    # fasta file and write the results to a new fasta file. Doing this a single
    # chromosome at a time. 
    # TODO: (Why single chromosomes? Is this simply to avoid
    # TODO:  loading large chromosomes we do not need or something?)

    blast_file, match_len = sys.argv[1:3]
    filter_and_report(blast_file, int(match_len))
    exit(0)

if __name__ == '__main__':
    sys.exit(main())
