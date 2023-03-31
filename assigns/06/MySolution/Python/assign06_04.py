####################################################
#!/usr/bin/env python3
####################################################
import sys
sys.path.append('../../../06')
sys.path.append('./../../../../mypylib')
from mypylib_cls import *
import queue
from dictwords import *
####################################################
"""
HX-2023-03-24: 30 points
Solving the doublet puzzle
"""
####################################################
def strsub(word,f):
    return word[f]

def string_length(word):
    return string_foldleft(word, 0, lambda r,_ : r+1)

def string_implode(word):
    return foreach_to_foldleft(fnlist_foreach)(word, "", lambda r,s: r+s)

def string_filter(word):
    return foreach_to_filter_fnlist(string_foreach)

def fnlist_tabulate(word,f):
    return fnlist_reverse(int1_foldleft(word,fnlist_nil(),lambda xs,i: fnlist_cons(f(i),xs)))

def string_tabulate(word,i):
    return string_implode(fnlist_tabulate(word,i))
    
def word_neighbors(word):
    """
    Note that this function should returns a fnlist
    (not a pylist)
    Your implementation should be combinator-based very
    much like the posted solution.
    """
    lens = string_length(word)
    AB =  "abcdefghijklmnopqrstuvwxyz"

    return fnlist_concat(string_imap_fnlist\
                      (word, lambda i, c: fnlist_concat\
                       (string_imap_fnlist(AB, lambda _, c1: fnlist_sing\
                                           (string_tabulate(lens, lambda j: strsub(word, j) if i != j else c1)) if (c != c1) else fnlist_nil()))))
####################################################
def is_legal(word):
    return fnlist_filter_pylist\
           (word_neighbors(word), word_is_legal)
####################################################
def wpath_neighbors_legal(wpath):
    word1 = wpath[-1]
    words = is_legal(word1)
    return [wpath+(word2,) for word2 in words]
####################################################
def gtree_bfs(nxs, fchildren):
    def helps(nxs):
        if nxs.empty():
            return strcon_nil()
        else:
            nx1 = nxs.get()
            for nx2 in fchildren(nx1):
                nxs.put(nx2)
            return strcon_cons(nx1, gtree_bfs(nxs,fchildren))
    return lambda: helps(nxs)
####################################################
def doublet_stream_from(word):
    """
    Please revisit assign05_02.py.
    ######
    Given a word w1 and another word w2, w1 and w2 are a
    1-step doublet if w1 and w2 differ at exactly one position.
    For instance, 'water' and 'later' are a 1-step doublet.
    The doublet relation is the reflexive and transitive closure
    of the 1-step doublet relation. In other words, w1 and w2 are
    a doublet if w1 and w2 are the first and last of a sequence of
    words where every two consecutive words form a 1-step doublet.
    Here is a little website where you can use to check if two words
    for a doublet or not:
    http://ats-lang.github.io/EXAMPLE/BUCS320/Doublets/Doublets.html
    ######
    Given a word, the function [doublet_stream_from] returns a stream
    enumerating *all* the tuples such that the first element of the tuple
    is the given word and every two consecutive words in the tuple form a
    1-step doublet. The enumeration of tuples should be done so that shorter
    tuples are always enumerated ahead of longer ones.
    ######
    """
    nxs = queue.Queue(); nxs.put((word,))
    return gtree_bfs(nxs, wpath_neighbors_legal)
####################################################
stream_iforall\
                (doublet_stream_from('water'), lambda i, x: i<100 and not(print(x)))
####################################################
