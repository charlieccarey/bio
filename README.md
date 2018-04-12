# Command line utils for common bioinformatics tasks

Tools for producing and processing blast similarity searches.

## Motivation

I wanted to make my life easier with some common bioinformatic tasks.

## Caution

Plan to use these? Please review and test them thoroughly. This 
readme is years after I wrote the scripts.

### Many many blasts, many result files.

In some extreme cases, I ran a 64 node, ~1000 CPU (~2000 hyperthreaded units) 
High Performance Computing Cluster for a month, and at other times for 
weeks (using a smaller set of nodes) at a time.

I was working on a dataset of 12 de novo transcriptomes from which we 
derived approximately 10,000,000 predicted (assembled) RNA transcripts. We had 
clustered these 10 Million sequences by read group and similarity to 
generate about 1 million clusters. I selected the longest version from 
each representative cluster and wanted to assign some function to it, 
and therefore to the cluster from which it was derived.

I wanted to assign some function or label to each of the 1,000,000 
reduced set of transcripts by blastx (compare all translations of a 
transcript to a protein) against a reference set called uniref90 having
70 million sequences. So this was a 1,000,000 against 70,000,000
comparison. 70,000,000,000,000 or 70 trillion pairwise comparisons. While 
blast uses a number of tricks to cut down on the work, this is still a 
very large computational job. 

I split up our 1,000,000 representative sequences into smaller files as sets of, 
maybe 1,000 sequences per file. So that is 1,000 files of 1,000 sequences each. 
Each file was distributed to worker nodes on the cluster, blast was ran on 2-4 CPU
cores per input file. Over several jobs like this, I generated 
1000s of such result files. Since I did not want to 
be constrained to looking at only the best hit for each input sequence, 
I preserved many of the next best hits for each input. The result files were
on the order of 500 Gb for the larger jobs. I processed these on the cluster.

As an aside, before starting these jobs I had experimentally 
determined a reasonable number of CPU cores to use (Blast can use 
multiple CPUs), while not overwhelming any one node with too much 
memory demand (to avoid memory to disk writes). The number of sequences 
per input file was largely a result of a desired output file size.

In the end, I did only want the single best hit for each of the 1,000,000
input sequences.

One or more of the scripts was used to extract these best hits.

### Manage many blasts.

Over and over, I wanted to run blast to find potential
homologs of sequences and wanted some flexibility in file 
naming and output.

Or maybe I was submitting different options to test their effect on
the quality of my results.

Some of these scripts make that easier, particularly it seemed
I was focused on tblastn.

## Defintions

Sequence: 

- Representation of biological objects composed of units of the same basic type attached together to form a
longer object with emergent function.
- Ex. A protein is represented by a series of letters, each of which refer
to the single Amino Acids from which it was composed.

Transcript:

- A transcript is an RNA copy of, most frequently, a gene. 
- In the case of protein coding genes, the gene is transcribed into mRNA transcripts. The 
transcripts are then translated into proteins. 
- A single gene can produce multiple versions of a protein and does this by producing multiple versions
of the mRNA transcripts. Most often, the different versions of the gene
occur because of differences in splicing of a primary mRNA copy of the gene.

Blast:

- Biologists are commonly interested in how one sequence relates to, 
or is similar to, another sequence.
- For example, one might be interested in homology and orthology. 
- Commonly we are interested in the most similar sequence.
- BLAST is a tool most commonly used for this purpose. Compare one 
(or more) sequence(s) to other(s) and report scores, locations 
etc. indicating how close they are together and describing other attributes.
- If the score is (possibly) worth reporting, we call it a 'hit'.

Orthology:

- If we take a sequence from one organism, if it is the best hit to a sequence 
in another organism, and vice versa, we might have found orthologs. This is 
called a 'reciprocal best hits' approach to defining orthology.
- Orthology means that the object represented by a sequence performs at 
least some of the same function in different organisms. i.e. the gene 
in one organism has a similar role as the 'same' or very similar gene 
in another organism.
- A requirement for orthology is that you have completely sequenced all the 
genes and or have all the protein representations for all proteins that occur 
in both species. If one species has only 1/2 of its genes sequenced, we can't 
say much about orthology. Nonetheless, the hits might be indicative of some 
similarity.

Uniref90:

- Collection of 71,000,000 protein sequences.
- There are several sets of reference sequences available for blast similarity
searches to help identify the possible identity and / or function of 
transcripts of unknown, or unlabeled identity.
- Uniref90 is one of these reference collections. 
- It is comprised of a representative protein 
from each of the core uniref clusters. 
- It is useful for comparison of
unknown sequences because it is very representative of all known proteins.
If your particular protein does not 'hit' one of these proteins, it is 
possibly 'space junk', an artifact of an assembly algorithm, a sequence from non-coding genomic regions, a 
contaminant from an unsequenced taxonomic branch, or potentially 
interesting (or uninteresting depending on your point of 
view and practicality) as something that only exists in the species you
are examining. 
- Most often, when working with assembled transcriptomes, we start querying 
Uniref90 not with a protein, but with a transcript that 'might' come from a protein coding gene. Doing the blast in this way is a little more 
forgiving of small deletions and insertions from the sequencing process that
would shift the reading frame of a protein. We use Blastx for such querires.
- (Such frameshifts make the protein 
very different from what it should be. At the DNA or RNA level the similarity
is preserved across most of the sequence. Blastx translates all frames, so
there is a higher likelihood of a hit, even in the presence of frameshifts.)
- The uniref90 collection in April 2018 has 71,000,000 sequences, 
representing the same number of protein clusters. 

[uniref90 release notes][ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.release_note]
