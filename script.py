import os

def openCDS(filepath):
    with open(filepath) as f:
        lines = f.readlines()
        data = []
        gene = {'description':'', 'sequence':''}
        for line in lines:
            if line[0] == '>' and gene['description'] != '':
                data.append(gene)
                gene = {'description':'', 'sequence':''}
            if line[0] == '>' and gene['description'] == '':
                gene['description'] = line[:-1]
            else:
                gene['sequence'] += line[:-1]
        data.append(gene)
        lines = []
    
    return data

human_cds = openCDS('human_GCF_000001405.39/cds_from_genomic.fna')
mouse_cds = openCDS('mouse_GCF_000001635.27/cds_from_genomic.fna')
elephant_cds = openCDS('elephant_GCF_000001905.1/cds_from_genomic.fna')
bluewhale_cds = openCDS('bluewhale_GCF_009873245.2/cds_from_genomic.fna')
nakedmolerat_cds = openCDS('nakedmolerat_GCF_000247695.1/cds_from_genomic.fna')

import subprocess
from xml.dom.minidom import parse, parseString

def parseResults(results):
    doc = parseString(results)
    return len(doc.getElementsByTagName('Hit'))

def blastSeqDuplicates(sequence, genome):
    with open(f'query{genome}.fasta', 'w') as file:
        file.write('> Query\n')
        file.write(sequence)
    results = subprocess.check_output([
        '/usr/local/ncbi/blast/bin/blastn',
        '-db',
        f'databases/{genome}',
        '-query',
        f'/Users/jingluo/GitHub/biopython/query{genome}.fasta',
        '-evalue',
        '0.05',
        '-word_size',
        '28',
        '-outfmt',
        '5'
    ])
    return parseResults(results)

import sys

refGenome = sys.argv[1]
print(refGenome)
for cds in human_cds:
    description = cds['description']
    sequence = cds['sequence']
    duplicates = blastSeqDuplicates(sequence, refGenome)
    with open(f'{refGenome}.txt', 'a') as file:
        file.write(f'{description}==={duplicates}\n')