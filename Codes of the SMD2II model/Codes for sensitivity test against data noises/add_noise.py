# Valentin Mace
# valentin.mace@kedgebs.com
# Developed at Qwant Research

"""Main script to add noise to your corpus"""
import json
import os
import argparse

from noise_functions import *
from tqdm import tqdm
from utils import *
from RandomEdit import *

parser = argparse.ArgumentParser()
parser.add_argument('input',
                    help="The text file you want to add noise to")
parser.add_argument('--output', default=None,
                    help="Optional, the name you want to give to your output, default=yourfilename.noisy")
parser.add_argument('--progress', action='store_true',
                    help="Optional, show the progress")
parser.add_argument('--delete_probability', default=0.1, type=float,
                    help="Optional, the probability to remove each token, default=0.1")
parser.add_argument('--replace_probability', default=0.1, type=float,
                    help="Optional, the probability to replace each token with a filler token, default=0.1")
parser.add_argument('--permutation_range', default=3, type=int,
                    help="Optional, Max range for token permutation, default=3")
parser.add_argument('--filler_token', default='BLANK',
                    help="Optional, token to use for replacement function, default=BLANK")
def del_bookname(entity_name):
    """delete the book name"""
    if entity_name.startswith(u'《') and entity_name.endswith(u'》'):
        entity_name = entity_name[1:-1]
    return entity_name
def load_result(predict_filename):
    result_dict = {}
    with open(predict_filename) as gf:

        for line in gf:
            unchanged_words = []
            json_info = json.loads(line)
            sent = json_info['text']
            #print(sent)
            spo_list = json_info['spo_list']
            spo_result = []
            for item in spo_list:
                if type(item['object'])==list and type(item['subject'])==list:
                    o=del_bookname(' '.join(item['object']).lower())
                    s = del_bookname(' '.join(item['subject']).lower())
                elif type(item['object'])==list and type(item['subject'])!=list:
                    o = del_bookname(' '.join(item['object']).lower())
                    s = del_bookname(item['subject'].lower())
                elif type(item['object'])!=list and type(item['subject'])==list:
                    o = del_bookname(item['object'].lower())
                    s = del_bookname(' '.join(item['subject']).lower())
                else:
                    o = del_bookname(item['object'].lower())
                    s = del_bookname(item['subject'].lower())
                spo_result.append((s, item['predicate'], o))
                unchanged_words.append(s)
                unchanged_words.append(o)
            spo_result = set(spo_result)
            result_dict[sent] = spo_result
        print("unchanged_words",unchanged_words)
    return result_dict

def process_line(line):
    unchanged_words = []
    json_info = json.loads(line)
    sent = json_info['text']
    #print(sent)
    spo_list = json_info['spo_list']
    spo_result = []
    for item in spo_list:
        if type(item['object']) == list and type(item['subject']) == list:
            o = del_bookname(' '.join(item['object']).lower())
            s = del_bookname(' '.join(item['subject']).lower())
        elif type(item['object']) == list and type(item['subject']) != list:
            o = del_bookname(' '.join(item['object']).lower())
            s = del_bookname(item['subject'].lower())
        elif type(item['object']) != list and type(item['subject']) == list:
            o = del_bookname(item['object'].lower())
            s = del_bookname(' '.join(item['subject']).lower())
        else:
            o = del_bookname(item['object'].lower())
            s = del_bookname(item['subject'].lower())
        spo_result.append((s, item['predicate'], o))
        unchanged_words.append(s)
        unchanged_words.append(o)
    spo_result = set(spo_result)
    result_dict[sent] = spo_result
    return sent, unchanged_words

#print("unchanged_words", unchanged_words)



def check_unchanged_words(line,unchanged_words):
    line_origin=line
    no_error = 0
    for i in unchanged_words:

        if i not in line:
            no_error = +1
            #print("i不在line",i,line_origin)
        #print("i在line", i, line_origin)
    return no_error

def delete_random_token_no_unchanged_words(line,delete_probability):
    line_origin=line
    line2 = delete_random_words(line, probability=delete_probability)
    if check_unchanged_words(line2,unchanged_words)==0:
        line=line2

    return line


def replace_random_toke_no_unchanged_words(line,replace_probability):
    line_origin = line
    line2 = replace_random_words(line, probability=replace_probability)
    if check_unchanged_words(line2,unchanged_words)==0:
        #print("replace words")
        line = line2

    return line

def insert_random_toke_no_unchanged_words(line,replace_probability):
    line_origin = line
    line2 = insert_random_words(line, probability=replace_probability)
    if check_unchanged_words(line2,unchanged_words)==0:
        #print("replace words")
        line = line2

    return line

def random_token_permutation_no_unchanged_words(line,permutation_range):
    line_origin = line
    line2 = random_token_permutation(line, permutation_range)

    if check_unchanged_words(line2,unchanged_words)==0:
        line = line2

    return line

golden_dict= r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\raw_data\test1_data_postag.json"
#print ("golden_dict",golden_dict)

if __name__ == '__main__':
    result_dict = {}
    i=0
    n=0
    delete_probability=0.1
    replace_probability=0.1
    insert_probability=0.1
    permutation_range=3
    with open(golden_dict) as gf,open(r"D:\Downloads\noisy-text-master\noisy-text-master\output.txt", 'w') as output:
        for line in gf:
            i=i+1
            tweet,unchanged_words=process_line(line)
            tweet_with_noise=delete_random_token_no_unchanged_words(tweet,delete_probability)
            tweet_with_noise=replace_random_toke_no_unchanged_words(tweet_with_noise,replace_probability)
            tweet_with_noise=insert_random_toke_no_unchanged_words(tweet_with_noise,insert_probability)
            tweet_with_noise=random_token_permutation_no_unchanged_words(tweet_with_noise,delete_probability)
            #print(tweet_with_noise)
            while tweet_with_noise == tweet:

                #print(tweet_with_noise,"\n",tweet)
                tweet_with_noise = delete_random_token_no_unchanged_words(tweet, delete_probability)
                tweet_with_noise = replace_random_toke_no_unchanged_words(tweet_with_noise, replace_probability)
                tweet_with_noise = insert_random_toke_no_unchanged_words(tweet_with_noise, insert_probability)
                tweet_with_noise = random_token_permutation_no_unchanged_words(tweet_with_noise, delete_probability)
            if  tweet_with_noise != tweet:
                n = n + 1
            #print(i)
            output.write(tweet_with_noise + '\n')
    print("added",n)



