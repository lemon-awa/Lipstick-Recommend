import os
import re
import sys
from itertools import islice
from preprocess import removeSGML,tokenizeText
from Porterstemmer import PorterStemmer
from collections import defaultdict
from math import log
import math

def pre_process_all(files_list, type):
    preprocessed_data = {}
    count = 0
    for filename in files_list:
        tokens = pre_propocess(filename)
        classname = f"{type}_{count}"
        preprocessed_data[classname] = tokens
        count += 1
    return preprocessed_data

def pre_propocess(filename):
    tokens = []
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='ISO-8859-1') as file:
            for line in file:
                line = removeSGML(line)
                tokens = tokenizeText(line)
                tokens += tokens
            return tokens

def trainNaiveBayes(neg_dict, pos_dict):
    N = len(neg_dict) + len(pos_dict)
    neg_num = len(neg_dict)
    pos_num = len(pos_dict)
    vocab = set()

    word_counts = defaultdict(lambda: defaultdict(int))
    for _, tokens in pos_dict.items():
        vocab.update(tokens)
        for token in tokens:
            word_counts["pos"][token] += 1

    for _, tokens in neg_dict.items():
        vocab.update(tokens)
        for token in tokens:
            word_counts["neg"][token] += 1

    vocab_size = len(vocab)
    class_probs = {
        "pos": log(pos_num / N),
        "neg":log(neg_num / N)
    }

    word_cond_probs = defaultdict(dict)
    pos_sum = sum(word_counts["pos"].values())
    neg_sum = sum(word_counts["neg"].values())
    for cls,counts in word_counts.items():
        total_words = sum(counts.values())
        for word in vocab:
            word_cond_probs[cls][word] = log((counts[word] + 1)/(total_words + vocab_size))
    

    return class_probs,word_cond_probs,vocab_size,pos_sum,neg_sum


def predictNaiveBayes(test_tokens,class_probs,word_cond_probs,vocab_size,pos_sum,neg_sum):
    score1 = class_probs["pos"]
    score2 = class_probs["neg"]

    default_score1 = log(1/(vocab_size + pos_sum))
    default_score2 = log(1/(vocab_size + neg_sum))
    for token in test_tokens:
        score1 += word_cond_probs["pos"].get(token,default_score1)
        score2 += word_cond_probs["neg"].get(token,default_score2)

    if score1 >= score2:
        predict = "pos"
    else:
        predict = "neg"
    
    return predict

def sentimental_train():
    neg_foldname = "negdata"
    pos_foldname = "posdata"

    neg_files_list = []
    pos_files_list = []
    for filename in os.listdir(neg_foldname):
        filepath = os.path.join(neg_foldname, filename)
        neg_files_list.append(filepath)
    
    for filename in os.listdir(pos_foldname):
        filepath = os.path.join(pos_foldname, filename)
        pos_files_list.append(filepath)
    
    neg_data = pre_process_all(neg_files_list, "neg")
    pos_data = pre_process_all(pos_files_list, "pos")

    class_probs,word_cond_probs,vocab_size,pos_sum,neg_sum = trainNaiveBayes(neg_data, pos_data)
    return class_probs,word_cond_probs,vocab_size,pos_sum,neg_sum


def prepare(comment):
    line = removeSGML(comment)
    tokens = tokenizeText(line)
    stemmer = PorterStemmer()
    stemmed_tokens = []
    for token in tokens:
        stemmed_token = stemmer.stem(token,0,len(token)-1)
        stemmed_tokens.append(stemmed_token)
    return stemmed_tokens


if __name__ == "__main__":
    comment = "She doesn't need to “fake” lip filler. They look filled."
    line = removeSGML(comment)
    tokens = tokenizeText(line)
    stemmer = PorterStemmer()
    stemmed_tokens = []
    for token in tokens:
        stemmed_token = stemmer.stem(token,0,len(token)-1)
        stemmed_tokens.append(stemmed_token)

    class_probs,word_cond_probs,vocab_size,pos_sum,neg_sum = sentimental_train()
    print(predictNaiveBayes(stemmed_tokens, class_probs,word_cond_probs,vocab_size,pos_sum,neg_sum))
