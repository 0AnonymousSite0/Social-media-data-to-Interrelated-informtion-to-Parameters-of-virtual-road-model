#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 01:54:10 2022

@author: taha
"""

from RandomEdit import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_file', '-i', help="Path to the input text file", type=str)
parser.add_argument('--output_file', '-o', help="Path to output file", type=str)
parser.add_argument('--delete', '-d', help="Probability of deleting a word",\
                    type=float)
parser.add_argument('--insert', '-s', help="Probability of inserting a random word",\
                    type=float)   
parser.add_argument('--replace', '-r',\
                    help="Probability of replacing a word with another random word",\
                    type=float)
parser.add_argument('--permutation', '-p', help="Permuting words at the end",\
                    type=bool)
parser.add_argument('--seed', '-e', help="Random seed",\
                    type=int) 
parser.add_argument('--verbose', '-v', help="Verbose",\
                    type=bool, default=False)

args = parser.parse_args()

if args.input_file is None or args.output_file is None:
    raise Exception('Input and output files are required')

# Reade data
f = open(args.input_file, 'r')
lines = f.readlines()
f.close()

# Report
if args.delete is not None:
    if args.verbose:
        print('Delete random words with probability',args.delete)

if args.insert is not None:
    if args.verbose:
        print('Insert random words with probability',args.insert)

if args.replace is not None:
    if args.verbose:
        print('Replace random words with probability',args.replace)

if args.permutation is not None:
    if args.verbose:
        print('Perfome random permutation',args.permutation)

if args.seed is not None:
    if args.verbose:
        print('Set seed to ',args.seed)

# Seed seed for reproducibility
if args.seed is not None:
    set_seed(args.seed)

# Apply noise to each line

output_lines = []

for line in lines:

    if args.delete is not None:
        line = delete_random_words(line, args.delete)
    
    if args.insert is not None:
        line = insert_random_words(line, args.insert)
    
    if args.replace is not None:
        line = replace_random_words(line, args.replace)
    
    if args.permutation is not None:
        line = random_permutation(line)
    
    output_lines.append(line)

# Write data
f = open(args.output_file, 'w')
for line in output_lines:
    f.write(line)
    f.write('\n')
f.close()
