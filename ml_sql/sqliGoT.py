import numpy as np
from typing import Literal
from tokenization import Tokenizer
from token_graph import TokenGragh
from tqdm import trange

#transfer all dataset by sqliGoT
def sqliGoT(
        X,
        windows_size:int = 5, 
        type: Literal['directed','undirected'] = 'undirected',
        mode: Literal['uniform','proportional'] = 'uniform',
        degree: Literal['in','out'] = 'out'
    ):
    feature_generator = TokenGragh(windows_size, type, mode, degree)
    tokenized = Tokenizer()
    token_list = tokenized.get_token_list()
    feature_generator.import_token_list(token_list)
    feature_generator.build_index()

    height = len(X)
    width = len(token_list)
    processed = np.zeros((height,width), dtype = np.int32)
    
    for i in trange(height):
        tokenized.import_query(X[i])
        tokenized.tokenization()
        feature_generator.import_token_line(tokenized.get_str())
        feature_generator.init_matrix()
        feature_generator.build_matrix()
        feature_generator.centrality_measure()
        processed[i] = feature_generator.get_feature_vector()
    
    return processed
