#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 13:10:39 2021

@author: hectorlorente
"""


import os
import sys
import urllib
import re
import argparse
import csv
import subprocess
from Bio.Align.Applications import MafftCommandline
from class_list_files import list_files

##Arguments
parser = argparse.ArgumentParser(description='Translates sequences.')
parser.add_argument('--genome', help='extract unique hits from genome data stored at genome folder or specify genome type if using --directory argument.', nargs='?', const='genome', type=str)
parser.add_argument('--rna', help='extract unique hits from rna data stored at Rna folder or specify genome type if using --directory argument.', nargs='?', const='rna', type=str)
parser.add_argument('--directory', help='path to custom folder', type=str)
parser.add_argument('--genetic_code', help='Default 1 -Standard. Look below for the number of other genetic codes.', nargs='?', type=int, default=1)
parser.add_argument('--pattern', help='custom pattern to find files for translation. Defaul "_final.fas" and "RAW.fas" as backup.', nargs='?', default='final.fas', const='final.fas', type=str)
parser.add_argument('--out_exten', help= 'extension of the output file. Default "_transtaled.fas".', nargs='?', type=str, default='_transtaled.fas')
args = parser.parse_args()
genome = args.genome
rna = args.rna
directory = args.directory
genetic_code = args.genetic_code
pattern = args.pattern
out_exten = args.out_exten
path = os.getcwd()
data_type_lst=[genome, rna]


codes = {1:
#Code: 1 Standard
{"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "X","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},
#Code: 2 Vertebrate Mitochondrial
2:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "X","AGC" : "S","AGG" : "X","AGT" : "S",
"ATA" : "M","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "W","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 3 Yeast Mitochondrial
3:{


"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "M","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "T","CTC" : "T","CTG" : "T","CTT" : "T",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "W","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 4 Mold Mitochondrial, Protozoan Mitochondrial, Coelenterate Mitochondrial, Mycoplasma, Spiroplasma
4:{


"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "W","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 5 Invertebrate Mitochondrial
5:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "S","AGC" : "S","AGG" : "S","AGT" : "S",
"ATA" : "M","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "W","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 6 Ciliate Nuclear, Dasycladacean Nuclear, Hexamita Nuclear
6:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "Q","TAC" : "Y","TAG" : "Q","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "X","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 7 Echinoderm Mitochondrial, Flatworm Mitochondrial
7:{

"AAA" : "N","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "S","AGC" : "S","AGG" : "S","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "W","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 8 Euplotid Nuclear
8:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "C","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 9 Bacterial and Plant Plastid
9:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "X","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 10 Alternative Yeast Nuclear
10:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "S","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "X","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 11 Ascidian Mitochondrial
11:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "G","AGC" : "S","AGG" : "G","AGT" : "S",
"ATA" : "M","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "W","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 12 Alternative Flatworm Mitochondrial
12:{

"AAA" : "N","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "S","AGC" : "S","AGG" : "S","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "Y","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "W","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 13 Blepharisma Macronuclear
13:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "Q","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "X","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 14 Chlorophycean Mitochondrial
14:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "L","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "X","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 15 Trematode Mitochondrial
15:{

"AAA" : "N","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "S","AGC" : "S","AGG" : "S","AGT" : "S",
"ATA" : "M","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "W","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 16 Scenedesmus obliquus Mitochondrial
16:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "L","TAT" : "Y",
"TCA" : "X","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "X","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "L","TTC" : "F","TTG" : "L","TTT" : "F",
},

#Code: 17 Thraustochytrium Mitochondrial
17:{

"AAA" : "K","AAC" : "N","AAG" : "K","AAT" : "N",
"ACA" : "T","ACC" : "T","ACG" : "T","ACT" : "T",
"AGA" : "R","AGC" : "S","AGG" : "R","AGT" : "S",
"ATA" : "I","ATC" : "I","ATG" : "M","ATT" : "I",
"CAA" : "Q","CAC" : "H","CAG" : "Q","CAT" : "H",
"CCA" : "P","CCC" : "P","CCG" : "P","CCT" : "P",
"CGA" : "R","CGC" : "R","CGG" : "R","CGT" : "R",
"CTA" : "L","CTC" : "L","CTG" : "L","CTT" : "L",
"GAA" : "E","GAC" : "D","GAG" : "E","GAT" : "D",
"GCA" : "A","GCC" : "A","GCG" : "A","GCT" : "A",
"GGA" : "G","GGC" : "G","GGG" : "G","GGT" : "G",
"GTA" : "V","GTC" : "V","GTG" : "V","GTT" : "V",
"TAA" : "X","TAC" : "Y","TAG" : "X","TAT" : "Y",
"TCA" : "S","TCC" : "S","TCG" : "S","TCT" : "S",
"TGA" : "X","TGC" : "C","TGG" : "W","TGT" : "C",
"TTA" : "X","TTC" : "F","TTG" : "L","TTT" : "F",
}}

def select_files(path):
    return list_files.list_files_method(list_files,path)

def get_files(path, pattern):
    files = []
    for folder in select_files(path):
        try:
            found = False
            for i in range(len(folder[1])):
                file = re.search('(.*)' + pattern + '.*', folder[1][i])
                if file and (not re.search('.gz', file.group())):
                    found = True
                    in_file = re.sub('\\\\', '/', file.group())
                    files.append(in_file)
            if not found:
                for i in range(len(folder[1])):
                    file = re.search('(.*)RAW.fas', folder[1][i])
                    if file and (not re.search('.gz', file.group())):
                        in_file = re.sub('\\\\', '/', file.group())
                        files.append(in_file)
        except IndexError:
            continue
    return files

def read_FASTA_strings(fasta_input_file):
    with open(fasta_input_file) as file:
        return file.read().split('>')[1:]
def read_FASTA_entries(fasta_input_file):
    return [seq.partition('\n') for seq in read_FASTA_strings(fasta_input_file)]
def read_FASTA_sequences(fasta_input_file):
    return[[info,
            seq.replace('\n', "")]
            for info, ignore, seq in read_FASTA_entries(fasta_input_file)]

def translate_RNA_codon(codon):
    return codes[genetic_code][codon]


def codons_translation(codon):
    """Generate a random list of codons between minlength and maxlength, inclusive"""
    try:
        aa_codon = translate_RNA_codon(codon.upper())
    except KeyError:
        aa_codon = "*"
    return aa_codon

def AA_seq_creator(filename):
    """Return a list object that produces an amino acid by translating
    the next three characters of rnaseq each time next is called on it"""
    nu_seqs = read_FASTA_sequences(filename)
    aa_seqs = []
    for seq in nu_seqs:
        aa_seq = str()
        for n in range(0, len(seq[1]), 3):
            aa_seq += codons_translation(seq[1][n:n+3])   
        aa_seqs.append([seq[0],aa_seq])
    return aa_seqs

def translate_sequences_all_sequences(path, data_type):
    files_lst = get_files(path, pattern)
    for filename in files_lst:
        with open(re.sub('\.f.*', out_exten, filename), "w") as file:
            for seq in AA_seq_creator(filename):
                file.write('>')
                file.write(seq[0])
                file.write('\n')
                file.write(seq[1])
                file.write('\n')

if genetic_code in range(1,18):
    if directory is not None:
        for data_type in data_type_lst:
            print('INFO. Running directory and %s argument.\n' %data_type)
            translate_sequences_all_sequences(directory+'/*', data_type)
    else:
        found = False
        for data_type in data_type_lst:
            if data_type is not None:
                found = True
                print('INFO. Running %s argument.\n' %data_type)
                translate_sequences_all_sequences(path+'/../Data/'+ data_type.capitalize()+'/*', data_type)
        if not found:
            print('ERROR. You must use genomic, rna or directory arguments.')
else:
     print('ERROR. Genetic code argument must be between 1 and 17. See README file for more info.')

