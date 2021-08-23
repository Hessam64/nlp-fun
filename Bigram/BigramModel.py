import nltk

from collections import defaultdict 
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.util import bigrams
import glob
import os
import ast


class BigramModel:
    
    def __init__(self , name = "default", dirName= '.', ext= "*", smooth = 0, stopWordList = [], otherWordList = []):
        
        self.name = name
        self.dirName = dirName
        self.ext = ext
        self.stopWordList = [x.lower() for x in stopWordList]
        self.otherWordList = [x.lower() for x in otherWordList] 
        self.smooth = smooth
        self.cleaned_sentences = []
        self.bigram_model = {}
        self.vocab = []
        self.error_messsage = 'probability has not been calculated.'
        
        
        self.load_corpus()
    
    
    def load_corpus(self):    
        
        file_list = glob.glob(os.path.join(os.getcwd(), self.dirName, "*." + self.ext))
        corpus = ''
        
        for index, file_path in enumerate(file_list):
            with open(file_path) as f_input:
                corpus += (f_input.read())
                if (index + 1 < len(file_path)):
                    corpus += ' '
        
        self.files = corpus
    
    def text_cleanup(self):
       
        sentences = sent_tokenize(self.files)
        cleaned_sentences = []
        all_words = set()
        self.vocab = []
        
        for sentence in sentences:
            sentence = sentence.translate(str.maketrans('','','^$*'))
            sentence = '^ ' + sentence + ' $'
            words = []
            tokens = word_tokenize(sentence.lower())
            
            for word in tokens:
                if (word.isalpha() or word == '$' or word == '^') and word not in self.stopWordList:
                    if (word in self.otherWordList):
                        words.append('*')
                        all_words.add('*')
                    else:
                        words.append(word)
                        all_words.add(word)
                  
            self.vocab = list(all_words)
            cleaned_sentences.append(' '.join(words).split())
        return cleaned_sentences
    
    def calculate(self):
        
        self.cleaned_sentences = self.text_cleanup()
        b_model = defaultdict(lambda: defaultdict(self.isValue))
      
        for w1 in self.vocab:
            for w2 in self.vocab:
                if ( (w1 != '$' and w2 !='^') and not (w1 == '^' and w2 =='$')):
                     b_model[w1][w2] = 0
        
        for sentence in self.cleaned_sentences:
            for w1, w2 in bigrams(sentence):
                b_model[w1][w2] += 1 
        for w1 in b_model:
            total = float(sum(b_model[w1].values()))
            den_co = len(self.vocab) -1
            if (w1 == '^'):
                den_co = len(self.vocab) -2
            for w2 in b_model[w1]:
                b_model[w1][w2] = (b_model[w1][w2] +  self.smooth)  / (total + ( self.smooth * den_co ))
                

        b_model = self.create_bigram_list(b_model)


        self.bigram_model =  [(x ,y ,z) for (x, y, z) in b_model if (z > 0.0 )]
        
        return self.bigram_model
        
    
    def isValue(self):
        return 0
    
    def Save(self):
        
        if len(self.bigram_model) == 0:
            self.calculate()
        with open(self.name + '.txt', 'w') as f:
            f.write(str(self.bigram_model))
        
    
    def Load(self):
        
        with open(self.name + '.txt', 'r') as f:
            self.bigram_model = ast.literal_eval(f.read())
        
        if len(self.bigram_model) == 0:
            return self.error_messsage
   
    
    def getAll(self, sortMethod = 0):
        
        if (len(self.bigram_model) == 0):
            return self.error_messsage
        
        if (sortMethod == 0):
            return self.bigram_model
        if (sortMethod == 1):
            return sorted (self.bigram_model, key=lambda elm: (elm[0]))
        if (sortMethod == 2):
            return sorted (self.bigram_model, key=lambda elm: elm[2], reverse=True)
        if (sortMethod == 3):
            return sorted (self.bigram_model, key=lambda elm: (elm[1]))
        
    
    def getProbList(self, w1, sortMethod = 0):
            
        result = [(y ,z) for (x, y, z) in self.bigram_model if (x == w1 )] 
        
        if (len(result)):
            if (sortMethod == 0):
                return result 
            if (sortMethod == 1):
                return sorted (result, key=lambda elm: elm[0])
            if (sortMethod == 2):
                return sorted (result, key=lambda elm: elm[1], reverse=True)
        
        return result
    
    def getProb(self, w1, w2):
        
        result = [(x ,y ,z) for (x, y, z) in self.bigram_model if (x == w1 and y == w2 )]
        
        if (len(result) == 0):
            return -1
        return result[0]
    
    
    def create_bigram_list(self, md):
        
        model = []
         
        for w1 in md :
            for w2 in md[w1]:
                 model.append((w1, w2, md[w1][w2]))
         
        return model