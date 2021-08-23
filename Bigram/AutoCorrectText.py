from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.corpus import gutenberg
import numpy as np
from collections import Counter
import string
from EditDistance import *

class AutoCorrectText(object):
    
    def __init__(self):
        
        dic = words.words()
        self.words =  [w.lower() for w in dic]
        self.three_grams = self.create_3gram_model(dic)
        self.word_prob_uni = self.calculate_unigram()
    
    
    def Correct(self,text):
        candidates = []
        result = []
        
        tokens = word_tokenize(text.lower())
        
        for index, word in enumerate(tokens):
            if (word.isalpha() and word not in self.words):
                
                candidates = []
                candidates = AutoCorrectText.suggest_words_jaccard(self.three_grams,word)
                edit_distance_one = AutoCorrectText.edit_distance_one(word)
                for w in edit_distance_one:
                    if w in self.words:
                        candidates = np.append(candidates, w)
                
                mydic = myDict(candidates)
                
                for i in range(10):
                    tmp_candidates = mydic.search(word , maxDistance = i)
                    if (len(tmp_candidates) != 0):
                        break
                
                candidates = tmp_candidates
                suggested_word = AutoCorrectText.cal_suggested_word(candidates, self.word_prob_uni)       
                result.append((index, word, suggested_word))

        return result
    
    @staticmethod
    def create_3gram_model(dic):
        
        three_grams = {}
        
        for index, word in enumerate (dic):
            three_grams[word] = AutoCorrectText.create_3_gram(word)
        
        return three_grams  
   
    @staticmethod
    def create_3_gram(word):
        
        return set([word[i:i+3] for i in range(len(word)-3+1)])
    
    @staticmethod
    def calculate_prob_jaccard_coefficient(w1,w2):
        #Ref: https://www.statisticshowto.com/jaccard-index/
        w1 = set(w1)
        w2 = set(w2)
        return len(w1.intersection(w2)) / len(w1.union(w2))

    
    def get_3_gram(self,w):
        return self.three_grams[w]
    
    @staticmethod
    def suggest_words_jaccard(three_grams, w1):
        suggested_words  = []
        w1 = AutoCorrectText.create_3_gram(w1)
        for item in three_grams:
            w2 = three_grams[item]
            prob = AutoCorrectText.calculate_prob_jaccard_coefficient(w1, w2)
            if prob > .3:
                suggested_words.append(item)

        return suggested_words
    

    @staticmethod    
    def calculate_unigram():

        words = []
        words = gutenberg.words(gutenberg.fileids())
        vocabs = set(words)
        all_words = Counter(words)
        total_words = float(sum(all_words.values()))
        word_probas = {word: all_words[word] / total_words for word in vocabs}
        
        return word_probas
    
    @staticmethod
    def edit_distance_one(word):
        
        #Ref: https://wolfgarbe.medium.com/1000x-faster-spelling-correction-algorithm-2012-8701fcd87a5f
        #Ref: https://colab.research.google.com/drive/1ySD8icJIDWDwuTKCcIn8TXf3Dl1xgsc4?usp=sharing
        lowercase = string.ascii_lowercase
        chop = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        return set([l + r[1:] for l,r in chop if r] +
           [l + c + r for l, r in chop for c in lowercase] +
           [l + r[1] + r[0] + r[2:] for l, r in chop if len(r)>1] + 
           [l + c + r[1:] for l, r in chop if r for c in lowercase] +  
           [l + c + r for l, r in chop for c in lowercase])
    
    
    @staticmethod
    def cal_suggested_word(suggested_words, unigram):
    
        max_p = -1
        suggested_word = -1

        if (len(suggested_words) > 0):
            suggested_word = suggested_words[0]

        for s_w in suggested_words:
            if (unigram.get(s_w, -1) !=-1 and unigram[s_w] > max_p):
                max_p = unigram[s_w] 
                suggested_word = s_w

        return suggested_word