from __future__ import print_function
import os
import sys
import subprocess
import argparse
import textwrap
import logging
from Bio import SeqIO

logger = logging.getLogger(__name__)

def get_parser():
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = 'Blasts sequences possibly one at a time, possibly various formats.',
        epilog = textwrap.dedent('''\
        blast_html_multi_fasta_as_single_fasta.py -task tblastn -db nucl_db -query possibly_multi_fasta_prots -odir outdir
        '''))
    parser.add_argument('-task',
                        type=str,
                        dest='task',
                        default='tblastn',
                        help='''
                        for now just tblastn.
                        ''')
    parser.add_argument('-db',
                        type=str,
                        dest='db',
                        required=True,
                        help= '''
                        database name.
                        ''')
    parser.add_argument('-max_target_seqs',
                        type=str,
                        dest='max_target_seqs',
                        help= '''
                        Max number of sequences in db to try to return.
                        ''')
    parser.add_argument('-other_switches',
                        type=str,
                        dest='other_switches',
                        help= '''
                        Optionally specify other switches (and values)
                        to use.
                        ''')
    parser.add_argument('-query',
                        type=str,
                        dest='query',
                        required=True,
                        help='''
                        query: fasta file with one or more sequences
                        ''')
    parser.add_argument('-outdir',
                        type=str,
                        dest='outdir',
                        help='''
                        results go to this directory, possibly
                        creating the directory.
                        ''')
    parser.add_argument('-outname',
                        type=str,
                        dest='outname',
                        default='blast_result',
                        help='''
                        results go here.
                        ''')
    parser.add_argument('-outfmt',
                        type=str,
                        dest='outfmt',
                        default='html',
                        help='''
                        outfmt: 5=xml 6=tsv 11=blast html=html
                        ''')
    parser.add_argument('-num_threads',
                        type=str,
                        dest='num_threads',
                        default='6',
                        help='''
                        Number of threads to run ncbi programs. (default 6).
                        ''')
    return parser

def get_seqs(fasta_fname):
    '''
    Access individual seqs to do stuff with them.
    '''
    return SeqIO.parse(fasta_fname, 'fasta')

def try_blast(blastcmd):
    logger.info(' '.join(blastcmd))
    try:
        r = subprocess.check_output(blastcmd)
    except subprocess.CalledProcessError, e:
        logger.error('Error in blast:')
        logger.error(e)

def tblastn(cmd, query):
    '''
    tblastn a single fasta query getting html file named after the query.
    '''
    cmd = ['tblastn'] + ['-query', query] + cmd
    try_blast(cmd)

def set_out_dir(args):
    if args.outdir is not None:
        try:
            os.makedirs(args.outdir)
        except OSError:
            if not os.path.isdir(args.outdir):
                raise

def blastcmdcommon(args):
    '''
    Builds part of command that we almost always will use.
    '''
    cmd = ['-db', args.db]
    if args.max_target_seqs is not None:
        cmd = cmd + ['-max_target_seqs', args.max_target_seqs]
    if args.num_threads is not None:
        cmd = cmd + ['-num_threads', args.num_threads]
    return cmd

def set_outloc(args, query_name):
    if args.outdir is not None:
        set_out_dir(args)
        oloc = ['-out', os.path.join(args.outdir, query_name)]
    else:
        oloc = ['-out', query_name]
    return oloc

def set_common_command(args, query_name=None):
    '''
    builds part of the command (especially for output names).
    '''
    cmd = blastcmdcommon(args)
    if args.outfmt == 'html':
        outloc = set_outloc(args, query_name + '.html')
        cmd = cmd + ['-html'] + outloc
    else:
        if args.outfmt == '5':
            ext = '.xml'
        elif args.outfmt == '6':
            ext = '.tsv'
        elif args.outfmt == '11':
            ext = '.blast'
        outloc = set_outloc(args, query_name + ext)
        cmd = cmd + ['-outfmt', args.outfmt] + outloc
    return cmd

def do_tblastn(argv):
    parser = get_parser()
    args = parser.parse_args(argv)
    cmd = set_common_command(args, args.outname)
    tblastn(cmd, query=args.query)

def main(argv=None):
    '''
    tblastn search. Retrun one result file.
    '''
    logging.basicConfig(level=logging.INFO)
    if argv is None:
        argv = sys.argv[1:]
    do_blastn(argv)
    parser = get_parser()
    args = parser.parse_args(argv)

    # queries = get_seqs(args.query) # ex. if we wanted to blast to
                                     # individual results for each
                                     # input sequence
    cmd = set_common_command(args, args.outname)
    tblastn(cmd, query=args.query)
    return(0)


if __name__=='__main__':
    sys.exit(main())
