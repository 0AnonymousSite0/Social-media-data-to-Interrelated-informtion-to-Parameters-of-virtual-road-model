import numpy as np

def set_seed(random_seed):
	np.random.seed(random_seed)

def read_vocab():
    vocab_file = 'vocab.txt'
    f = open(vocab_file,'r')
    words = f.readlines()
    f.close()
    return words


def generate_random_wrod():
    
    words = read_vocab()
    
    found_word = False
    
    while not found_word:
        
        random_number = np.random.randint(0,len(words))
        word = words[random_number]
        
        word = word.replace('\n', '')
        
        if not word.startswith('##'):
            found_word = True
    
    return word


def delete_random_words(text, probability):

    text_split = text.split()
    
    random_mask = np.random.choice(a=[False, True], size=(len(text_split)), \
                                   p=[probability, 1-probability])
        
    ret = [token for i, token in enumerate(text_split) if random_mask[i]]
    
    return " ".join(ret)

def replace_random_words(text, probability):
    
    text_split = text.split()
    
    random_array = np.random.choice(a=[False, True], size=(len(text_split)), \
                               p=[1-probability, probability])
        
    for i,replace in enumerate(random_array):
        if replace:
            text_split[i] = generate_random_wrod()
    
    return " ".join(text_split)


def insert_random_words(text, probability):
    
    text_split = text.split()

    i = 0
    while i<= len(text_split):
    
        replace = np.random.choice(a=[False, True], p=[1-probability, probability])
        
        if replace:
            text_split = text_split[:i] + [generate_random_wrod()] + text_split[i:]
            i += 1

        i += 1
    
    return " ".join(text_split)


def random_permutation(text):
    
    text_split = text.split()
    
    perm_list = np.random.permutation(text_split)
    
    return " ".join(perm_list)
