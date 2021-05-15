import multiprocessing as mp
import numpy as np

def init(seqs):
    global global_seqs
    global_seqs = seqs

def get_one_to_all_comparison_global(i, threshold=0.8):
    return np.greater(np.equal(global_seqs[i+1:], global_seqs[i].T).mean(1), threshold)
