from __future__ import print_function
import sys
import csv
from collections import namedtuple
from collections import OrderedDict

def read_blast_recs(outfmt6_fname):
    """
    ARGS:
        outfmt6_fname: blast results in outformat6.

    RETURNS: a list of blast records as named tuples

    DETAILS:
        outfmt6 has columns
            'qseqid sseqid pident length mismatch gapopen qstart qend sstart send
             evalue bitscore'
    """
    blast_rec = namedtuple('blast_fmt6_rec', 'qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore')
    blast_recs = []
    with open(outfmt6_fname) as f:
        reader = csv.reader(f, delimiter='\t')
        for r in reader:
            r = [field.strip() for field in r]
            br = blast_rec._make(r)
            blast_recs.append(br)
    return(blast_recs)

def get_set(blast_recs):
    # given list of blast_recs, give all the unique sseqids
    pass

def get_best(blast_recs):
    # given list of blast_recs, give single best sseqid and eval
    pass

def get_best_blast_recs(blast_recs):
    """
    Returns the best blast rec for each query id. Results are ordered
    according to the first encounter of the query in the blast_recs.

    Bitscore disambiguates equally good evalues. Can't go by
    bitscore alone because e-value is from combined bitscore of all
    high scoring fragments.

    (So, say 2 forward matches and 1 reverse are present, the 2
    forwards get a single e-value, but separate bitscores. Each of
    the single bitscores may be lower than the reverse hit, but the
    e-value is higher than the reverse hit. So we need the e-value
    which considers all high scoring pairs (on same strand).
    """
    # Note: The elif has no effect on undisturbed blast results due to
    # the ordering of the blast results by highest e-value then
    # bitscore. The elif makes the solution stable to unordered blast
    # results.
    best_d = OrderedDict()
    for b in blast_recs:
        if not b.qseqid in best_d:
            best_d[b.qseqid] = b
        #    print('.....{} {}'.format(b[0:2], b[10:]))
        elif float(b.evalue) < float(best_d[b.qseqid].evalue):
            best_d[b.qseqid] = b
        #     print('>>>>>{} {}'.format(b[0:2], b[10:]))
        elif ( float(b.evalue) == float(best_d[b.qseqid].evalue) and
               float(b.bitscore) > float(best_d[b.qseqid].bitscore) ):
            best_d[b.qseqid] = b
        #     print('->->-{} {}'.format(b[0:2], b[10:]))
        # else:
        #     print('<<<<<{} {}'.format(b[0:2], b[10:]))
    return(best_d.values())

def get_best_blast_rec(blast_recs):
    """
    Returns blast hit with best e-value and best bitscore.
    """
    best = blast_recs[0]
    for b in blast_recs:
        if float(b.evalue) < float(best.evalue) :
             best = b
        elif ( float(b.evalue) == float(best.evalue) and
               float(b.bitscore) > float(best.bitscore) ):
            best = b
    return(best)

def print_blast_rec(blast_rec):
    """
    blast_recs: a list of blast_recs where blast_recs are named tuples
    from outfmt6 formatted blast results.
    """
    br = blast_rec
    strand = '+'
    if br.qend < br.qstart:
        strand = '-'
    print('{}\t{}\t{}\t{}'.format(br.qseqid, br.sseqid, br.evalue, br.bitscore, strand))

def print_blast_recs(blast_recs):
    """
    blast_recs: a list of blast_recs where blast_recs are named tuples
    from outfmt6 formatted blast results.
    """
    for br in blast_recs:
        print_blast_rec(br)

def main(argv=None):
    """
    Summarizes blast record to best e-val and sseqids hit.

    Input file format is like this:

        'qseqid sseqid pident length mismatch gapopen qstart qend sstart send
         evalue bitscore'

        MISEQ06:19:000000000-A2P46:1:1101:12917:2737#AGCGATGCCTT;size=18027;	Nag2FF85group_Whyrligig_cloneBW303	100.00	253	0	0	1	253	473	725	1e-130	 457

    Usage:

        python ./blast_fmt6_summary.py blastoutfmt6.txt
    """
    if argv is None:
        argv = sys.argv[1:]
    blast_files = argv

    # for each input file get all the recs then filter
    # to only the best recs per transcript
    # then filter to only the best rec of all transcripts

    all_blast_recs = OrderedDict()
    for f in blast_files:
        all_blast_recs[f] = read_blast_recs(f)

    best_recs = OrderedDict()
    for f in all_blast_recs:
        best_recs[f] = get_best_blast_recs(all_blast_recs.get(f))

    # for f in all_blast_recs:
    #     print_blast_recs(all_blast_recs[f])

    for f in all_blast_recs:
        print_blast_recs(best_recs[f])

    # for f in best_recs:
    #     best_blast_rec = get_best_blast_rec(best_recs.get(f))

    # print(best_blast_rec)

    for f in all_blast_recs:
        best_blast_rec = get_best_blast_rec(all_blast_recs.get(f))

    print(best_blast_rec)
    print_blast_rec(best_blast_rec)



    # for f in all_blast_recs:
    #     best_recs = get_best_blast_recs(all_blast_recs.get(f))
    #     print_blast_recs(best_recs)


    # get the single best

    exit(0)

if __name__ == '__main__':
    sys.exit(main())
