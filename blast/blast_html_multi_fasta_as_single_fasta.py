from __future__ import print_function
import os
import sys
import logging
import charcar.blast.blast_helper as bh
from Bio import SeqIO

logger = logging.getLogger(__name__)

def multi_as_single_fasta_blasts(argv):
    parser = bh.get_parser()
    args = parser.parse_args(argv)
    queries = bh.get_seqs(args.query)
    for q in list(queries):
        with open("temp.fasta", "w") as f:
            SeqIO.write(q, f, "fasta")
        qname = q.id
        qname = q.id.replace('lcl|', '')
        cmd = bh.set_common_command(args, query_name=qname)
        print('Running  with parameters: {}'.format(' '.join(cmd)))
        bh.tblastn(cmd, query='temp.fasta')
        os.remove('temp.fasta')

def main(argv=None):
    '''
    For each sequence in query file do a tblastn search.
    '''
    logging.basicConfig(level=logging.INFO)
    if argv is None:
        argv = sys.argv[1:]
    multi_as_single_fasta_blasts(argv)
    return(0)
    # logging.basicConfig(level=logging.INFO)
    # if argv is None:
    #     argv = sys.argv[1:]
    # parser = bh.get_parser()
    # args = parser.parse_args(argv)
    # queries = bh.get_seqs(args.query)
    # for q in list(queries):
    #     with open("temp.fasta", "w") as f:
    #         SeqIO.write(q, f, "fasta")
    #     qname = q.id
    #     qname = q.id.replace('lcl|', '')
    #     cmd = bh.set_common_command(args, query_name=qname)
    #     print('Running  with parameters: {}'.format(' '.join(cmd)))
    #     bh.tblastn(cmd, query='temp.fasta')
    #     os.remove('temp.fasta')
    # return(0)

if __name__=='__main__':
    sys.exit(main())
