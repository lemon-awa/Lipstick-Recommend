# Ziyang Xiong    xziyang
import os
import re
from collections import defaultdict
import collections
import sys

def removeSGML(input):
    clean_text = re.sub(r'<.*?>','',input)
    return clean_text

# def tokenizeText(input):
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(input)
#     tokens = [token.text for token in doc if not token.is_punct and not token.is_space]
#     return tokens

def expand_contractions(text):
    contractions = {
        "I'm": "I am",
        "I'm'a": "I am about to",
        "I'm'o": "I am going to",
        "I've": "I have",
        "I'll": "I will",
        "I'll've": "I will have",
        "I'd": "I would",
        "I'd've": "I would have",
        "Whatcha": "What are you",
        "amn't": "am not",
        "ain't": "are not",
        "aren't": "are not",
        "'cause": "because",
        "can't": "cannot",
        "can't've": "cannot have",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "daren't": "dare not",
        "daresn't": "dare not",
        "dasn't": "dare not",
        "didn't": "did not",
        "didn’t": "did not",
        "don't": "do not",
        "don’t": "do not",
        "doesn't": "does not",
        "e'er": "ever",
        "everyone's": "everyone is",
        "finna": "fixing to",
        "gimme": "give me",
        "gon't": "go not",
        "gonna": "going to",
        "gotta": "got to",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he've": "he have",
        "he's": "he is",
        "he'll": "he will",
        "he'll've": "he will have",
        "he'd": "he would",
        "he'd've": "he would have",
        "here's": "here is",
        "how're": "how are",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how's": "how is",
        "how'll": "how will",
        "isn't": "is not",
        "it's": "it is",
        "'tis": "it is",
        "'twas": "it was",
        "it'll": "it will",
        "it'll've": "it will have",
        "it'd": "it would",
        "it'd've": "it would have",
        "kinda": "kind of",
        "let's": "let us",
        "luv": "love",
        "ma'am": "madam",
        "may've": "may have",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "ne'er": "never",
        "o'": "of",
        "o'clock": "of the clock",
        "ol'": "old",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "o'er": "over",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shalln't": "shall not",
        "shan't've": "shall not have",
        "she's": "she is",
        "she'll": "she will",
        "she'd": "she would",
        "she'd've": "she would have",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so is",
        "somebody's": "somebody is",
        "someone's": "someone is",
        "something's": "something is",
        "sux": "sucks",
        "that're": "that are",
        "that's": "that is",
        "that'll": "that will",
        "that'd": "that would",
        "that'd've": "that would have",
        "'em": "them",
        "there're": "there are",
        "there's": "there is",
        "there'll": "there will",
        "there'd": "there would",
        "there'd've": "there would have",
        "these're": "these are",
        "they're": "they are",
        "they've": "they have",
        "they'll": "they will",
        "they'll've": "they will have",
        "they'd": "they would",
        "they'd've": "they would have",
        "this's": "this is",
        "this'll": "this will",
        "this'd": "this would",
        "those're": "those are",
        "to've": "to have",
        "wanna": "want to",
        "wasn't": "was not",
        "we're": "we are",
        "we've": "we have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we'd": "we would",
        "we'd've": "we would have",
        "weren't": "were not",
        "what're": "what are",
        "what'd": "what did",
        "what've": "what have",
        "what's": "what is",
        "what'll": "what will",
        "what'll've": "what will have",
        "when've": "when have",
        "when's": "when is",
        "where're": "where are",
        "where'd": "where did",
        "where've": "where have",
        "where's": "where is",
        "which's": "which is",
        "who're": "who are",
        "who've": "who have",
        "who's": "who is",
        "who'll": "who will",
        "who'll've": "who will have",
        "who'd": "who would",
        "who'd've": "who would have",
        "why're": "why are",
        "why'd": "why did",
        "why've": "why have",
        "why's": "why is",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "you're": "you are",
        "you've": "you have",
        "you'll've": "you shall have",
        "you'll": "you will",
        "you'd": "you would",
        "you'd've": "you would have",
        "You're" : "You are",
        "to cause": "to cause",
        "will cause": "will cause",
        "should cause": "should cause",
        "would cause": "would cause",
        "can cause": "can cause",
        "could cause": "could cause",
        "must cause": "must cause",
        "might cause": "might cause",
        "shall cause": "shall cause",
        "may cause": "may cause"
    }
    expanded_text = text
    for contraction, expanded in contractions.items():
        expanded_text = expanded_text.replace(contraction, expanded)

    return expanded_text

