import numpy as np
from typing import Literal

class TokenGragh:
    def __init__(
        self, 
        windows_size:int = 5, 
        type: Literal['directed','undirected'] = 'undirected',
        mode: Literal['uniform','proportional'] = 'uniform',
        degree: Literal['in','out'] = 'out'
        ):
        self.windows_size = windows_size
        self.type = type
        self.mode = mode
        self.degree = degree

    #Line of tokens and its length
    def import_token_line(self, words):
        self.words = words.split()
        self.n_words = len(self.words)

    #Line of tokens and its length
    def import_token_list(self, tokens):
        self.tokens = tokens
        self.n_tokens = len(self.tokens)
    
    #index of scroll of tokens
    def build_index(self):
        self.index = dict(zip(self.tokens,list(range(self.n_tokens))))

    #create matrix in size n_tokens*n_tokens to save the graph of tokens
    def init_matrix(self):
        self.matrix = np.zeros((self.n_tokens, self.n_tokens), dtype = np.int32)

    #Build graph of tokens
    def build_matrix(self):
        for i in range(self.n_words):
        #controlling the limit of sliding window
            p = 0
            if(i + self.windows_size <= self.n_words):
                p = i + self.windows_size
            else:
                p = self.n_words
            #building graph
            for j in range(i + 1, p):
                if self.mode == "proportional":
                    self.matrix[self.index[self.words[i]]][self.index[self.words[j]]] += i + self.windows_size - j
                else:
                    self.matrix[self.index[self.words[i]]][self.index[self.words[j]]] += 1
                if self.type == "undirected":
                    self.matrix[self.index[self.words[j]]][self.index[self.words[i]]] = self.matrix[self.index[self.words[i]]][self.index[self.words[j]]]

    #Return the matrix of graph
    def get_matrix(self):
        return self.matrix

    #Centrality measure
    def centrality_measure(self):
        if self.type == "undirected":
            self.arr = np.zeros(self.n_tokens, dtype = np.int32)
            for i in range(self.n_tokens):
                self.arr[i] = np.sum(self.matrix[i]) + self.matrix[i][i]
        else:
            if self.degree == "out":
                self.arr = np.sum(self.matrix, axis=1)
            else:
                self.arr = np.sum(self.matrix, axis=0)

    #Return the feature vector
    def get_feature_vector(self):
        return self.arr