def tokenizeText(input):
    text = expand_contractions(input)
    token_pattern = r"""
        (?:[A-Za-z]\.)+|                
        \d{1,2}/\d{1,2}/\d{2,4}|        
        \d+(?:,\d{3})*(?:\.\d+)?|       
        \w+(?:-\w+)*|                    
        \b'[\w]+                         
    """
    tokens = re.findall(token_pattern, text, re.VERBOSE)
    tokens = [token.lower() for token in tokens]
    return tokens

def get_pairs_frequency(vocabs):
    '''
    from list of vocabulary to get pair_frequency
    '''
    pairs = collections.defaultdict(int)
    for word,freq in vocabs.items():
        symbols = word.split()
        # print(symbols)
        for i in range(len(symbols)-1):
            pairs[symbols[i],symbols[i+1]] += freq
    return pairs

def merge(pair,vocab):
    '''
    merge the max pair and update vocab, 
    '''
    output = {}
    bigram = re.escape(' '.join(pair))
    pattern = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in vocab:
        newword = pattern.sub(''.join(pair), word)
        output[newword] = vocab[word]
    # print(output)
    return output
    
def get_tokens(vocab):
    '''
    calculate tokens in the vocabulary, splite the ' ', and if merged, there will not ' ', so new token and its frequency appear
    '''
    # print(vocab)
    tokens = collections.defaultdict(int)
    for word, freq in vocab.items():
        word_tokens = word.split()
        # splite each word with ' '
        for token in word_tokens:
            tokens[token] += freq
    return tokens

def BPE(vocab, vocabSize):
    merged_rules = []
    tokens = get_tokens(vocab)
    while len(tokens) < vocabSize:
        pairs = get_pairs_frequency(vocab)
        if not pairs:
            break
        # find max pairs and merge
        best = max(pairs, key=pairs.get)
        # print(best)
        vocab = merge(best, vocab)
        # print(vocab)
        merged_rules.append(best)
        tokens = get_tokens(vocab)
        
    tokens = get_tokens(vocab)
    return tokens, merged_rules

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 preprocess.py <directory> <vocabSize>")
        sys.exit(1)

    directory = sys.argv[1]
    vocabSize = int(sys.argv[2])

    vocab = collections.defaultdict(int)
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='ISO-8859-1') as file:
                for line in file:
                    line = removeSGML(line)
                    tokens = tokenizeText(line)
                    for token in tokens:
                        vocab[' '.join(list(token)) + ' </w>'] += 1
    # pre-process each line by removeSGML and tokenizeText, and then update a directory named vocab，which collect all unique words show in the file and their frequency, and make each character in a word join a ' ' and each word end with <\w>
    tokens, merge_rules = BPE(vocab, vocabSize)
    
    sorted_tokens = sorted(tokens.items(), key=lambda item: item[1], reverse=True)
    sum = 0
    for token,freq in sorted_tokens:
        sum += freq
    
    with open('preprocess.output', 'w') as f:
        f.write("Tokens [{}]\n".format(sum))
        f.write("Merge rules [{}]\n".format(len(merge_rules)))
        f.write("The first 20 merge rules:\n")
        for rule in merge_rules[:20]:
            f.write("({}, {}) -> {}\n".format(rule[0], rule[1], ''.join(rule)))
        f.write("Top 50 tokens:\n")
        for token, freq in sorted(tokens.items(), key=lambda item: item[1], reverse=True)[:50]:
            f.write("{} [{}]\n".format(token, freq))
        
    
    count = 0
    newsum = 0
    for token,freq in sorted_tokens:
        if newsum < 0.25*sum:
            count += 1
            newsum += freq
        else:
            break
        
    # with open('preprocess.answers', 'w') as f:
    #     f.write("Tokens [{}]\n".format(sum))
    #     f.write("Merge rules [{}]\n".format(len(merge_rules)))
    #     f.write("{}\n".format(count))



